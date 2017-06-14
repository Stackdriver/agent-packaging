FROM centos:6

RUN yum update -y && yum install -y \
	git \
	flex \
	bison \
	gcc \
	automake \
	libtool \
	libgcrypt-dev \
	make \
	rpm-build \
	rpm-sign \
	dejavu-sans-fonts \
	libcurl-devel \
	openssl-devel \
	epel-release \

RUN yum update -y \
	&& yum install -y mock \
	&& yum -y clean all

COPY amzn-2014.03-x86_64.cfg  /etc/mock/amzn-2014.03-x86_64.cfg
COPY amzn-2015.03-x86_64.cfg  /etc/mock/amzn-2015.03-x86_64.cfg
