#!/bin/bash

chmod +x /etc/init.d/logs-manager
chkconfig --add logs-manager
/etc/init.d/logs-manager start | stop | restart

exit 0
