FROM centos:8

# CentOS 8 is EOL, so we have to switch to the vault repos.
RUN sed -i \
        -e 's%^mirrorlist%#mirrorlist%' \
        -e 's%^# *baseurl=http://mirror%baseurl=http://vault%' \
        /etc/yum.repos.d/CentOS-*.repo

RUN dnf -y install 'dnf-command(config-manager)' \
 && yum config-manager --set-enabled powertools \
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
