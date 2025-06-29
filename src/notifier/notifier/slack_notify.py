from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def send_trends_to_slack(trends, slack_channel, slack_token):
    if not trends:
        return
    client = WebClient(token=slack_token)
    text = "現在のXのトレンドです！\n" + "\n".join(f"- {t}" for t in trends)
    try:
        client.chat_postMessage(channel=slack_channel, text=text)
    except SlackApiError as e:
        raise 