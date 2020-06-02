from document_db import Documents
from datetime import datetime
from slack_notification import SlackNotification


class Notify:
    ENABLE_SLACK = True
    ENABLE_EMAIL = True
    ENABLE_SMS = True

    def __init__(self):
        self.doc = Documents()

    @staticmethod
    def disable_slack():
        Notify.ENABLE_SLACK = False

    @staticmethod
    def disable_email():
        Notify.ENABLE_EMAIL = False

    @staticmethod
    def disable_sms():
        Notify.ENABLE_SMS = False

    @staticmethod
    def get_slack_message(records):
        if len(records) == 0:
            return None
        response_message = ":red_circle: `ALERT` ```Records expiring or expired. \nplease check the documents```\n"
        for record in records:
            response_message += "*%s*: _%s_\n" % (record["UserName"], record["DocumentName"])
        return response_message

    def check_notification(self):
        to_notify, already_expired = \
            self.doc.get_records_to_notify(datetime.combine(datetime.today(), datetime.min.time()))
        slack_msg = Notify.get_slack_message(to_notify)
        if slack_msg is not None:
            SlackNotification.notify("notifications", slack_msg)


def main():
    Notify().check_notification()
