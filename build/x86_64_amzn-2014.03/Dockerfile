FROM amazonlinux:2014.03

COPY os-release /etc/os-release
COPY system-release /etc/system-release
RUN yum -y update \
 && yum -y install \
        epel-release \
 && sed -i 's/enabled=0/enabled=1/' /etc/yum.repos.d/epel* \
 && yum -y install \
        autoconf \
        automake \
        bison \
        flex \
        gcc \
        git \
        java-1.6.0-openjdk-devel \
        libcurl-devel \
        libgcrypt-devel \
        libtool \
        libtool-ltdl-devel \
        make \
        mysql-devel \
        openssl-devel \
        perl-devel \
        perl-ExtUtils-Embed \
        pkgconfig \
        postgresql-devel \
        python-devel \
        rpm-build \
        rpm-sign \
        varnish-libs-devel \
        which \
        yajl-devel \
 && yum -y clean all
