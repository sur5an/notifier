sudo docker stop notifier
sudo docker rm notifier
sudo docker build -t notifier .
sudo docker run --name notifier -p 1888:1888 --env-file notification/environment_key.list -d -t notifier

