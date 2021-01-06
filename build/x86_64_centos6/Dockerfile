FROM centos:6

# CentOS 6 is EOL, so we have to switch to the vault repos.
RUN sed -i \
        -e 's%^mirrorlist%#mirrorlist%' \
        -e 's%^# *baseurl=http://mirror%baseurl=http://vault%' \
        /etc/yum.repos.d/CentOS-*.repo

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
        java-devel \
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
        postgresql-devel \
        python-devel \
        rpm-build \
        varnish-libs-devel \
        which \
        yajl-devel \
 && yum -y clean all
