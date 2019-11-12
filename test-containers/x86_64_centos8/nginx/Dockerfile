From us.gcr.io/stackdriver-test-143416/stackdriver-agent-test-container-x86_64_centos8-base:latest
Run yum -y install nginx;\
(cd /etc/nginx/conf.d/ && curl -O https://raw.githubusercontent.com/Stackdriver/stackdriver-agent-service-configs/master/etc/nginx/conf.d/status.conf);
 
EXPOSE 80
CMD ["/usr/sbin/init"]

