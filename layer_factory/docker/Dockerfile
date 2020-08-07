FROM amazonlinux:2.0.20200722.0

RUN yum update -y \
    && yum install -y wget tar gzip make \
    gcc openssl-devel bzip2-devel libffi-devel \
    git zip \
    && cd /opt \
    && wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz \
    && tar xzf Python-3.8.5.tgz \
    && cd Python-3.8.5 \
    && ./configure --enable-optimizations \
    && make altinstall \
    && rm -f /opt/Python-3.8.5.tgz \
    && rm -rf /var/cache/yum/* \
    && yum clean all \
    && mkdir -p /var/task/python

COPY entrypoint.sh /usr/local/bin/
WORKDIR /var/task

ENTRYPOINT [ "entrypoint.sh" ]
