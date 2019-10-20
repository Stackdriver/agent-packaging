#!/bin/bash
if [[ "${PKGFORMAT-}" != "deb" && "${PKGFORMAT-}" != "rpm" ]]; then
  echo >&2 "This script requires PKGFORMAT to be either 'deb' or 'rpm'"
  exit 1
fi
cp -p collectd.conf "${PKGFORMAT}"
cp -p stack-config "${PKGFORMAT}"
