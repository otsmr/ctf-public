#!/bin/bash

echo "docker build image"
cd /root/challenge
docker build -t python_in_the_middle .

echo "start manager.py"
cd /root
python3 manager.py

# docker run -it --env ENV_SSH_PASSWORD=password --cap-add=NET_ADMIN --cap-add=NET_RAW -p 8585:22 python_in_the_middle /bin/bash