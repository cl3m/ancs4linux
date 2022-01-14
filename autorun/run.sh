#!/bin/bash
set -eu
set -x

if [ "$(whoami)" != "root" ]; then
    echo "Run this as root!"
    exit 1
fi

address=$(ancs4linux-ctl get-all-hci | jq -r '.[0]')
ancs4linux-ctl enable-advertising --hci-address $address --name PiZero
/usr/local/bin/ancs4linux-unicorn