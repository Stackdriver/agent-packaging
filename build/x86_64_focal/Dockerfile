FROM ubuntu:focal

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
        python2-dev \
        python3-dev \
 && apt-get -y clean \
 && rm -rf /var/lib/apt/lists/*
