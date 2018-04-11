FROM debian:wheezy

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get install -y \
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
        libpq-dev \
        libtool \
        libvarnishapi-dev \
        libyajl-dev \
        make \
        pkg-config \
        python-dev \
  && rm -rf /var/lib/apt/lists/*
