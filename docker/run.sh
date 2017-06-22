#!/bin/bash

configuration_file="/opt/stackdriver/collectd/etc/collectd.conf"

if [[ ! -z "$NODE_NAME" ]]; then
    sed -i "s/%METADATA_AGENT_URL%/$NODE_NAME/" "$configuration_file"
else
    sed -i "s/%METADATA_AGENT_URL%/metadata-agent/" "$configuration_file"
fi

if [[ ! -z "$POD_NAMESPACE"  &&  ! -z "$POD_NAME"  &&  ! -z "$MONITORED_CONTAINER_NAME" ]]; then
    sed -i "s/%HOSTNAME%/gke_container.$POD_NAMESPACE.$POD_NAME.$MONITORED_CONTAINER_NAME/" "$configuration_file"

elif [[ -e /var/run/docker.sock ]]; then
    iid=$(curl --silent -f -H 'Metadata-Flavor: Google' http://169.254.169.254/computeMetadata/v1/instance/id 2>/dev/null)

    sed -i "s/%HOSTNAME%/$iid/" "$configuration_file"

else
    echo "Failed to determine the monitored resource."
    exit 1

fi

mount -a && \
    cp /etc/hosts /host/etc/hosts && \
    cp /etc/resolv.conf /host/etc/resolv.conf && \
    chroot /host /opt/stackdriver/collectd/sbin/stackdriver-collectd -f -C "$configuration_file"