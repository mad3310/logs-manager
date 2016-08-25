FROM letv:centos6
MAINTAINER bingzheng.zhou <zhoubingzheng@letv.com>

RUN rpm -ivh http://pkg-repo.oss.letv.com/pkgs/centos6/letv-release.noarch.rpm
RUN yum install java-1.7.0-openjdk-devel -y

RUN yum install -y vim
RUN yum install -y unzip
RUN yum install -y tar
RUN yum install -y gcc python-devel python-pip

RUN alias vi='vim'
RUN alias ll='ls -l'


RUN mkdir -p /usr/local/init/

#elasticsearch
ADD init/elasticsearch-1.5.1.noarch.rpm /tmp/elasticsearch-1.5.1.noarch.rpm
RUN rpm -ivh /tmp/elasticsearch-1.5.1.noarch.rpm

ADD init/bigdesk-master.zip /tmp/bigdesk-master.zip
ADD init/elasticsearch-head-master.zip /tmp/elasticsearch-head-master.zip
ADD init/elasticsearch-kopf-master.zip /tmp/elasticsearch-kopf-master.zip

ADD init/init.sh /usr/local/init/init.sh
RUN chmod 755 /usr/local/init/init.sh

RUN yum install -y logs-manager


ENTRYPOINT bash /usr/local/init/init.sh && service logs-manager start &&  /bin/bash
