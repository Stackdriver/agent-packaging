From us.gcr.io/stackdriver-test-143416/stackdriver-agent-test-container-x86_64_centos8-base:latest
Run yum -y install redis; \
curl -LO http://rpms.famillecollet.com/enterprise/remi-release-8.rpm; \ 
yum -y install remi-release-8.rpm; \
yum -y install hiredis;
 
CMD ["/usr/sbin/init"]

