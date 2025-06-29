import pytest
from unittest.mock import Mock, patch
from slack_sdk.errors import SlackApiError

# テスト対象の関数をインポート
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from notifier.slack_notify import send_trends_to_slack

@patch('notifier.slack_notify.WebClient')
def test_send_trends_to_slack_success(mock_web_client):
    """
    トレンド情報が正常にSlackに送信されることをテストする
    """
    # WebClientのモックを設定
    mock_instance = mock_web_client.return_value
    mock_instance.chat_postMessage.return_value = {"ok": True}

    trends = ["#トレンド1", "トレンド2", "トレンド3"]
    slack_channel = "#test-channel"
    slack_token = "xoxp-test-token"

    # テスト対象の関数を実行
    send_trends_to_slack(trends, slack_channel, slack_token)

    # chat_postMessageが正しい引数で呼び出されたことを確認
    mock_web_client.assert_called_once_with(token=slack_token)
    mock_instance.chat_postMessage.assert_called_once_with(
        channel=slack_channel,
        text="現在のXのトレンドです！\n- #トレンド1\n- トレンド2\n- トレンド3"
    )

@patch('notifier.slack_notify.WebClient')
def test_send_trends_to_slack_no_trends(mock_web_client):
    """
    トレンド情報が空の場合、Slackに通知しないことをテストする
    """
    mock_instance = mock_web_client.return_value

    trends = []
    slack_channel = "#test-channel"
    slack_token = "xoxp-test-token"

    send_trends_to_slack(trends, slack_channel, slack_token)

    # chat_postMessageが呼び出されないことを確認
    mock_instance.chat_postMessage.assert_not_called()

@patch('notifier.slack_notify.WebClient')
def test_send_trends_to_slack_api_error(mock_web_client):
    """
    Slack APIがエラーを返した場合の挙動をテストする
    """
    # chat_postMessageがSlackApiErrorを発生させるように設定
    mock_instance = mock_web_client.return_value
    mock_instance.chat_postMessage.side_effect = SlackApiError("API Error", {"ok": False, "error": "some_error"})

    trends = ["#トレンド1"]
    slack_channel = "#test-channel"
    slack_token = "xoxp-test-token"

    # SlackApiErrorが発生することを確認
    with pytest.raises(SlackApiError):
        send_trends_to_slack(trends, slack_channel, slack_token)
