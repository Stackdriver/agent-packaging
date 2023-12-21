FROM debian:stretch

RUN \
 # Point to the archive...
    sed -i \
      -e 's/\(deb\|httpredir\)\.debian\.org/archive.debian.org/g' \
      -e 's/security\.debian\.org/archive.debian.org/g' \
      -e '/-updates main/d' \
      -e '/http\.debian\.net/d' \
      /etc/apt/sources.list

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
