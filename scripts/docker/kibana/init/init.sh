#!/bin/bash

echo 'do init action'
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

#set monit
cat >  /etc/monitrc  << EOF
set daemon 30
set logfile /var/log/monit.log
set pidfile /var/run/monit.pid
set httpd port 30000
allow 127.0.0.1

check process kibana with pidfile /var/run/kibana.pid
    start program = "/etc/init.d/kibana start"
    stop  program = "/etc/init.d/kibana stop"    
EOF
/etc/init.d/monit start
echo 'set monit successfully'

#set logrotate
cat > /etc/logrotate.d/kibana << EOF
/var/log/kibana/kibana.log
{
daily
dateext
dateformat -%Y%m%d-%s
nocompress
size 10M
missingok
notifempty
copytruncate
rotate 3
postrotate
endscript
}
EOF

cat > /etc/logrotate.d/monit << EOF
/var/log/monit.log
{
daily
dateext
dateformat -%Y%m%d-%s
nocompress
size 10M
missingok
notifempty
copytruncate
rotate 3
postrotate
endscript
}
EOF

is_logrotate=`grep -c "logrotate" /etc/crontab`
if [ ${is_logrotate} -eq 0 ]
then
echo '0 * * * * root /usr/sbin/logrotate /etc/logrotate.conf >/dev/null 2>&1' >> /etc/crontab
fi

service crond restart
echo 'set logrotate successfully'
