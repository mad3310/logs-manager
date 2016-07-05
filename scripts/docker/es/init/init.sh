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
if [ ! -d "/usr/share/elasticsearch/plugins/bigdesk" ]; then
cd /tmp
/usr/bin/unzip bigdesk-master.zip
/usr/bin/unzip elasticsearch-head-master.zip
/usr/bin/unzip elasticsearch-kopf-master.zip
mv bigdesk-master /usr/share/elasticsearch/plugins/bigdesk
mv elasticsearch-head-master /usr/share/elasticsearch/plugins/head
mv elasticsearch-kopf-master /usr/share/elasticsearch/plugins/kopf
chmod 755 /usr/share/elasticsearch/plugins/bigdesk
chmod 755 /usr/share/elasticsearch/plugins/head
chmod 755 /usr/share/elasticsearch/plugins/kopf
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
CONF_FILE=/etc/elasticsearch/elasticsearch.yml
ES_HEAP_SIZE=8g
ES_HEAP_NEWSIZE=1g
ES_JAVA_OPTS="\$JAVA_OPTS -XX:+UseCondCardMark -XX:CMSWaitDuration=250 -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly"
ES_USER=root
EOF
echo 'set es'
