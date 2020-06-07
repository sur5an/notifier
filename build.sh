sudo docker stop notifier
sudo docker rm notifier
sudo docker build -t notifier .
sudo docker run --cap-add=SYS_ADMIN --cap-add DAC_READ_SEARCH --name notifier -p 1888:1888 --env-file notification/environment_key.list -v /home/ubuntu/git/notifier/notifier_db:/var/notification/db -d -t notifier
