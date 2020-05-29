import os
from slack import RTMClient
from slack.errors import SlackApiError
import reminder

commands = {
    "list": reminder.slack_list
}


@RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    # rtm_client = payload['rtm_client']
    user = data['user']

    msg = f"Hi <@{user}>!\n"
    channel_id = data['channel']
    thread_ts = data['ts']
    try:
        for cmd in commands:
            if cmd == data['text'].split(":")[0].strip():
                msg += commands.get(cmd)(data['text'].split(':'))
    except Exception as e:
        print(e)
        msg += e
    try:
        web_client.chat_postMessage(
            channel=channel_id,
            text=msg,
            thread_ts=thread_ts
        )
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        print(f"Got an error: {e.response['error']}")


rtm_client = RTMClient(token=os.environ["SLACK_API_TOKEN"])
rtm_client.start()