FROM opensuse/leap:15.1

RUN zypper addrepo https://download.opensuse.org/repositories/devel:/libraries:/c_c++/openSUSE_Leap_15.1/devel:libraries:c_c++.repo \
 && zypper -n --gpg-auto-import-keys refresh \
 && zypper -n install \
        autoconf \
        automake \
        bison \
        expect \
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
 && wget ftp://ftp.pbone.net/mirror/ftp.gwdg.de/pub/opensuse/repositories/home:/Herbster0815/openSUSE_Leap_15.1/noarch/automake-1.16.1-lp151.92.1.noarch.rpm \
 && rpm --force -Uvh automake-1.16.1-lp151.92.1.noarch.rpm \
 && rm automake-1.16.1-lp151.92.1.noarch.rpm \
 && /bin/sed -i -e 's/VERSION="15.1"/VERSION="15-SP1"/' /etc/os-release \
 && zypper -n clean
