#!/bin/bash

service ssh start

useradd -m -p $(openssl passwd -1 $ENV_SSH_PASSWORD) -s /bin/bash user
echo 'user ALL=(root) NOPASSWD: /usr/sbin/iptables, /usr/sbin/tcpdump -i lo tcp and port 1337 -A' >> /etc/sudoers

sudo -u ctf python3 /home/ctf/alice.py & \
    sudo -u ctf python3 /home/ctf/bob.py