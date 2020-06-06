import smtplib
import os
from util import Util

message = """From: SURSAN-PI <EMAIL_ADDRESS>
To: Sudharsan <EMAIL_ADDRESS>
MIME-Version: 1.0
Content-type: text/html
Subject: Message for SURSAN-PI - DATED

<style>
table {
  width:100%;
}
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  padding: 15px;
  text-align: left;
}
table#t01 tr:nth-child(even) {
  background-color: #eee;
}
table#t01 tr:nth-child(odd) {
 background-color: #fff;
}
table#t01 th {
  background-color: black;
  color: white;
}
</style>

MESSAGE_BODY
"""


class EMailNotification:
    EMAIL_NOTIFICATION_ENABLED = True
    EMAIL_PASSWORD = None
    EMAIL_ADDRESS = None

    @staticmethod
    def update_feature():
        if "EMAIL_ADDRESS" not in os.environ or "EMAIL_PASSWORD" not in os.environ:
            EMailNotification.disable_email()

    @staticmethod
    def disable_email():
        EMailNotification.EMAIL_NOTIFICATION_ENABLED = False

    @staticmethod
    def email_setup():
        if Util.check_env_variable(["EMAIL_ADDRESS", "EMAIL_PASSWORD"]) is False:
            EMailNotification.disable_email()
        elif EMailNotification.EMAIL_NOTIFICATION_ENABLED:
            EMailNotification.EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
            EMailNotification.EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
            os.environ["EMAIL_PASSWORD"] = "reset"
            file = "/etc/ssmtp/ssmtp.conf"
            hostname = None
            for line in open(file, "r").readlines():
                if line.find("hostname=") >= 0:
                    hostname = line
                    break
            fin = open(file, "w+")
            fin.write("%s" % hostname.strip())
            fin.write('\nUseSTARTTLS=YES\n%s' % Util.get_env_variable("EMAIL_SERVER", "mailhub=smtp.gmail.com:587"))
            fin.write("\nAuthUser=%s" % EMailNotification.EMAIL_ADDRESS)
            fin.write("\nAuthPass=%s" % EMailNotification.EMAIL_PASSWORD)
            fin.close()

    @staticmethod
    def get_email_message(records):
        if not EMailNotification.EMAIL_NOTIFICATION_ENABLED:
            return None

        if len(records) == 0:
            return "No Alerts for Now"
        response_message = '<h1> ALERT - Records expiring or expired. </h1>' \
                           '<br/><p><b>please check the following documents</p></b><br/>'
        response_message += '<table id="t01"><tr><th>Name</th><th>DocumentName</th></tr>'
        for record in records:
            response_message += "<tr><td>%s</td><td>%s</td></tr>" % (record["UserName"], record["DocumentName"])
        response_message += '</table>'
        return response_message

    @staticmethod
    def send_email(tn, dated):
        body = EMailNotification.get_email_message(tn)
        if body is None:
            return
        msg = ""
        for line in message.split('\n'):
            if line.find("EMAIL_ADDRESS") >= 0:
                line = line.replace("EMAIL_ADDRESS", EMailNotification.EMAIL_ADDRESS)
            if line.find("DATED") >= 0:
                line = line.replace("DATED", dated)
            if line.find("MESSAGE_BODY") >= 0:
                line = line.replace("MESSAGE_BODY", body)
            msg += line + "\n"

        smtp_server = smtplib.SMTP('smtp.gmail.com', '587')
        smtp_server.starttls()
        smtp_server.login(EMailNotification.EMAIL_ADDRESS, EMailNotification.EMAIL_PASSWORD)
        smtp_server.sendmail(EMailNotification.EMAIL_ADDRESS, EMailNotification.EMAIL_ADDRESS, msg)
        print("Successfully sent email")

