#!/bin/bash
set -e
echo "=== START ==="
make re 2>&1 | tee /tmp/make_output.txt
echo "=== MAKE DONE ==="
python3 /scripts/coding_style_checker.py < /tmp/make_output.txt
echo "=== PYTHON DONE ==="
