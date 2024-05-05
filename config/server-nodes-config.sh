#needed stuff for distributed nodes
#1-docker

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

#add user to docker group
sudo usermod -aG docker $USER
newgrp docker
######
. /bata/config/daemonize/deamonize-server.sh
##needed by efs for ubuntu
# cd ~
# sudo apt-get update
# sudo apt-get -y install git binutils rustc cargo pkg-config libssl-dev
# git clone https://github.com/aws/efs-utils
# cd efs-utils
# ./build-deb.sh
# sudo apt-get -y install ./build/amazon-efs-utils*deb
# #cleanup
# cd ~
# sudo rm -rf efs-utils

# for amazon linux instances, just 
#sudo yum install amazon-efs-utils
#sudo mkdir /bata
#sudo chmod 777 /bata
#sudo mount -t efs -o tls fs-0ff5500b92ccda99c:/ /bata
#sudo chmod 777 /bata
