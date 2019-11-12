From us.gcr.io/stackdriver-test-143416/stackdriver-agent-test-container-x86_64_centos8-base:latest
Run yum -y install httpd; yum clean all; systemctl enable httpd.service;\
 (cd /etc/httpd/conf.d/ && curl -O https://raw.githubusercontent.com/Stackdriver/stackdriver-agent-service-configs/master/etc/httpd/conf.d/status.conf);
EXPOSE 80
 
CMD ["/usr/sbin/init"]

