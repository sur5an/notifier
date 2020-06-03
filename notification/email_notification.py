import smtplib

message = """From: SURSAN-PI <EMAIL_ADDRESS>
To: Sudharsan <EMAIL_ADDRESS>
Subject: Message for SURSAN-PI - DATED

<html>
<body>
MESSAGE_BODY
</body>
</html>
"""


class EMailNotification:
    @staticmethod
    def send_email(body, email_address, dated, password):
        msg = ""
        for line in message.split('\n'):
            if line.find("EMAIL_ADDRESS") >= 0:
                line = line.replace("EMAIL_ADDRESS", email_address)
            if line.find("DATED") >= 0:
                line = line.replace("DATED", dated)
            if line.find("MESSAGE_BODY") >= 0:
                line = line.replace("MESSAGE_BODY", body)
            msg += line + "\n"

        smtp_server = smtplib.SMTP('smtp.gmail.com', '587')
        smtp_server.starttls()
        smtp_server.login(email_address, password)
        print (msg)
        smtp_server.sendmail(email_address, email_address, msg)
        print("Successfully sent email")

