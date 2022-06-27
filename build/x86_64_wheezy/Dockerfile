FROM debian:wheezy

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
 # Needed for autoconf, due to broken Debian 7 repos.
 && apt-get -y -o Apt::Get::force-yes=1 install perl-base=5.14.2-21+deb7u3 \
 # Needed for g++, due to broken Debian 7 repos.
 && apt-get download libc-bin=2.13-38+deb7u10 \
 && dpkg -i libc-bin_2.13-38+deb7u10_amd64.deb \
 && apt-get download libc6=2.13-38+deb7u10 \
 && dpkg -i libc6_2.13-38+deb7u10_amd64.deb \
 && apt-get -y install linux-libc-dev \
 # Needed for libcurl4-openssl-dev and libpq-dev, due to broken Debian 7 repos.
 && apt-get download libssl1.0.0=1.0.1e-2+deb7u20 \
 && dpkg -i libssl1.0.0_1.0.1e-2+deb7u20_amd64.deb \
 # Needed for default-jdk, due to broken Debian 7 repos.
 && apt-get download tzdata=2016d-0+deb7u1 \
 && dpkg -i tzdata_2016d-0+deb7u1_all.deb \
 # Clean up all the downloaded packages.
 && rm -f *.deb \
 # Now install the necessary packages.
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
