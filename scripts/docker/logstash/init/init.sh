#!/bin/bash

echo 'do init action'
mkdir -p /var/log/logstash
chmod 777 /var/log/logstash

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

#set logrotate
cat > /etc/logrotate.d/monit << EOF
/var/log/monit.log
{
daily
dateext
dateformat -%Y%m%d-%s
nocompress
size 1M
missingok
notifempty
copytruncate
rotate 5
postrotate
endscript
}
EOF
echo 'set logrotate successfully'

# set monit
cat >  /etc/monitrc  << EOF
set daemon 30
set logfile /var/log/monit.log
set pidfile /var/run/monit.pid
set httpd port 30000
allow 127.0.0.1

check process salt_minion MATCHING 'logstash'
    start program = "/etc/init.d/logstash start"
    stop  program = "/etc/init.d/logstash stop"    
EOF

/etc/init.d/monit start

echo 'set monit successfully'

#set logstash
cat > /etc/sysconfig/logstash << EOF
LS_HEAP_SIZE="1500m"
LS_JAVA_OPTS="\$JAVA_OPTS -XX:+UseCondCardMark -XX:CMSWaitDuration=250 -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly"
LS_WORKER_THREADS=20
EOF
echo 'set logstash'
