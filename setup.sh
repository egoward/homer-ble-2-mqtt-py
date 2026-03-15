#!/bin/bash
set -e
INSTALL_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$INSTALL_DIR"
python3 -m venv venv
venv/bin/pip install --prefer-binary -r requirements.txt

cat > ble2mqtt.service << EOF
[Unit]
Description=BLE to MQTT
After=multi-user.target

[Service]
Type=simple
Restart=always
ExecStart=${INSTALL_DIR}/venv/bin/python3 ${INSTALL_DIR}/ble2mqtt.py

[Install]
WantedBy=multi-user.target
EOF

echo "Done. Now run:"
echo "  sudo cp ${INSTALL_DIR}/ble2mqtt.service /etc/systemd/system/"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl restart ble2mqtt"
