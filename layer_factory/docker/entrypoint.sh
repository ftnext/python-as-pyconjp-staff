#!/usr/bin/env bash
set -eu
PACKAGES=$@

python3.8 -m pip install -t python/ $PACKAGES
zip -r python_layer.zip python/
