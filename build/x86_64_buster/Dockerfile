FROM debian:buster

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update \
 && apt-get -y install \
        autoconf \
        automake \
        bison \
        debhelper \
        debian-keyring \
        default-jdk \
        default-libmysqlclient-dev \
        devscripts \
        flex \
        gcc \
        git \
        libcurl4-openssl-dev \
        libhiredis-dev \
        libltdl-dev \
        libssl-dev \
        libtool \
        libyajl-dev \
        make \
        pkg-config \
        python-dev \
 && apt-get -y clean \
 && rm -rf /var/lib/apt/lists/*
