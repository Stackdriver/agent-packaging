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
        java-1_8_0-openjdk \
        glibc-devel \
        linux-glibc-devel \
        pkg-config \
        libcurl4-7.66.0-lp151.270.1.x86_64 \
	libcurl-devel \
	libgcrypt20-1.8.5-lp151.161.1.x86_64 \
	libgcrypt-devel \
        libtool \
        libyajl2 \
        libyajl-devel \
        libmysqlclient-devel \
        make \
        openssl \
        postgresql-devel \
        hiredis-devel \
        pkg-config \
        python-devel \
        rpm-build \
        varnish-devel \
        wget \
        which \
 && wget https://ftp.gwdg.de/pub/opensuse/repositories/home%3A/Herbster0815/openSUSE_Leap_15.1/noarch/automake-1.16.1-lp151.92.1.noarch.rpm \
 && rpm --force -Uvh automake-1.16.1-lp151.92.1.noarch.rpm \
 && rm automake-1.16.1-lp151.92.1.noarch.rpm \
 && /bin/sed -i -e 's/VERSION="15.1"/VERSION="15-SP1"/' /etc/os-release \
 && zypper -n clean
