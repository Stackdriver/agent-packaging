FROM opensuse:latest

RUN zypper addrepo https://download.opensuse.org/repositories/devel:libraries:c_c++/SLE_12_SP3/devel:libraries:c_c++.repo \
    && zypper --non-interactive --gpg-auto-import-keys refresh \
    && zypper install -y \
	autoconf \
	automake \
	bison \
	flex \
	gcc \
	git \
	java-1_7_0-openjdk-devel \
	libcurl-devel \
	libgcrypt-devel \
	libtool \
	libtool-ltdl-devel \
	libyajl2 \
	libyajl-devel \
	libmysqlclient-devel \
	make \
	openssl-devel \
	postgresql-devel \
	hiredis-devel \
	pkg-config \
	python-devel \
	rpm-build \
	varnish-devel \
	wget \
	which \
    && wget ftp://ftp.pbone.net/mirror/ftp5.gwdg.de/pub/opensuse/repositories/home:/Herbster0815/openSUSE_Factory/noarch/automake-1.14.1-56.1.noarch.rpm \
    && rpm --force -Uvh automake-1.14.1-56.1.noarch.rpm \
    && rm automake-1.14.1-56.1.noarch.rpm \
    && zypper clean
