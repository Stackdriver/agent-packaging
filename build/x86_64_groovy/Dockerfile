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
        libmongoc-dev \
        libmysqlclient-dev \
        libpq-dev \
        libssl-dev \
        libtool \
        libvarnishapi-dev \
        libyajl-dev \
        lsb-release \
        make \
        pkg-config \
        python-dev-is-python2 \
        python3-dev \
 # Work around https://gitlab.archlinux.org/archlinux/archlinux-docker/-/issues/32.
 && echo 'deb http://archive.ubuntu.com/ubuntu/ focal main' >/etc/apt/sources.list.d/focal.list \
 && apt-get -y update \
 && apt-get -y install --allow-downgrades coreutils=8.30-3ubuntu2 \
 && apt-get -y clean \
 && rm -rf /var/lib/apt/lists/*
