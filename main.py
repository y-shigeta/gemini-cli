
import requests
from bs4 import BeautifulSoup

def get_trends_from_twitter():
    """Twitterからトレンドを取得する"""
    try:
        # 実際のURLに置き換える必要があります
        response = requests.get("https://twitter.com/i/trends")
        response.raise_for_status() # HTTPエラーがあれば例外を発生
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trends: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    trends = []
    # 実際のHTML構造に合わせてセレクタを調整する必要があります
    for a_tag in soup.find_all("a"):
        if a_tag.has_attr("href") and "/search?q=" in a_tag["href"]:
            trends.append({
                "name": a_tag.text,
                "url": a_tag["href"]
            })
    return trends


import os
import psycopg2
import psycopg2.extras

def save_trends_to_db(trends):
    """トレンドをデータベースに保存する"""
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            dbname=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"]
        )
        cursor = conn.cursor()

        # (仮のテーブル名・カラム名)
        # CREATE TABLE trends (id SERIAL PRIMARY KEY, name VARCHAR(255), url VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        sql = "INSERT INTO trends (name, url) VALUES %s"
        
        # execute_valuesで効率的に複数行を挿入
        data = [(t["name"], t["url"]) for t in trends]
        psycopg2.extras.execute_values(cursor, sql, data)
        
        saved_count = cursor.rowcount
        conn.commit()
        return saved_count

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        if conn:
            conn.rollback()
        return 0

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# ロガーの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

def notify_slack(message):
    """Slackに通知する"""
    try:
        client = WebClient(token=os.environ["SLACK_API_TOKEN"])
        client.chat_postMessage(
            channel=os.environ["SLACK_CHANNEL"],
            text=message
        )
    except SlackApiError as e:
        logger.error(f"Error sending Slack notification: {e.response['error']}")
    except Exception as e:
        logger.error(f"Error sending Slack notification: {e}")

def fetch_and_save_trends():
    """
    トレンドを取得し、DBに保存し、結果を通知する
    """
    trends = get_trends_from_twitter()
    if trends:
        saved_count = save_trends_to_db(trends)
        notify_slack(f"{saved_count}件のトレンドを保存しました。")
        return saved_count
    else:
        notify_slack("トレンドは0件でした。")
        return 0
