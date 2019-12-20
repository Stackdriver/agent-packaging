FROM centos:7

RUN yum -y update \
 && yum -y install epel-release \
 && yum -y install \
        autoconf \
        automake \
        bison \
        expect \
        flex \
        gcc \
        git \
        hiredis-devel \
        java-devel \
        java-1.7.0-openjdk-devel \
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
        python-devel \
        rpm-build \
        rpm-sign \
        which \
        yajl-devel \
 && yum -y clean all
