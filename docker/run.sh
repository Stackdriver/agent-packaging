#!/bin/bash

configuration_file="/opt/stackdriver/collectd/etc/collectd.conf"

# It is OK if the container_id is empty, the monitoring agent will attempt to fill it.
container_id=$(cat /proc/self/cgroup | grep -o  -e "docker/.*" | head -n 1 | sed "s/docker\/\(.*\)/\\1/")

sed -i "s/%CONTAINER_ID%/$container_id/" "$configuration_file"

# If the metadata agent hostname is not provided, we will assume a link by the name of metadata-agent.
METADATA_AGENT_HOSTNAME="${METADATA_AGENT_HOSTNAME:-metadata-agent}"

sed -i "s/%METADATA_AGENT_HOSTNAME%/$METADATA_AGENT_HOSTNAME/" "$configuration_file"

# Determine the monitored resource based or use empty and let the monitoring agent figure it out.
monitored_resource=""

if [[ ! -z "$POD_NAMESPACE"  &&  ! -z "$POD_NAME"  &&  ! -z "$MONITORED_CONTAINER_NAME" ]]; then
    monitored_resource="gke_containerName.$POD_NAMESPACE.$POD_NAME.$MONITORED_CONTAINER_NAME"

elif [[ "$LOOKUP_GCE_INSTANCE_ID" == "true" ]]; then
    monitored_resource=$(curl --silent -f -H 'Metadata-Flavor: Google' http://169.254.169.254/computeMetadata/v1/instance/id 2>/dev/null)

elif [[ ! -z "$MONITORED_CONTAINER_NAME" ]]; then
    monitored_resource="containerName.$MONITORED_CONTAINER_NAME"

fi

sed -i "s/%MONITORED_RESOURCE%/$monitored_resource/" "$configuration_file"

mount -a && \
    cp -r /etc/* /host/etc/ && \
    chroot /host /opt/stackdriver/collectd/sbin/stackdriver-collectd -f -C "$configuration_file"
