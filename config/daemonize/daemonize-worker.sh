sudo tee /etc/systemd/system/docker-worker-compose.service <<EOF
[Unit]
Description=Docker Compose Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=true
WorkingDirectory=/bata/src/cleanCopy/components/execution
ExecStart=docker compose up -d --build
ExecStop=docker compose down

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable docker-worker-compose
sudo systemctl start docker-worker-compose