from twilio.rest import Client
import os
from util import Util


class WhatsAppNotification:
    WHATS_APP_NOTIFICATION_ENABLED = True
    ACCOUNT_SID = None
    SMS_AUTH_TOKEN = None
    WHATS_APP_FROM_NUMBER = None
    TO_NUMBER = None

    @staticmethod
    def update_feature():
        if Util.check_env_variable(["ACCOUNT_SID", "SMS_AUTH_TOKEN", "WHATS_APP_FROM_NUMBER", "TO_NUMBER",
                                    "ENABLE_WHATS_APP"]) is False:
            WhatsAppNotification.disable_whats_app()
        else:
            WhatsAppNotification.SMS_AUTH_TOKEN = os.environ.get("SMS_AUTH_TOKEN")
            WhatsAppNotification.ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
            WhatsAppNotification.WHATS_APP_FROM_NUMBER = 'whatsapp:' + os.environ.get("WHATS_APP_FROM_NUMBER")
            WhatsAppNotification.TO_NUMBER = 'whatsapp:' + os.environ.get("TO_NUMBER")

    @staticmethod
    def disable_whats_app():
        WhatsAppNotification.WHATS_APP_NOTIFICATION_ENABLED = False

    @staticmethod
    def get_whats_app_message(records, cd):
        if not WhatsAppNotification.WHATS_APP_NOTIFICATION_ENABLED:
            return None
        if len(records) == 0:
            return None

        response_message = "*%s*: _Records expiring or expired_" \
                           "\n _please check the following documents_ \n\n" % cd
        for record in records:
            response_message += "*%s*: _%s_\n" % (record["UserName"], record["DocumentName"])
        return response_message

    @staticmethod
    def notify_through_whats_app(recs, ref_date):
        msg = WhatsAppNotification.get_whats_app_message(recs, ref_date)
        if msg is None:
            return
        client = Client(WhatsAppNotification.ACCOUNT_SID, WhatsAppNotification.SMS_AUTH_TOKEN)

        message = client.messages.create(
            body=str(msg),
            from_=str(WhatsAppNotification.WHATS_APP_FROM_NUMBER),
            to=str(WhatsAppNotification.TO_NUMBER)
        )

        print(message.sid)
