FROM amazonlinux:2016.09

ADD https://rpmfind.net/linux/dag/redhat/el6/en/x86_64/dag/RPMS/rpm-macros-rpmforge-0-6.el6.rf.noarch.rpm .
RUN yum -y install epel-release \
 && yum -y install \
        autoconf \
        automake \
        bison \
        ca-certificates \
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
        pkgconfig \
        postgresql-devel \
        python2-devel \
        python36-devel \
        rpm-build \
        rpm-sign \
        varnish-libs-devel \
        which \
        yajl-devel \
 && rpm -Uvh rpm-macros-rpmforge*.rpm \
 && yum install rpm-macros-rpmforge \
 && sed -i 's/el6/amzn1/' /etc/rpm/macros.rpmforge \
 && rm /rpm-macros-rpmforge-0-6.el6.rf.noarch.rpm \
 && yum -y clean all
