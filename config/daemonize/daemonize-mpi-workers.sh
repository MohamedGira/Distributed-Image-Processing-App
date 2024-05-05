# #!/bin/bash
# sudo tee /etc/systemd/system/mpi-worker.service <<EOF
# [Unit]
# Description=Mpi-Run-Sample
# After = network.target  bata.mount

# [Service]
# Type=simple
# WorkingDirectory=/bata/src/cleanCopy/components/execution
# ExecStart=nohup /bata/venv/bin/python3 mpi_spawner.py >> /bata/mpi_spawner.log
# Restart=always
# [Install]
# WantedBy=multi-user.target
# EOF

# sudo systemctl enable mpi-worker
# sudo systemctl stop mpi-worker
# sudo systemctl start mpi-worker

#damonize doesnt work well we will use crom

sudo apt update
sudo apt install cron
sudo systemctl enable cron