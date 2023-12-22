FROM opensuse/leap:15.1 AS mongo-c-driver-build

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

FROM opensuse/leap:15.1

RUN true \
 && zypper addrepo https://ftp.lysator.liu.se/pub/opensuse/repositories/devel:/libraries:/c_c++/openSUSE_Leap_15.1/devel:libraries:c_c++.repo \
 # The lysator.liu.se mirror still references download.opensuse.org.
 && sed -i 's@download.opensuse.org@ftp.lysator.liu.se/pub/opensuse@' /etc/zypp/repos.d/devel_libraries_c_c++.repo \
 # Add Herbster0815 repo to install the latest automake.
 && zypper addrepo https://download.opensuse.org/pub/opensuse/repositories/home:/Herbster0815/openSUSE_Leap_15.6/home:Herbster0815.repo \
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
COPY --from=mongo-c-driver-build /rpms /tmp/mongo-c-rpms
RUN zypper -n --no-gpg-checks install /tmp/mongo-c-rpms/*.rpm
