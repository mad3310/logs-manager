FROM letv:centos6
MAINTAINER bingzheng.zhou <zhoubingzheng@letv.com>

RUN rpm -ivh http://pkg-repo.oss.letv.com/pkgs/centos6/letv-release.noarch.rpm

RUN yum install -y vim

RUN alias vi='vim'
RUN alias ll='ls -l'

RUN mkdir -p /usr/local/init/

#kibana
ADD init/kibana-4.0.2-linux-x64.tar.gz /tmp/kibana-4.0.2-linux-x64.tar.gz
ADD init/kibana /etc/init.d/kibana
RUN chmod u+x  /etc/init.d/kibana


ADD init/init.sh /usr/local/init/init.sh
RUN chmod 755 /usr/local/init/init.sh

RUN yum install -y logs-manager

ENTRYPOINT bash /usr/local/init/init.sh && service logs-manager start &&  /bin/bash
