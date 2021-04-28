
FROM alpine:3.7

RUN apt update && apt -y install sudo

RUN useradd -m usuario && echo "usuario:grupo" | chpasswd && adduser usuario sudo

USER usuario

CMD /bin/bash

RUN sudo apt update


