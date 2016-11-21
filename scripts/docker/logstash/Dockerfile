FROM letv:centos6
MAINTAINER bingzheng.zhou <zhoubingzheng@letv.com>

RUN rpm -ivh http://pkg-repo.oss.letv.com/pkgs/centos6/letv-release.noarch.rpm
RUN yum install java-1.7.0-openjdk-devel-1.7.0.101 -y

RUN yum install -y vim
RUN yum install -y cronie

RUN mkdir -p /usr/local/init/
RUN yum install -y logrotate
RUN yum install -y wget

#logstash
RUN /usr/bin/wget --no-check-certificate https://s3.lecloud.com/matrix/plugins/ELK/logstash-2.3.4-1.noarch.rpm
RUN rpm -ivh logstash-2.3.4-1.noarch.rpm
RUN rm -rf logstash-2.3.4-1.noarch.rpm
ADD init/logstash.conf /etc/logstash/conf.d/logstash.conf

# install monit
RUN yum install -y wget
RUN yum install -y monit
ADD ./init/monit /etc/init.d/monit
RUN chmod 755 /etc/init.d/monit

# install monit
ADD init/init.sh /usr/local/init/init.sh
RUN chmod 755  /usr/local/init/init.sh

RUN yum install -y logs-manager

ENTRYPOINT bash /usr/local/init/init.sh && service logs-manager start &&  /bin/bash