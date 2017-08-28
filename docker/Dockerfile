FROM ubuntu:xenial

ENV RUNLEVEL=1
RUN sed -i 's/101/0/' /usr/sbin/policy-rc.d

ARG version=5.5.2-364+docker1
ADD https://storage.googleapis.com/stackdriver-container-alpha/deb/xenial/stackdriver-agent_$version.xenial_amd64.deb /stackdriver-agent_$version.xenial_amd64.deb

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y \
        curl \
        default-jdk \
        default-jre \
        libcurl3 \
        libhiredis0.13 \
        libltdl7 \
        libmysqlclient20 \
        libpq5 \
        libvarnishapi1 \
        libyajl2 \
    && (dpkg -i /stackdriver-agent_$version.xenial_amd64.deb || true) \
    # We are temporarily ignoring the error due to builds happening outside of 
    # a GCP VM that don't have access to the metadata server.
    && (apt-get install -f -y || true) \
    && rm -rf /var/lib/apt/lists/*

# Allow user specified configuration files.
VOLUME ["/etc/collectd/collectd.d/"]

ADD collectd.conf /etc/collectd/collectd.conf
ADD run.sh /run.sh

# Populate dynamic values in the configuration and run the collectd process.
CMD /run.sh