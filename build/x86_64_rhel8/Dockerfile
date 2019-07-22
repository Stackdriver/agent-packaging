FROM registry.access.redhat.com/ubi8/ubi:latest

RUN yum -y update \
 && dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm \
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
        java-1.8.0-openjdk-devel \
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
        python36-devel \
        rpm-build \
        rpm-sign \
        varnish-libs-devel \
        which \
        yajl-devel \
 && yum -y install \
        mongo-c-driver-devel \
        cyrus-sasl-devel \
 && yum -y clean all
