FROM centos:8

RUN yum -y update \
 && dnf -y install 'dnf-command(config-manager)' \
 && yum config-manager --set-enabled PowerTools \
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
