FROM ubuntu
MAINTAINER schwasi2@students.zhaw.ch
RUN apt-get -y update && apt-get install -y python3 && apt-get install -y git-all && apt-get install python-pip python-dev build-essential -y
RUN git clone https://github.com/SimonGadgeteer/swedishLeader.git
WORKDIR /swedishLeader
RUN pip install -r requirements.txt
EXPOSE 5050
#CMD "python --version"

#not yet working
CMD ["/usr/bin/python", "/swedishLeader/app.py"]