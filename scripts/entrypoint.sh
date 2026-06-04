#!/bin/bash
set -e

make install_deps || true

make re 2>&1 | tee /tmp/make_output.txt

python3 /scripts/coding_style_checker.py < /tmp/make_output.txt
