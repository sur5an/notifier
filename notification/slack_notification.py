import os
from slack import WebClient
from slack.errors import SlackApiError
from slack import RTMClient
import traceback
from conversation import Conversation
import reminder
from util import Util
import logging


commands = {
    "list": reminder.Reminder().slack_list,
    "add": reminder.Reminder().add_new_reminder,
    "delete": reminder.Reminder().remove_reminder
}


@RTMClient.run_on(event='message')
def listener(**payload):
    data = payload['data']
    web_client = payload['web_client']
    # rtm_client = payload['rtm_client']
    user = data['user']

    try:
        msg = f"Hi <@{user}>!\n"
        channel_id = data['channel']
        thread_ts = data['ts']
        conversation_id = data.get('thread_ts')
        event_ts = data.get('event_ts', 0)
        text = str(data['text'])
        match = False
        if conversation_id is None:
            conversation_id = thread_ts
        elif Conversation.active_con.get(conversation_id) is not None:
            text = Conversation.active_con[conversation_id].get("command")

        if float(conversation_id) + 300.0 < float(event_ts):
            msg += "`This conversation is expired please start a new conversation` \n `-Thanks`\n"
        elif len(text.split()) > 1:
            try:
                token = text.split()
                if token[0].strip().lower() == "doc":
                    for cmd in commands:
                        if cmd == token[1].strip().lower():
                            msg += commands.get(cmd)(str(data['text']), conversation_id, user)
                            match = True
            except Exception as e:
                traceback.print_exc()
                logging.error(f"Got an error inside module: " + str(e))
                msg = "Something went wrong - you might have found a bug please report it.\n - Thanks"
            if not match:
                msg += "`I didn't get you. can you try some thing else.`"
        web_client.chat_postMessage(
            channel=channel_id,
            text=msg,
            thread_ts=thread_ts
        )
    except Exception as e:
        # You will get a SlackApiError if "ok" is False
        traceback.print_exc()
        logging.error(f"Got an error: " + str(e))


class SlackNotification:
    SLACK_NOTIFICATION_ENABLED = True
    SLACK_CHANNEL_USER = None

    @staticmethod
    def slack_setup():
        SlackNotification.update_feature()
        if SlackNotification.SLACK_NOTIFICATION_ENABLED:
            rtm_client = RTMClient(token=os.environ["SLACK_API_TOKEN"])
            rtm_client.start()

    @staticmethod
    def update_feature():
        SlackNotification.SLACK_CHANNEL_USER = Util.get_env_variable("SLACK_NOTIFY_CHANNEL", "notifications")
        if Util.check_env_variable(["SLACK_API_TOKEN"]) is False:
            SlackNotification.disable_slack()

    @staticmethod
    def disable_slack():
        SlackNotification.SLACK_NOTIFICATION_ENABLED = False

    @staticmethod
    def get_slack_message(records, cd):
        if not SlackNotification.SLACK_NOTIFICATION_ENABLED:
            return None
        if len(records) == 0:
            return ":large_blue_circle: *%s*: No Alerts for Now\n" % cd
        response_message = ":red_circle: *%s*: `ALERT` \n _Records expiring or expired_" \
                           "\n _please check the following documents_ \n\n" % cd
        for record in records:
            response_message += "*%s*: _%s_\n" % (record["UserName"], record["DocumentName"])
        return response_message

    @staticmethod
    def notify(tn, ref_date):
        message = SlackNotification.get_slack_message(tn, ref_date)
        if message is None:
            return True
        client = WebClient(token=os.environ['SLACK_API_TOKEN'])

        try:
            response = client.chat_postMessage(
                channel='#%s' % SlackNotification.SLACK_CHANNEL_USER,
                text="%s" % message)
            logging.info("Send message to slack: %s" % response)
            return True
        except SlackApiError as e:
            logging.error(f"Got an error: {e.response['error']}")
        return False


if __name__ == '__main__':
    SlackNotification.notify("notifications", "test message")

