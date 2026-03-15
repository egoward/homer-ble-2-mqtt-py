#!/bin/bash
set -e
cd "$(dirname "$0")"
python3 -m venv venv
venv/bin/pip install --prefer-binary -r requirements.txt
echo "Done. Now run:"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl restart ble2mqtt"
