FROM debian:jessie

RUN \
 # Point to the archive...
    sed -i \
      -e 's/\(deb\|httpredir\)\.debian\.org/archive.debian.org/g' \
      -e '/-updates main/d' \
      -e '/http\.debian\.net/d' \
      /etc/apt/sources.list \
 # ...and disable the expiration check...
 && echo 'Acquire::Check-Valid-Until "0";' \
      >/etc/apt/apt.conf.d/10no-check-valid-until \
 # ...and remove pointers to the defunct security repos.
 && sed -i \
      -e '/security\.debian\.org/d' \
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
 && apt-get -y clean \
 && rm -rf /var/lib/apt/lists/*
