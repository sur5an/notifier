sudo docker build -t notifier .
sudo docker rm notifier
touch documents.db
sudo docker run --name notifier -v documents.db:/var/notification/documents.db --env SLACK_API_TOKEN=pass -d -t notifier