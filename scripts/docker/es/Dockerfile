FROM letv:centos6
MAINTAINER bingzheng.zhou <zhoubingzheng@letv.com>

RUN rpm -ivh http://pkg-repo.oss.letv.com/pkgs/centos6/letv-release.noarch.rpm
RUN yum install java-1.7.0-openjdk-devel-1.7.0.101 -y

RUN yum install -y vim
RUN yum install -y unzip
RUN yum install -y tar
RUN yum install -y gcc python-devel python-pip
RUN yum install -y wget

RUN mkdir -p /usr/local/init/

#elasticsearch
RUN /usr/bin/wget --no-check-certificate https://s3.lecloud.com/matrix/plugins/ELK/elasticsearch-2.3.2.rpm
RUN rpm -ivh elasticsearch-2.3.2.rpm
RUN rm -rf elasticsearch-2.3.2.rpm

#add es plugin
RUN /usr/bin/wget --no-check-certificate https://s3.lecloud.com/matrix/plugins/ELK/elasticsearch-head-master.zip
RUN /usr/bin/wget --no-check-certificate https://s3.lecloud.com/matrix/plugins/ELK/elasticsearch-kopf-master.zip
RUN /usr/bin/wget --no-check-certificate https://s3.lecloud.com/matrix/plugins/ELK/elasticsearch-sql.zip
RUN /usr/bin/unzip elasticsearch-head-master.zip
RUN /usr/bin/unzip elasticsearch-kopf-master.zip
RUN /usr/bin/unzip elasticsearch-sql.zip
RUN rm -rf elasticsearch-head-master.zip
RUN rm -rf elasticsearch-kopf-master.zip
RUN rm -rf elasticsearch-sql.zip 
RUN mv elasticsearch-head-master /usr/share/elasticsearch/plugins/head
RUN mv elasticsearch-kopf-master /usr/share/elasticsearch/plugins/kopf
RUN mv elasticsearch-sql-2.3.2.0 /usr/share/elasticsearch/plugins/sql
RUN chmod 755 /usr/share/elasticsearch/plugins/head
RUN chmod 755 /usr/share/elasticsearch/plugins/kopf
RUN chmod 755 /usr/share/elasticsearch/plugins/sql

# add init script
ADD init/init.sh /usr/local/init/init.sh
RUN chmod 755 /usr/local/init/init.sh

RUN yum install -y logs-manager


ENTRYPOINT bash /usr/local/init/init.sh && service logs-manager start &&  /bin/bash
