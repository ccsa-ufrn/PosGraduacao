#!/bin/bash
# CAUTION: only run this script once.
# It's a development script that installs standard collections
# using mongo shell.

if [ "$1" == "-i" ] || [ "$1" == "--install" ]; then
    mongo < ./i.js
else
    echo "ERROR: Use $0 with --install or --uninstall flags only."
fi
