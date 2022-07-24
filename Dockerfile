# Build container

FROM ubuntu:latest

WORKDIR /root
COPY tests/requirements.txt test_requirements.txt
COPY requirements.txt requirements.txt

RUN apt-get update &&\
    apt-get install --yes build-essential &&\
    apt-get install --yes pip

RUN pip install -r requirements.txt
RUN pip install -r test_requirements.txt

ENTRYPOINT ["make"]

# EOF

 
