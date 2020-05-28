docker build --build-arg MARIADB_PASS=${MARIADB_PASS} .
docker tag 2b4318682957 notifier
docker run --env SLACK_API_TOKEN=xoxb-1139702237570-1134730520423-pplQtfEU3sZWNDsgafG8WMAM -d -p 3306:3306 -t notifier

apt install software-properties-common mariadb-server mariadb-client
/etc/init.d/mysql stop
