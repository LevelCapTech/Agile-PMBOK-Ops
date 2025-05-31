import os
import requests

class MissingEnvironmentVariableError(RuntimeError):
    """Raised when a required environment variable is missing."""

SLACK_TOKEN = os.environ.get("SLACK_USER_TOKEN")
if not SLACK_TOKEN:
    raise MissingEnvironmentVariableError("SLACK_USER_TOKEN 環境変数が設定されていません")


def set_presence_away():
    """
    Slackのユーザーのプレゼンスを「離席中（away）」に設定します。

    Slack APIの `users.setPresence` エンドポイントを利用して、
    認証済みユーザーのプレゼンスを「away」に変更します。
    """
    url = "https://slack.com/api/users.setPresence"
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"presence": "away"}
    response = requests.post(url, headers=headers, json=data)
    if response.ok and response.json().get("ok"):
        print("setPresence succeeded:", response.json())
    else:
        raise Exception(f"Failed to set presence: {response.json()}")


def set_custom_status():
    """
    Slackのユーザーステータスをカスタムメッセージ「離席中です」と
    絵文字「:coffee:」に設定します。

    Slack APIの `users.profile.set` エンドポイントを利用して、
    認証済みユーザーのプロフィールステータスを更新します。
    """
    url = "https://slack.com/api/users.profile.set"
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "profile": {
            "status_text": "離席中です",
            "status_emoji": ":coffee:",
            "status_expiration": 0
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print("profile.set:", response.json())


if __name__ == "__main__":
    """
    スクリプトを直接実行した場合、Slackのプレゼンスを「away」にし、
    ステータスを「離席中です :coffee:」に設定します。
    """
    set_presence_away()
    set_custom_status()
