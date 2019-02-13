FROM ubuntu:cosmic

RUN apt-get -y update && \
    apt-get -y install python3 python3-pip git && \
    pip3 install ansible ansible-lint yamllint && \
    mkdir /ansible

WORKDIR /ansible

CMD /bin/bash
