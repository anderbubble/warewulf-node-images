#!/bin/sh
set -x
LANG=C
LC_CTYPE=C
export LANG LC_CTYPE
dnf clean all
rm -f /var/lib/dbus/machine-id
truncate -s0 /etc/machine-id
