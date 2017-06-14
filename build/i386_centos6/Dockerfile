FROM toopher/centos-i386:centos6

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
	epel-release

RUN yum update -y \
	&& yum install -y mock \
	&& yum -y clean all
