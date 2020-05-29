docker build .
docker tag 2b4318682957 notifier
docker run --env SLACK_API_TOKEN=<Pass> -d -t notifier

apt install software-properties-common mariadb-server mariadb-client
/etc/init.d/mysql stop

#RUN \
#    apt install software-properties-common -y
#
#RUN \
#    export DEBIAN_FRONTEND=noninteractive \
#    && rm -f /tmp/m \
#    && echo 'mariadb-server-10.0 mysql-server/root_password password $MARIADB_PASS' >> /tmp/m \
#    && echo 'mariadb-server-10.0 mysql-server/root_password_again password $MARIADB_PASS' >> /tmp/m \
#    && debconf-set-selections /tmp/m \
#    && apt-get install mariadb-server mariadb-client -y \
#    && /etc/init.d/mysql restart