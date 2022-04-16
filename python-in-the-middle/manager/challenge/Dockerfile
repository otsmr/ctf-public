FROM debian:latest

RUN apt update && apt upgrade -y && \
    apt install -y sudo python3 python3-pip iptables netcat openssh-server tcpdump

RUN pip3 install flask pycryptodome

RUN useradd ctf -ms /bin/bash && \
    chown -R root.ctf /home/ctf && chmod -R 755 /home/ctf

COPY . /home/ctf
RUN chown -R ctf.ctf /home/ctf/secret.py && \
    chmod 0600 /home/ctf/secret.py

EXPOSE 22

COPY "./entrypoint.sh" "/root/"

RUN chmod +x "/root/entrypoint.sh"

ENTRYPOINT [ "./root/entrypoint.sh" ]