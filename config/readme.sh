to daemonize docker use --restart, or restart:true in docker-compose.


create a file to start at boot 
1.





#create a systemd service file for Docker Compose:Create a systemd service file, for example, docker-compose.service, in /etc/systemd/system/ with the following content:
#
#[Unit]
#Description=Docker Compose Application
#Requires=docker.service
#After=docker.service
#
#[Service]
#Type=oneshot
#RemainAfterExit=true
#WorkingDirectory=/path/to/your/docker-compose/project
#ExecStart=docker compose up -d #can replace with docker run for simple cases
#
#[Install]
#WantedBy=multi-user.target
#
#sudo systemctl enable docker-compose
#sudo systemctl start docker-compose


















