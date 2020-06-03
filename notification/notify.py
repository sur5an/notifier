from document_db import Documents
from datetime import datetime
from slack_notification import SlackNotification
from email_notification import EMailNotification
import os


class Notify:
    SLACK_NOTIFICATION_ENABLED = True
    EMAIL_NOTIFICATION_ENABLED = True
    SMS_NOTIFICATION_ENABLED = True
    EMAIL_PASSWORD = None
    LAST_NOTIFY_DATE = None

    @staticmethod
    def setup_email():
        if Notify.EMAIL_NOTIFICATION_ENABLED:
            if "EMAIL_ADDRESS" not in os.environ or "EMAIL_PASSWORD" not in os.environ:
                print("disabling email alert as email is not sent")
                Notify.disable_email()
                return
            email_address = os.environ["EMAIL_ADDRESS"]
            Notify.EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
            os.environ["EMAIL_PASSWORD"] = "reset"
            file = "/etc/ssmtp/ssmtp.conf"
            hostname = None
            for line in open(file, "r").readlines():
                if line.find("hostname=") >= 0:
                    hostname = line
                    break
            fin = open(file, "w+")
            fin.write("%s" % hostname.strip())
            fin.write('\nUseSTARTTLS=YES\nmailhub=smtp.gmail.com:587')
            fin.write("\nAuthUser=%s" % email_address)
            fin.write("\nAuthPass=%s" % Notify.EMAIL_PASSWORD)
            fin.close()

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
    def get_email_message(records):
        if not Notify.SLACK_NOTIFICATION_ENABLED or len(records) == 0:
            return "No Alerts for Now"
        response_message = '<p style="color:red;"> ALERT - Records expiring or expired. </p>' \
                           '<br/><p><b>please check the following documents</p></b><br/>'
        response_message += '<table><tr><th>Column</th><th>Details</th></tr>'
        for record in records:
            response_message += "<tr><td>%s</td><td>%s</td></tr>" % (record["UserName"], record["DocumentName"])
        response_message += '</table>'
        return response_message

    @staticmethod
    def get_slack_message(records):
        if not Notify.SLACK_NOTIFICATION_ENABLED:
            return None
        if len(records) == 0:
            return ":large_blue_circle: No Alerts for Now"
        response_message = ":red_circle: `ALERT` ```Records expiring or expired. \nplease check the documents```\n"
        for record in records:
            response_message += "*%s*: _%s_\n" % (record["UserName"], record["DocumentName"])
        return response_message

    def check_notification(self):
        check_date = datetime.combine(datetime.today(), datetime.min.time())
        print("check_date: %s" % check_date)
        to_notify, already_expired = self.doc.get_records_to_notify(check_date)

        if len(to_notify) <= 0 or check_date == Notify.LAST_NOTIFY_DATE:
            return

        Notify.LAST_NOTIFY_DATE = check_date
        slack_msg = Notify.get_slack_message(to_notify)
        if slack_msg is not None:
            SlackNotification.notify("notifications", slack_msg)

        email_msg = Notify.get_email_message(to_notify)
        if email_msg is not None:
            EMailNotification.send_email(email_msg, os.environ["EMAIL_ADDRESS"], str(check_date), Notify.EMAIL_PASSWORD)


def main():
    Notify().check_notification()
