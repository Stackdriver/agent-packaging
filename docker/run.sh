configuration_file="/opt/stackdriver/collectd/etc/collectd.conf"

if [ -f /usr/src/collectd/collectd.conf ]; then
    configuration_file="/usr/src/collectd/collectd.conf"
fi

echo "Using configuration file: $configuration_file.";

mount -a && \
    cp /etc/hosts /host/etc/hosts && \
    cp /etc/resolv.conf /host/etc/resolv.conf && \
    chroot /host /opt/stackdriver/collectd/sbin/stackdriver-collectd -f -C "$configuration_file"