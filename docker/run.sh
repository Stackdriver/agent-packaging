#!/bin/bash

configuration_file="/opt/stackdriver/collectd/etc/collectd.conf"
container_id=$(cat /proc/self/cgroup | grep -o  -e "docker/.*" | head -n 1 | sed "s/docker\/\(.*\)/\\1/")

if [[ ! -z "$NODE_NAME" ]]; then
    sed -i "s/%METADATA_AGENT_URL%/$NODE_NAME/" "$configuration_file"
else
    sed -i "s/%METADATA_AGENT_URL%/metadata-agent/" "$configuration_file"
fi

monitored_resource=""

if [[ ! -z "$POD_NAMESPACE"  &&  ! -z "$POD_NAME"  &&  ! -z "$MONITORED_CONTAINER_NAME" ]]; then
    monitored_resource="gke_containerName.$POD_NAMESPACE.$POD_NAME.$MONITORED_CONTAINER_NAME"

elif [[ ! -z "$container_id" ]]; then
    monitored_resource="container.$container_id"

elif [[ -e /var/run/docker.sock ]]; then
    monitored_resource=$(curl --silent -f -H 'Metadata-Flavor: Google' http://169.254.169.254/computeMetadata/v1/instance/id 2>/dev/null)
fi

if [[ -z "$monitored_resource" ]]; then
    echo "Failed to determine the monitored resource."
    exit 1
fi

sed -i "s/%HOSTNAME%/$monitored_resource/" "$configuration_file"

mount -a && \
    cp -r /etc/* /host/etc/ && \
    chroot /host /opt/stackdriver/collectd/sbin/stackdriver-collectd -f -C "$configuration_file"
