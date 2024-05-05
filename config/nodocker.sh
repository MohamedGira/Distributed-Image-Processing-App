#!/bin/bash
# #sudo apt-get install python-dev   # for python2.x installs
# sudo dpkg --configure -a
# sudo apt-get update
# sudo apt-get install python3-pip -y
# sudo apt-get install python3-dev -y  # for python3.x installs
# sudo apt install build-essential 
# sudo apt-get install openmpi-bin openmpi-doc libopenmpi-dev 
# pip install -r /bata/src/cleanCopy/components/execution/nodocker_reqs.txt --break-system-packages 


sudo apt-get update && sudo apt-get install ffmpeg libsm6 libxext6  -y #opencv deps
sudo apt-get update && sudo apt-get install -y python3-opencv
# for node in mpi-worker-01 mpi-worker-02  mpi-worker-03 mpi-worker-04
# do
#   scp -i $1 $1 $node:$2
# done

# for node in mpi-worker-01 mpi-worker-02  mpi-worker-03 mpi-worker-04
# do
#   ssh ubuntu@$node "tee /etc/hosts << EOF `cat /bata/src/cleanCopy/components/execution/hosts` EOF"
# done


for node in mpi-worker-01 mpi-worker-02  mpi-worker-03 mpi-worker-04
do
  ssh ubuntu@$node "sudo apt-get update && sudo apt-get install -y python3-opencv"
done