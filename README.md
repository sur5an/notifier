# Notifier

* The core of this project is to sent notification to users thru various medium (slack/sms/whatsapp/email) about expiring user documents
* This project uses sqlite database to store user document information. 
* Based on documents expire date and reminder start date - first notification will be sent.
* the following notification are sent based on notification frequency. 
* example say your document expires in 12 months and notification start is 1Y, then today the first 
notification will be sent and say notification frequency is 1M, notification will be sent every month.
* To enter the details on document, port 1888 runs a simple python server, which expose web page to add and delete records.
* you can also use slack bot to add and delete records (doc list/add/delete commands in slack channel/bot will give you the details)  
  
 
## EMail Notification 
1. To enable email notification you need to add proper value in EMAIL_ADDRESS and EMAIL_PASSWORD
1. Byt default EMAIL_SERVER is gmail (code is rt now tested only with gmail)
1. In your gmail account you need to enable [Less secure app access](https://myaccount.google.com/security)  
1. any of these details if missed in environment_key.list, then email will be disabled for notification

## SMS Notification
1. In this project we use twilo account for sending sms - please follow instruction and get the following details 
1. ACCOUNT_SID, SMS_AUTH_TOKEN, SMS_FROM_NUMBER, TO_NUMBER
1. any of these details if missed in environment_key.list, then sms will be disabled for notification

## Whatsapp Notification
1. In this project we use twilo account for sending whatsapp message - please follow instruction and get the following details 
1. ACCOUNT_SID, SMS_AUTH_TOKEN, WHATS_APP_FROM_NUMBER, TO_NUMBER
1. any of these details if missed in environment_key.list, then sms will be disabled for notification
 
## slack notification
1. Create a slack workspace and a legacy api bot
1. pass the slack bot token in SLACK_API_TOKEN
1. SLACK_NOTIFY_CHANNEL is notification by default - you can pass any value thru environment_key.list
