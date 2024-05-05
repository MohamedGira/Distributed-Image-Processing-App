#!/bin/bash
#make sure you have security perms (some security group on aws)
cd ~
sudo apt-get update
sudo apt-get -y install git binutils rustc cargo pkg-config libssl-dev
git clone https://github.com/aws/efs-utils
cd efs-utils
./build-deb.sh
sudo apt-get -y install ./build/amazon-efs-utils*deb
#cleanup
cd ~
sudo rm -rf efs-utils
sudo mkdir /bata
sudo chmod 777 /bata
sudo mount -t efs -o tls fs-0c1ff19a9ae971e45.efs.eu-central-1.amazonaws.com:/ /bata
sudo chmod 777 /bata

sudo tee -a /etc/fstab <<EOF
fs-0c1ff19a9ae971e45.efs.eu-central-1.amazonaws.com:/ /bata nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport,_netdev 0 0
EOF