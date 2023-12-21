FROM opensuse/leap:42.3

# Remove expired root certificate.
RUN mv /var/lib/ca-certificates/pem/DST_Root_CA_X3.pem /etc/pki/trust/blacklist/ \
 && update-ca-certificates

RUN true \
 # The 'OSS Update' repo signature is no longer valid, so verify the checksum instead.
 && zypper --no-gpg-check refresh 'OSS Update' \
 && (echo 'b889b4bba03074cd66ef9c0184768f4816d4ccb1fa9ec2721c5583304c5f23d0  /var/cache/zypp/raw/OSS Update/repodata/repomd.xml' | sha256sum --check) \
 # Add Herbster0815 repo to install the latest automake.
 && zypper addrepo https://download.opensuse.org/pub/opensuse/repositories/home:/Herbster0815/openSUSE_Leap_15.6/home:Herbster0815.repo \
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
        pkg-config \
        postgresql-devel \
        python2-devel \
        python3-devel \
        rpm-build \
        varnish-devel \
        which \
 # Use the SLES 15 repo to install libhiredis0_13 from hiredis-devel.
 && zypper -n -p https://download.opensuse.org/distribution/leap/15.3/repo/oss/ install hiredis-devel \
 # Pretend we are on SLES 12.
 && /bin/sed -i -e 's/VERSION = 42.3/VERSION = 12/' /etc/SuSE-release \
 && /bin/sed -i -e 's/VERSION="42.3"/VERSION="12-SP3"/' -e 's/VERSION_ID="42.3"/VERSION_ID="12.3"/' /etc/os-release \
 && zypper -n clean
