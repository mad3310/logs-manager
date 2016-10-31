FROM letv:centos6
MAINTAINER bingzheng.zhou <zhoubingzheng@letv.com>

RUN rpm -ivh http://pkg-repo.oss.letv.com/pkgs/centos6/letv-release.noarch.rpm
RUN yum install java-1.7.0-openjdk-devel -y

RUN yum install -y vim

RUN alias vi='vim'
RUN alias ll='ls -l'

RUN mkdir -p /usr/local/init/
RUN yum install -y logrotate
RUN yum install -y wget

#logstash
RUN cd /tmp
RUN /usr/bin/wget --no-check-certificate https://10.154.29.92:443/v1/AUTH_gaoqiang3/oss/logstash-2.4.0.noarch.rpm
RUN rpm -ivh logstash-2.4.0.noarch.rpm
ADD init/logstash.conf /etc/logstash/conf.d/logstash.conf


ADD init/init.sh /usr/local/init/init.sh
RUN chmod 755  /usr/local/init/init.sh

# install monit
RUN yum install -y wget
RUN yum install -y monit
ADD ./init/monit /etc/init.d/monit
RUN chmod 755 /etc/init.d/monit

RUN yum install -y logs-manager

ENTRYPOINT bash /usr/local/init/init.sh && service logs-manager start &&  /bin/bash