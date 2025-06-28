import unittest
from unittest.mock import patch, MagicMock
import requests
import os
from slack_sdk.errors import SlackApiError

from main import fetch_and_save_trends, get_trends_from_twitter, save_trends_to_db, notify_slack

class MockResponse:
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP Error {self.status_code}")

class TestTrendCrawler(unittest.TestCase):

    @patch("main.get_trends_from_twitter")
    @patch("main.save_trends_to_db")
    @patch("main.notify_slack")
    def test_fetch_and_save_trends_flow(
        self, mock_notify_slack, mock_save_trends_to_db, mock_get_trends_from_twitter
    ):
        """
        トレンド取得、DB保存、通知の一連の流れをテストする
        """
        # --- Arrange (準備) ---
        mock_trends = [
            {"name": "#Python", "url": "http://twitter.com/search?q=%23Python"},
            {"name": "#FastAPI", "url": "http://twitter.com/search?q=%23FastAPI"},
        ]
        mock_get_trends_from_twitter.return_value = mock_trends
        mock_save_trends_to_db.return_value = len(mock_trends)

        # --- Act (実行) ---
        result = fetch_and_save_trends()

        # --- Assert (検証) ---
        mock_get_trends_from_twitter.assert_called_once()
        mock_save_trends_to_db.assert_called_once_with(mock_trends)
        mock_notify_slack.assert_called_once_with("2件のトレンドを保存しました。")
        self.assertEqual(result, 2)

    @patch("requests.get")
    def test_get_trends_from_twitter_success(self, mock_requests_get):
        """
        Twitterからトレンドを正常に取得できることをテストする
        """
        # --- Arrange (準備) ---
        mock_html = """
        <html>
            <body>
                <a href="http://twitter.com/search?q=%23Python">#Python</a>
                <a href="http://twitter.com/search?q=%23FastAPI">#FastAPI</a>
            </body>
        </html>
        """
        mock_requests_get.return_value = MockResponse(mock_html, 200)

        # --- Act (実行) ---
        trends = get_trends_from_twitter()

        # --- Assert (検証) ---
        self.assertEqual(len(trends), 2)
        self.assertEqual(trends[0]["name"], "#Python")
        self.assertEqual(trends[0]["url"], "http://twitter.com/search?q=%23Python")
        self.assertEqual(trends[1]["name"], "#FastAPI")
        self.assertEqual(trends[1]["url"], "http://twitter.com/search?q=%23FastAPI")

    @patch("requests.get")
    def test_get_trends_from_twitter_http_error(self, mock_requests_get):
        """
        HTTPエラーが発生した場合にNoneが返ることをテストする
        """
        # --- Arrange (準備) ---
        mock_requests_get.return_value = MockResponse("Not Found", 404)

        # --- Act (実行) ---
        trends = get_trends_from_twitter()

        # --- Assert (検証) ---
        self.assertIsNone(trends)

    @patch.dict(os.environ, {"DB_NAME": "test_db", "DB_USER": "test_user", "DB_PASSWORD": "test_pass", "DB_HOST": "localhost", "DB_PORT": "5432"})
    @patch("psycopg2.connect")
    @patch("psycopg2.extras.execute_values")
    def test_save_trends_to_db_success(self, mock_execute_values, mock_connect):
        """
        トレンドをDBに正常に保存できることをテストする
        """
        # --- Arrange (準備) ---
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 2

        trends = [
            {"name": "#Test1", "url": "http://test.com/1"},
            {"name": "#Test2", "url": "http://test.com/2"},
        ]

        # --- Act (実行) ---
        result = save_trends_to_db(trends)

        # --- Assert (検証) ---
        mock_connect.assert_called_once()
        mock_execute_values.assert_called_once()
        mock_conn.commit.assert_called_once()
        self.assertEqual(result, 2)

    @patch.dict(os.environ, {"DB_NAME": "test_db", "DB_USER": "test_user", "DB_PASSWORD": "test_pass", "DB_HOST": "localhost", "DB_PORT": "5432"})
    @patch("psycopg2.connect")
    def test_save_trends_to_db_error(self, mock_connect):
        """
        DB保存時にエラーが発生した場合にロールバックされ、0が返ることをテストする
        """
        # --- Arrange (準備) ---
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.side_effect = Exception("DB Error")

        trends = [{"name": "#Error", "url": "http://error.com"}]

        # --- Act (実行) ---
        result = save_trends_to_db(trends)

        # --- Assert (検証) ---
        mock_conn.rollback.assert_called_once()
        self.assertEqual(result, 0)

    @patch.dict(os.environ, {"SLACK_API_TOKEN": "test_token", "SLACK_CHANNEL": "#test_channel"})
    @patch("main.WebClient")
    def test_notify_slack_success(self, mock_slack_client):
        """
        Slackへの通知が正常に成功することをテストする
        """
        # --- Arrange (準備) ---
        mock_client_instance = MagicMock()
        mock_slack_client.return_value = mock_client_instance
        mock_client_instance.chat_postMessage.return_value = {"ok": True}

        message = "テストメッセージ"

        # --- Act (実行) ---
        notify_slack(message)

        # --- Assert (検証) ---
        mock_slack_client.assert_called_once_with(token="test_token")
        mock_client_instance.chat_postMessage.assert_called_once_with(channel="#test_channel", text=message)

    @patch.dict(os.environ, {"SLACK_API_TOKEN": "test_token", "SLACK_CHANNEL": "#test_channel"})
    @patch("main.WebClient")
    def test_notify_slack_error(self, mock_slack_client):
        """
        Slack通知時にエラーが発生した場合をテストする
        """
        # --- Arrange (準備) ---
        mock_client_instance = MagicMock()
        mock_slack_client.return_value = mock_client_instance
        mock_response = {"ok": False, "error": "invalid_auth"}
        mock_client_instance.chat_postMessage.side_effect = SlackApiError(
            message="Slack API Error",
            response=mock_response
        )

        # --- Act (実行) & Assert (検証) ---
        with self.assertLogs('main', level='ERROR') as cm:
            notify_slack("エラーメッセージ")
            self.assertIn("Error sending Slack notification: invalid_auth", cm.output[0])

if __name__ == "__main__":
    unittest.main()

