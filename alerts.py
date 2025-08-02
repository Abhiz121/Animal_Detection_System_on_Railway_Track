import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"  # Replace with your webhook URL

def send_slack_alert():
    message = {
        "text": "⚠️ *Animal Detected on Railway Track!* \nPlease take immediate action."
    }
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        if response.status_code == 200:
            print("✅ Slack alert sent successfully.")
        else:
            print(f"❌ Slack alert failed: {response.status_code} {response.text}")
    except Exception as e:
        print("❌ Error sending Slack alert:", e)