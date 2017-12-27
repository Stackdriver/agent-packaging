FROM amazonlinux:2016.09

RUN yum update -y && yum install -y \
	git \
	flex \
	bison \
	gcc \
	automake \
	autoconf \
	libtool \
	libtool-ltdl-devel \
	make \
	rpm-build \
	libcurl-devel \
	openssl-devel \
	epel-release \
	python-devel \
	mysql-devel \
	postgresql-devel \
	java-1.6.0-openjdk-devel \
	java-devel \
	yajl-devel \
	perl-devel \
	pkg-config \
	which

RUN yum install -y \
	libgcrypt-devel \
	varnish-libs-devel \
	perl-ExtUtils-Embed

ADD http://ftp.tu-chemnitz.de/pub/linux/dag/redhat/el6/en/x86_64/rpmforge/RPMS/rpm-macros-rpmforge-0-6.el6.rf.noarch.rpm .

RUN rpm -Uvh rpm-macros-rpmforge*.rpm \
	&& yum install rpm-macros-rpmforge \
	&& yum -y clean all

RUN sed -i 's/el6/amzn1/' /etc/rpm/macros.rpmforge
