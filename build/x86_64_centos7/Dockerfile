FROM centos:7

RUN yum update -y && yum install -y \
	autoconf \
	automake \
	bison \
	epel-release \
	expect \
	flex \
	gcc \
	git \
	java-devel \
	java-1.7.0-openjdk-devel \
	libcurl-devel \
	libtool \
	libtool-ltdl-devel \
	make \
	mysql-devel \
	openssl-devel \
	perl-devel \
	pkg-config \
	postgresql-devel \
	python-devel \
	rpm-build \
	rpm-sign \
	which \
	yajl-devel

RUN yum install -y \
	hiredis-devel \
	libgcrypt-devel \
	perl-ExtUtils-Embed \
	varnish-libs-devel \
     && yum -y clean all
