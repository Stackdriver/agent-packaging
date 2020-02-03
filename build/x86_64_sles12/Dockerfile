FROM opensuse/leap:42.3

RUN zypper addrepo https://download.opensuse.org/repositories/Apache/SLE_12_SP4/Apache.repo \
 # Add SLES 15 repo to install libhiredis0_13 from hiredis-devel
 && zypper addrepo https://download.opensuse.org/repositories/server:database/SLE_15/server:database.repo \
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
        hiredis-devel \
        pkg-config \
        python-devel \
        rpm-build \
        wget \
        which \
 && wget https://ftp.gwdg.de/pub/opensuse/repositories/home:/Herbster0815/openSUSE_Leap_15.1/noarch/automake-1.16.1-lp151.93.1.noarch.rpm \
 && rpm --force -Uvh automake-1.16.1-lp151.93.1.noarch.rpm \
 && rm automake-1.16.1-lp151.93.1.noarch.rpm \
 # Pretend we are on SLES 12.
 && /bin/sed -i -e 's/VERSION = 42.3/VERSION = 12/' /etc/SuSE-release \
 && /bin/sed -i -e 's/VERSION="42.3"/VERSION="12-SP3"/' -e 's/VERSION_ID="42.3"/VERSION_ID="12.3"/' /etc/os-release \
 && zypper -n clean
