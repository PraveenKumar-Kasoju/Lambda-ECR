FROM ubuntu:20.04

RUN apt-get install -y python3.8 python3.8-venv python3.8-dev python3-pip

CMD ["/bin/bash"]
