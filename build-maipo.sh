#!/usr/bin/bash
set -xeuo pipefail
srcdir=$(cd $(dirname $0) && pwd)
rm fs-maipo{,.tmp} -rf
cp -a --reflink=auto fs-base fs-maipo.tmp
cd fs-maipo.tmp

# create os-release
cat << EOF >> usr/lib/os-release
NAME="Red Hat CoreOS (Maipo)"
VERSION_ID="47"
EOF

# let systemd handle core dumps on maipo
# https://bugzilla.redhat.com/show_bug.cgi?id=1191045
mkdir -p usr/lib/sysctl.d/
install -m 0644 ${srcdir}/49-coredump.conf usr/lib/sysctl.d/

cd ..
mv fs-maipo{.tmp,}
