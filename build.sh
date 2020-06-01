docker build -t notifier .
docekr rm notifier
docker run --name notifier --env SLACK_API_TOKEN=pass -d -t notifier