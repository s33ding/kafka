#!/bin/bash

set -e

# Define constants
RELEASE_NAME="kafka"
VALUES_FILE="values-kafka.yaml"
CHART_REPO="oci://registry-1.docker.io/bitnamicharts/kafka"

# Add client.enabled=true if not already present
if ! grep -q "^client:" "$VALUES_FILE"; then
  echo -e "\n# Enable Kafka test client\nclient:\n  enabled: true" >> "$VALUES_FILE"
  echo "✅ Appended client.enabled: true to $VALUES_FILE"
else
  echo "ℹ️  Kafka client section already exists in $VALUES_FILE"
fi

# Perform the upgrade
echo "🚀 Upgrading Kafka Helm release..."
helm upgrade "$RELEASE_NAME" -f "$VALUES_FILE" "$CHART_REPO"

echo "✅ Upgrade complete."

