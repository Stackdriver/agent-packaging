#!/bin/bash
if [[ "${PKGFORMAT-}" != "deb" && "${PKGFORMAT-}" != "rpm" ]]; then
  echo >&2 "This script requires PKGFORMAT to be either 'deb' or 'rpm'"
  exit 1
fi
set -x
cp collectd.conf VERSION "${PKGFORMAT}"
