#!/bin/bash

set -e
set -o pipefail

docker build -f Dockerfile.base -t amzn-2014.03-build .
docker run amzn-2014.03-build | docker import - amazonlinux:2014.03
