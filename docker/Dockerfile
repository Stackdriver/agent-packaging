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

ADD . /collectd

# Mount everything under /host in order to volume the host's proc into the 
# container.
RUN mkdir -p /host/bin /host/dev /host/etc /host/etc/ssl /host/lib /host/lib64 /host/opt /host/usr/bin /host/usr/lib /host/var/lib \
    && cp /collectd/collectd.conf /opt/stackdriver/collectd/etc/collectd.conf \
    && cp /collectd/fstab /etc/fstab

# Mount the chroot dependencies and run collectd in the foreground.
CMD /collectd/run.sh

# Allow user specified configuration files.
VOLUME ["/host/proc", "/host/usr/src/collectd"]
