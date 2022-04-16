FROM debian:11

COPY --from=docker:dind /usr/local/bin/docker /usr/local/bin/

RUN apt update && apt upgrade -y && \
    apt install -y sudo python3 python3-pip

RUN pip3 install flask docker pyjwt

COPY ./ /root/

EXPOSE 80

RUN chmod +x "/root/entrypoint.sh"

ENTRYPOINT [ "/root/entrypoint.sh" ]