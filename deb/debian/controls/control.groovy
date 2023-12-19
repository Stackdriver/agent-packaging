Source: stackdriver-agent
Maintainer: Stackdriver Agents <stackdriver-agents@google.com>
Section: misc
Priority: optional
Standards-Version: 3.9.2
Build-Depends: autoconf, automake, debhelper (>= 10), default-jdk, libcurl4-openssl-dev, libhiredis-dev (>= 0.14), libltdl-dev, libmysqlclient-dev, libpq-dev, libtool, libvarnishapi-dev, libyajl-dev, lsb-release, pkg-config

Package: stackdriver-agent
Architecture: any
Depends: ${shlibs:Depends}, ${misc:Depends}, libcurl4, libltdl7, libyajl2
Suggests: default-jre, libhiredis0.14, libmysqlclient21, libpq5
Description: Stackdriver system metrics collection daemon
  The Stackdriver system metrics daemon collects system statistics and
  sends them to the Stackdriver service.
  Currently includes collectd.
  
