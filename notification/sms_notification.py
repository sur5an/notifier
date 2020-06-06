from twilio.rest import Client
import os
from util import Util


class SMSNotification:
    SMS_NOTIFICATION_ENABLED = True
    ACCOUNT_SID = None
    SMS_AUTH_TOKEN = None
    SMS_FROM_NUMBER = None
    TO_NUMBER = None

    @staticmethod
    def update_feature():
        if Util.check_env_variable(["ACCOUNT_SID", "SMS_AUTH_TOKEN", "SMS_FROM_NUMBER", "TO_NUMBER", "ENABLE_SMS"]) is \
                False:
            SMSNotification.disable_sms()
        else:
            SMSNotification.SMS_AUTH_TOKEN = os.environ.get("SMS_AUTH_TOKEN")
            SMSNotification.ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
            SMSNotification.SMS_FROM_NUMBER = os.environ.get("SMS_FROM_NUMBER")
            SMSNotification.TO_NUMBER = os.environ.get("TO_NUMBER")

    @staticmethod
    def disable_sms():
        SMSNotification.SMS_NOTIFICATION_ENABLED = False

    @staticmethod
    def get_sms_message(records, cd):
        if not SMSNotification.SMS_NOTIFICATION_ENABLED:
            return None
        if len(records) == 0:
            return None

        response_message = "*%s*: _Records expiring or expired_" \
                           "\n _please check the following documents_ \n\n" % cd
        for record in records:
            response_message += "*%s*: _%s_\n" % (record["UserName"], record["DocumentName"])
        return response_message

    @staticmethod
    def notify_through_sms(recs, ref_date):
        msg = SMSNotification.get_sms_message(recs, ref_date)
        if msg is None:
            return
        client = Client(SMSNotification.ACCOUNT_SID, SMSNotification.SMS_AUTH_TOKEN)

        message = client.messages.create(
            body=str(msg),
            from_=str(SMSNotification.SMS_FROM_NUMBER),
            to=str(SMSNotification.TO_NUMBER)
        )

        print(message.sid)
