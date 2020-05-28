docker build .
docker tag 2b4318682957 mybase
docker run --env SLACK_API_TOKEN=xoxb-1139702237570-1134730520423-pplQtfEU3sZWNDsgafG8WMAM -i -t mybase -d
