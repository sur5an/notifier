sudo docker build -t notifier .
sudo docker rm notifier
sudo docker run --name notifier -v documents.db:/var/notification/documents.db --env SLACK_API_TOKEN=pass -d -t notifier
