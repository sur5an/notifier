from document_db import Documents
from datetime import datetime
from slack_notification import SlackNotification
from email_notification import EMailNotification
from whatsapp import WhatsAppNotification
from sms_notification import SMSNotification


class Notify:
    LAST_NOTIFY_DATE = None

    @staticmethod
    def enable_disable_features():
        EMailNotification.update_feature()
        SlackNotification.update_feature()
        WhatsAppNotification.update_feature()
        SMSNotification.update_feature()

    @staticmethod
    def setup():
        Notify.enable_disable_features()

        EMailNotification.email_setup()

    def __init__(self):
        self.doc = Documents()
        Notify.enable_disable_features()

    def check_notification(self):
        check_date = datetime.combine(datetime.today(), datetime.min.time())
        print("check_date: %s" % check_date)
        to_notify, already_expired = self.doc.get_records_to_notify(check_date)

        if len(to_notify) <= 0 or check_date == Notify.LAST_NOTIFY_DATE:
            return

        Notify.LAST_NOTIFY_DATE = check_date

        notification_channel = [
            SlackNotification.notify,
            EMailNotification.send_email,
            WhatsAppNotification.notify_through_whats_app,
            SMSNotification.notify_through_sms
        ]

        for nc in notification_channel:
            nc(to_notify, str(check_date).split()[0])


def main():
    Notify().check_notification()
