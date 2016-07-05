FROM letv:centos6
MAINTAINER bingzheng.zhou <zhoubingzheng@letv.com>

RUN rpm -ivh http://pkg-repo.oss.letv.com/pkgs/centos6/letv-release.noarch.rpm
RUN yum install java-1.7.0-openjdk-devel -y

RUN yum install -y vim

RUN alias vi='vim'
RUN alias ll='ls -l'

RUN mkdir -p /usr/local/init/

#logstash
ADD init/logstash-1.4.2-1_2c0f5a1.noarch.rpm /tmp/logstash-1.4.2-1_2c0f5a1.noarch.rpm
ADD init/logstash.conf /etc/logstash/conf.d/logstash.conf
RUN rpm -ivh /tmp/logstash-1.4.2-1_2c0f5a1.noarch.rpm

ADD init/init.sh /usr/local/init/init.sh
RUN chmod 755  /usr/local/init/init.sh

RUN yum install -y logs-manager

ENTRYPOINT bash /usr/local/init/init.sh && service logs-manager start &&  /bin/bash
