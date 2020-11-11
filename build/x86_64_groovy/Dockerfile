FROM ubuntu:groovy

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update \
 && apt-get -y install \
        autoconf \
        automake \
        bison \
        debhelper \
        debian-keyring \
        default-jdk \
        devscripts \
        flex \
        gcc \
        git \
        libcurl4-openssl-dev \
        libhiredis-dev \
        libltdl-dev \
        libmysqlclient-dev \
        libssl-dev \
        libtool \
        libyajl-dev \
        lsb-release \
        make \
        pkg-config \
        python-dev-is-python2 \
 && curl -sSO http://security.ubuntu.com/ubuntu/pool/main/c/coreutils/coreutils_8.30-3ubuntu2_amd64.deb \
 && dpkg -i coreutils_8.30-3ubuntu2_amd64.deb \
 && apt-get install -f \
 && apt-get -y clean \
 && rm -rf /var/lib/apt/lists/*
