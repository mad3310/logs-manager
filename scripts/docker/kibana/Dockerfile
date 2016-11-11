FROM letv:centos6
MAINTAINER bingzheng.zhou <zhoubingzheng@letv.com>

RUN rpm -ivh http://pkg-repo.oss.letv.com/pkgs/centos6/letv-release.noarch.rpm

RUN yum install -y vim
RUN yum install -y wget
RUN yum install -y tar
RUN yum install -y cronie

RUN mkdir -p /usr/local/init/

#setup kibana(This version of Kibana requires Elasticsearch 2.3.0+ on all nodes)
RUN /usr/bin/wget --no-check-certificate https://s3.lecloud.com/matrix/plugins/ELK/kibana-4.5.4-linux-x64.tar.gz
RUN /bin/tar -xvzf kibana-4.5.4-linux-x64.tar.gz
RUN mv kibana-4.5.4-linux-x64 /opt/kibana
RUN rm -rf kibana-4.5.4-linux-x64.tar.gz
ADD init/kibana /etc/init.d/kibana
RUN chmod u+x  /etc/init.d/kibana

# install monit
RUN yum install -y monit
ADD ./init/monit /etc/init.d/monit
RUN chmod 755 /etc/init.d/monit

# add init script
ADD init/init.sh /usr/local/init/init.sh
RUN chmod 755 /usr/local/init/init.sh

RUN yum install -y logs-manager

ENTRYPOINT bash /usr/local/init/init.sh && service logs-manager start &&  /bin/bash
