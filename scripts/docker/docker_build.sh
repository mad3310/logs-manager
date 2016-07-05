#!/bin/bash
BUILE_LOG=build.log

VERSION=`grep 'version:' ../rpm/build_rpm.yml |sed 's/version: //g'`
RELEASE=`grep 'release:' ../rpm/build_rpm.yml |sed 's/release: //g'`

FINALE_VERSION=${VERSION}'-'${RELEASE}

echo ' -------------------start import letv-centos6 images----------------------' > ${BUILE_LOG}
docker import http://pkg-repo.oss.letv.com/pkgs/centos6/images/letv-centos6.tar letv:centos6 >> ${BUILE_LOG}
echo ' -------------------finish import letv-centos6 images----------------------' >> ${BUILE_LOG}

echo ' -------------------start building elasticsearch images----------------------' >> ${BUILE_LOG}
/usr/bin/docker build -t="dockerapp.et.letv.com/mcluster/elasticsearch:${FINALE_VERSION}" es/ >> ${BUILE_LOG}
echo ' -------------------finish building elasticsearch images----------------------' >> ${BUILE_LOG}

echo ' -------------------start building logstash images----------------------' >> ${BUILE_LOG}
/usr/bin/docker build -t="dockerapp.et.letv.com/mcluster/logstash:${FINALE_VERSION}" logstash/ >> ${BUILE_LOG}
echo ' -------------------finish building logstash images----------------------' >> ${BUILE_LOG}

echo ' -------------------start building kibana images----------------------' >> ${BUILE_LOG}
/usr/bin/docker build -t="dockerapp.et.letv.com/mcluster/kibana:${FINALE_VERSION}" kibana/ >> ${BUILE_LOG}
echo ' -------------------finish building kibana images----------------------' >> ${BUILE_LOG}


echo ' -------------------start push elasticsearch images----------------------' >> ${BUILE_LOG}
/usr/bin/docker push dockerapp.et.letv.com/mcluster/elasticsearch:${FINALE_VERSION}  >> ${BUILE_LOG}
echo ' -------------------finish push elasticsearch images----------------------' >> ${BUILE_LOG}

echo ' -------------------start push logstash images----------------------' >> ${BUILE_LOG}
/usr/bin/docker push dockerapp.et.letv.com/mcluster/logstash:${FINALE_VERSION}  >> ${BUILE_LOG}
echo ' -------------------finish push logstash images----------------------' >> ${BUILE_LOG}

echo ' -------------------start push kibana images----------------------' >> ${BUILE_LOG}
/usr/bin/docker push dockerapp.et.letv.com/mcluster/kibana:${FINALE_VERSION}  >> ${BUILE_LOG}
echo ' -------------------finish push kibana images----------------------' >> ${BUILE_LOG}
