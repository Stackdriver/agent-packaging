FROM centos:6

RUN yum update -y && yum install -y \
	automake \
	bison \
	epel-release \
	expect \
	flex \
	gcc \
	git \
	java-devel \
	java-1.6.0-openjdk-devel \
	libcurl-devel \
	libtool \
	make \
	mysql-devel \
	openssl-devel \
	perl-devel \
	postgresql-devel \
	python-devel \
	rpm-build \
	which \
	yajl-devel

RUN yum install -y \
	libgcrypt-devel \
	perl-ExtUtils-Embed \
	varnish-libs-devel \
     && yum -y clean all
