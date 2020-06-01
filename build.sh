sudo docker build -t notifier .
sudo docker rm notifier
sudo docker run --name notifier -v /var/notfier_db:/var/notification/db --env SLACK_API_TOKEN=pass -d -t notifier
