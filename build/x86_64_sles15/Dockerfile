FROM opensuse/leap:15.1

RUN zypper addrepo https://ftp.lysator.liu.se/pub/opensuse/repositories/devel:/libraries:/c_c++/openSUSE_Leap_15.1/devel:libraries:c_c++.repo \
 # The lysator.liu.se mirror still references download.opensuse.org.
 && sed -i 's@download.opensuse.org@ftp.lysator.liu.se/pub/opensuse@' /etc/zypp/repos.d/devel_libraries_c_c++.repo \
 # Add Herbster0815 repo to install the latest automake.
 && zypper addrepo https://download.opensuse.org/pub/opensuse/repositories/home:/Herbster0815/openSUSE_Leap_15.5/home:Herbster0815.repo \
 && zypper -n --gpg-auto-import-keys refresh \
 && zypper -n install --allow-vendor-change \
        autoconf \
        automake \
        bison \
        expect \
        flex \
        gcc \
        git \
        hiredis-devel \
        java-1_8_0-openjdk-devel \
        libcurl4 \
        libcurl-devel \
        libgcrypt20 \
        libgcrypt-devel \
        libtool \
        libtool-ltdl-devel \
        libyajl2 \
        libyajl-devel \
        libmysqlclient-devel \
        make \
        openssl-devel \
        pkg-config \
        postgresql-devel \
        python2-devel \
        python3-devel \
        rpm-build \
        varnish-devel \
        which \
 # Pretend we are on SLES 15.
 && /bin/sed -i -e 's/VERSION="15.1"/VERSION="15-SP1"/' /etc/os-release \
 && zypper -n clean
