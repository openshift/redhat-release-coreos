#!/usr/bin/bash
set -xeuo pipefail
srcdir=$(cd $(dirname $0) && pwd)
rm fs-ootpa{,.tmp} -rf
cp -a --reflink=auto fs-base fs-ootpa.tmp
cd fs-ootpa.tmp

# create os-release
cat << EOF >> usr/lib/os-release
NAME="Red Hat CoreOS (Ootpa)"
VERSION_ID="48"
EOF

cd ..
mv fs-ootpa{.tmp,}
