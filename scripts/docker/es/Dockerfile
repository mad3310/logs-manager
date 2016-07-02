FROM 10.160.140.32:5000/letv-centos6
MAINTAINER bingzheng.zhou <zhoubingzheng@letv.com>

RUN rpm -ivh http://pkg-repo.oss.letv.com/pkgs/centos6/letv-release.noarch.rpm
RUN yum install java-1.7.0-openjdk-devel -y

RUN yum install -y vim

RUN alias vi='vim'
RUN alias ll='ls -l'

#elasticsearch
ADD init/elasticsearch-1.5.1.noarch.rpm /opt/elasticsearch-1.5.1.noarch.rpm
RUN rpm -ivh /opt/elasticsearch-1.5.1.noarch.rpm

ADD init/init.sh /tmp/init.sh
RUN chmod 755  /tmp/init.sh

RUN yum install -y logs-manager

ENTRYPOINT bash /tmp/init.sh && service logs-manager start &&  /bin/bash