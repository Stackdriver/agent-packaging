FROM registry.access.redhat.com/ubi8/ubi:latest

ADD https://www.centos.org/keys/RPM-GPG-KEY-CentOS-Official /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-Official
ADD https://rpms.remirepo.net/RPM-GPG-KEY-remi2018 /etc/pki/rpm-gpg/RPM-GPG-KEY-remi.el8
COPY centos8.repo remi.repo /etc/yum.repos.d/

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
 && yum -y clean all
