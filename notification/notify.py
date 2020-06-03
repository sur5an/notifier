from document_db import Documents
from datetime import datetime
from slack_notification import SlackNotification


class Notify:
    SLACK_NOTIFICATION_ENABLED = True
    EMAIL_NOTIFICATION_ENABLED = True
    SMS_NOTIFICATION_ENABLED = True

    LAST_NOTIFY_DATE = None

    def __init__(self):
        self.doc = Documents()

    @staticmethod
    def disable_slack():
        Notify.SLACK_NOTIFICATION_ENABLED = False

    @staticmethod
    def disable_email():
        Notify.EMAIL_NOTIFICATION_ENABLED = False

    @staticmethod
    def disable_sms():
        Notify.SMS_NOTIFICATION_ENABLED = False

    @staticmethod
    def get_slack_message(records):
        if not Notify.SLACK_NOTIFICATION_ENABLED or len(records) == 0:
            return None
        response_message = ":red_circle: `ALERT` ```Records expiring or expired. \nplease check the documents```\n"
        for record in records:
            response_message += "*%s*: _%s_\n" % (record["UserName"], record["DocumentName"])
        return response_message

    def check_notification(self):
        check_date = datetime.combine(datetime.today(), datetime.min.time())
        to_notify, already_expired = self.doc.get_records_to_notify(check_date)

        if len(to_notify) <= 0 or check_date == Notify.LAST_NOTIFY_DATE:
            return

        Notify.LAST_NOTIFY_DATE = check_date
        slack_msg = Notify.get_slack_message(to_notify)
        if slack_msg is not None:
            SlackNotification.notify("notifications", slack_msg)


def main():
    Notify().check_notification()
