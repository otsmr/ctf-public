#!/bin/bash

service ssh start

useradd -m -p $(openssl passwd -1 $ENV_SSH_PASSWORD) -s /bin/bash user
echo 'user ALL=(root) NOPASSWD: /usr/sbin/iptables, /usr/bin/tcpdump -i lo tcp -A' >> /etc/sudoers

sudo -u ctf python3 /home/ctf/alice.py & \
    sudo -u ctf python3 /home/ctf/bob.py
