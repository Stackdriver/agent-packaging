FROM amazonlinux:2016.09

RUN yum update -y && yum install -y \
	autoconf \
	automake \
	bison \
	epel-release \
	flex \
	gcc \
	git \
	java-devel \
	java-1.6.0-openjdk-devel \
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
	libgcrypt-devel \
	perl-ExtUtils-Embed \
	varnish-libs-devel

ADD http://ftp.tu-chemnitz.de/pub/linux/dag/redhat/el6/en/x86_64/rpmforge/RPMS/rpm-macros-rpmforge-0-6.el6.rf.noarch.rpm .

RUN rpm -Uvh rpm-macros-rpmforge*.rpm \
	&& yum install rpm-macros-rpmforge \
	&& yum -y clean all

RUN sed -i 's/el6/amzn1/' /etc/rpm/macros.rpmforge
