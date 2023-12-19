FROM ubuntu:eoan

# Ubuntu Eoan is EOL, so we have to switch to the archive repos.
RUN sed -i \
        -e 's%^deb http://\(archive\|security\)\.%deb http://old-releases.%' \
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
        python-dev \
        python3-dev \
 && apt-get -y clean \
 && rm -rf /var/lib/apt/lists/*
