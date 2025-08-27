FROM ubuntu

RUN apt-get update
RUN apt-get install vim sudo curl python3 python3-pip -y

RUN useradd -m -s /bin/bash -G sudo coder
# Let's add a fancy prompt!
RUN echo "PS1='�~_~P� \[\033[1;36m\]\h \[\033[1;34m\]\W\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'" > /home/coder/.bashrc && \
    chown coder:coder /home/coder/.bashrc

USER coder
