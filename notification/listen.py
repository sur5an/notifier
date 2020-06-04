import os, sys
import time
from slack import RTMClient
import reminder
import document_db
import traceback
from conversation import Conversation
from multiprocessing import Process
from notify import Notify
import simple_server
import logging

commands = {
    "list": reminder.Reminder().slack_list,
    "add": reminder.Reminder().add_new_reminder,
    "delete": reminder.Reminder().remove_reminder
}


def configure_logging():
    my_log_file_name = "db/" + os.path.basename(__file__) + ".log"
    logging.basicConfig(filename=my_log_file_name,
                        filemode='a',
                        format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                        datefmt='%D %H:%M:%S',
                        level=logging.INFO)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s,%(msecs)03d  %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


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
                print(f"Got an error inside module: " + str(e))
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
        print(f"Got an error: " + str(e))


def start_db():
    try:
        document_db.Documents().select_users()
    except:
        document_db.Documents().create_schema()


def start_slack():
    if "SLACK_API_TOKEN" not in os.environ or "SLACK_API_TOKEN" not in os.environ:
        Notify.disable_slack()
        return
    rtm_client = RTMClient(token=os.environ["SLACK_API_TOKEN"])
    rtm_client.start()


def alert_cron():
    Notify.setup_email()
    while True:
        Notify().check_notification()
        time.sleep(60*60*12)


if __name__ == '__main__':
    configure_logging()
    start_db()
    method_list = [start_slack, alert_cron, simple_server.start_server]
    for m in method_list:
        p = Process(target=m, args=(), name=str(m.__name__))
        print(p.name)
        p.start()
