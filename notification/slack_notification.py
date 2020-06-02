import os
from slack import WebClient
from slack.errors import SlackApiError


class SlackNotification:

    @staticmethod
    def notify(channel, message):
        client = WebClient(token=os.environ['SLACK_API_TOKEN'])

        try:
            response = client.chat_postMessage(
                channel='#%s' % channel,
                text="%s" % message)
        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")


if __name__ == '__main__':
    SlackNotification.notify("notifications", "test message")

