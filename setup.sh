mkdir git
git clone https://github.com/sur5an/notifier.git
mkdir notifier_db
sudo mkdir /var/mount
sudo apt-get install cifs-utils -y
sudo apt-get install sqlite3 libsqlite3-dev -y
sudo apt  install docker.io -y
sudo apt install network-manager -y
sudo apt install net-tools -y
#sudo mount.cifs //IP/share /var/mount/ -o user=<user>
#cp /var/mount/ notifier_db/documents.db
#nmcli d wifi list
#nmtui -- connect to wifi
sudo echo "[Unit]
Description=notifier
Requires=docker.service
After=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker start -a notifier
ExecStop=/usr/bin/docker stop -t 2 notifier

[Install]
WantedBy=default.target" | sudo tee /etc/systemd/system/docker-notifier.service
sudo systemctl enable docker-notifier.service
#./build.sh
sudo reboot

