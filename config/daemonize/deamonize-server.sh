sudo tee /etc/systemd/system/docker-server-compose.service <<EOF
[Unit]
Description=Docker Compose Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=true
WorkingDirectory=/bata/src/cleanCopy/components/master2
ExecStart=docker compose up --scale backend=2 -d --build 
ExecStop=docker compose down

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable docker-server-compose
sudo systemctl start docker-server-compose