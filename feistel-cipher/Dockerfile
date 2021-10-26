FROM debian:latest

RUN apt update && apt upgrade -y && \
    apt install -y python3

COPY files /ctf/

RUN groupadd -r ctf && useradd -r -g ctf ctf
USER ctf

EXPOSE 1337

ENTRYPOINT [ "python3", "/ctf/server.py" ]