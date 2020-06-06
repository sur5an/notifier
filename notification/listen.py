import os
import time
import document_db
from multiprocessing import Process
from notify import Notify
import simple_server
import logging
from slack_notification import SlackNotification


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


def start_db():
    try:
        document_db.Documents().select_users()
    except:
        document_db.Documents().create_schema()


def alert_cron():
    configure_logging()
    Notify.setup()
    while True:
        Notify().check_notification()
        time.sleep(60*60*12)


if __name__ == '__main__':
    configure_logging()
    start_db()
    method_list = [SlackNotification.slack_setup, alert_cron, simple_server.start_server]
    for m in method_list:
        p = Process(target=m, args=(), name=str(m.__name__))
        print(p.name)
        p.start()
