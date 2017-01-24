FROM python:2.7
MAINTAINER niusmallnan <niusmallnan@gmail.com>

ENV SOURCE_REPO https://github.com/niusmallnan/infra-service-upgrade-cli.git

RUN mkdir /root/.pip
COPY .pip.aliyun.conf /root/.pip/pip.conf
COPY .jessie.source.list /etc/apt/sources.list

RUN mkdir -p /app
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        && rm -rf /var/lib/apt/lists/* \
        && git clone $SOURCE_REPO \
        && cd infra-service-upgrade-cli \
        && pip install -r requirements.txt \
        && python setup.py develop

CMD ["/bin/bash"]
