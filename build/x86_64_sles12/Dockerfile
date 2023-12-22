FROM opensuse/leap:42.3 AS mongo-c-driver-build

# Build and install mongo-c-driver packages.
RUN zypper -n install tar gzip make gcc gcc-c++ libopenssl-devel rpm-build #cyrus-sasl-devel

ARG CMAKE_VERSION=3.28.1
ADD https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-linux-x86_64.sh \
    /cmake.sh
RUN set -xe; \
    (echo "ada6a46be9da5f8cbeb00b9523ffe45ee6b36172eb81aaa5bdc6a2a8231b677c  /cmake.sh" | sha256sum -c); \
    bash /cmake.sh --skip-license --prefix=/usr/local

ARG VERSION=1.12.0
ADD https://github.com/mongodb/mongo-c-driver/archive/refs/tags/${VERSION}.tar.gz /src/mongo-c-driver-${VERSION}.tar.gz
RUN tar -xzf /src/mongo-c-driver-${VERSION}.tar.gz -C /src
ADD https://raw.githubusercontent.com/mongodb/mongo-c-driver/1.18.0/.evergreen/mongo-c-driver.spec /src/mongo-c-driver.spec
WORKDIR /src
RUN sed -i \
        -e '/BuildRequires: [cp\/]/d' \
        -e '/ENABLE_CLIENT_SIDE_ENCRYPTION/d' -e '/(mongocrypt)/d' \
        -e '/ENABLE_MAN_PAGES/d' -e '/%{_mandir}/d' \
        -e '/%{_libdir}\/cmake\/bson-/d' \
        -e '/%{_libdir}\/cmake\/mongoc-/d' \
        -e '/ENABLE_SASL/d' \
        -e '/ENABLE_ICU/d' \
        -e '/cmake-filesystem/d' \
        -e '/-S \./s/^/    -DCMAKE_INSTALL_PREFIX:STRING="%{_prefix}"/' \
        -e '/^%global up_version/s/[0-9.]\+$/'"${VERSION}"'/' mongo-c-driver.spec \
 && rpmbuild \
        --define "_topdir /" \
        --define "_source_filedigest_algorithm md5" \
        --define "_sourcedir ${PWD}" \
        --define "_srcrpmdir ${PWD}" \
        --define "package_version ${VERSION}" \
        --define "build_num 1" \
        --define "cmake /usr/local/bin/cmake" \
        -ba mongo-c-driver.spec \
 && mkdir -p /rpms \
 && mv /RPMS/*/*.rpm /rpms

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
COPY --from=mongo-c-driver-build /rpms /tmp/mongo-c-rpms
RUN zypper -n --no-gpg-checks install /tmp/mongo-c-rpms/*.rpm
