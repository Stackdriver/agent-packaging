FROM debian:stretch

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
        libpq-dev \
        libpq5 \
        libssl1.0-dev \
        libtool \
        libvarnishapi-dev \
        libyajl-dev \
        make \
        pkg-config \
        python-dev \
        python3-dev \
 && apt-get -y clean \
 && rm -rf /var/lib/apt/lists/*
