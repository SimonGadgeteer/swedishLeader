FROM ubuntu
MAINTAINER schwasi2@students.zhaw.ch
RUN apt-get -y update && apt-get install -y python3 && apt-get install -y git-all
RUN git clone https://github.com/SimonGadgeteer/swedishLeader.git
EXPOSE 1001-8000
ENTRYPOINT python /usr/swedishLeader/app.py