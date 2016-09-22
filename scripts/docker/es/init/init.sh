#!/bin/bash

echo 'do init action'
mkdir -p /var/log/elasticsearch
chown -R elasticsearch /var/log/elasticsearch
chown -R elasticsearch /srv/esdata

#init network
function checkvar(){
  if [ ! $2 ]; then
    echo ERROR: need  $1
    exit 1
  fi
}

IFACE=${IFACE:-pbond0}

checkvar IP $IP
checkvar NETMASK $NETMASK
checkvar GATEWAY $GATEWAY

#network
cat > /etc/sysconfig/network-scripts/ifcfg-$IFACE << EOF
DEVICE=$IFACE
ONBOOT=yes
BOOTPROTO=static
IPADDR=$IP
NETMASK=$NETMASK
GATEWAY=$GATEWAY
EOF
ifconfig $IFACE $IP/16
echo 'set network successfully'

#route
gateway=`echo $IP | cut -d. -f1,2`.0.1
route add default gw $gateway
route del -net 0.0.0.0 netmask 0.0.0.0 dev eth0

#hosts
umount /etc/hosts
cat > /etc/hosts <<EOF
127.0.0.1 localhost
$IP     `hostname`
EOF
echo 'set host successfully'

#unzip file to es
if [ ! -d "/usr/share/elasticsearch/plugins/head" ]; then
cd /tmp
/usr/bin/unzip elasticsearch-head-master.zip
/usr/bin/unzip elasticsearch-kopf-master.zip
/usr/bin/unzip elasticsearch-sql.zip

mv elasticsearch-head-master /usr/share/elasticsearch/plugins/head
mv elasticsearch-kopf-master /usr/share/elasticsearch/plugins/kopf
mv elasticsearch-sql-2.3.2.0 /usr/share/elasticsearch/plugins/sql

chmod 755 /usr/share/elasticsearch/plugins/head
chmod 755 /usr/share/elasticsearch/plugins/kopf
chmod 755 /usr/share/elasticsearch/plugins/sql

echo 'unzip file to es'
fi

#set elasticsearch
cat > /etc/sysconfig/elasticsearch << EOF
ES_HOME=/usr/share/elasticsearch
MAX_OPEN_FILES=65535
MAX_MAP_COUNT=262144
LOG_DIR=/var/log/elasticsearch
DATA_DIR=/var/lib/elasticsearch
WORK_DIR=/tmp/elasticsearch
CONF_DIR=/etc/elasticsearch
ES_HEAP_SIZE=8g
ES_HEAP_NEWSIZE=1g
ES_JAVA_OPTS="\$JAVA_OPTS -XX:+UseCondCardMark -XX:CMSWaitDuration=250 -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly"
ES_USER=root
EOF
echo 'set es'

#set elasticsearch.yml
is_wr1=`grep inline /etc/elasticsearch/elasticsearch.yml|wc -l`
if [ $is_wr1 -eq 0 ]; then
cat >> /etc/elasticsearch/elasticsearch.yml << EOF
script.inline: on
script.indexed: on
EOF
echo 'set elasticsearch.yml'
fi

#open root run es
is_wr2=`grep insecure /usr/share/elasticsearch/bin/elasticsearch.in.sh|wc -l`
if [ $is_wr2 -eq 0 ]; then
cat >> /usr/share/elasticsearch/bin/elasticsearch.in.sh << EOF
JAVA_OPTS="\$JAVA_OPTS -Des.insecure.allow.root=true"
EOF
fi


