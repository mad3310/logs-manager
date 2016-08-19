#!/bin/bash

chmod +x /etc/init.d/logs-manager
chkconfig --add logs-manager
cd /opt/letv/logs-manager/packages && unzip psutil-4.3.0.zip && cd psutil-4.3.0 && python setup.py install && cd -
/etc/init.d/logs-manager start | stop | restart

exit 0
