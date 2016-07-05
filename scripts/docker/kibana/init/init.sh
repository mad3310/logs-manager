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

#uncompress kibana file
if [ ! -d "/opt/kibana" ]; then
cd /tmp
tar -xvzf kibana-4.0.2-linux-x64.tar.gz
mv kibana-4.0.2-linux-x64 /opt/kibana
echo 'uncompress kibana file'
fi
