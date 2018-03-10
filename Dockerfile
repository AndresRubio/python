FROM ubuntu:16.04
#TODO: try alphine

RUN apt-get update && \
    apt-get install -y software-properties-common vim && \
    add-apt-repository ppa:jonathonf/python-3.6 && \
    apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv

# update pip
RUN python3 -m pip install pip --upgrade && \
    python3 -m pip install numpy

WORKDIR /usr/src/app

COPY ./*.py ./
COPY input.txt .
CMD ["python3","main.py"]