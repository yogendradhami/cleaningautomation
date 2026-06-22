#!/usr/bin/env bash
set -euo pipefail

# Helper to trigger a manual deploy on Render via API.
# Requires RENDER_SERVICE_ID and RENDER_API_KEY environment variables.

if [ -z "${RENDER_SERVICE_ID:-}" ] || [ -z "${RENDER_API_KEY:-}" ]; then
  echo "RENDER_SERVICE_ID and RENDER_API_KEY must be set in the environment or .env"
  exit 2
fi

echo "Triggering deploy for Render service $RENDER_SERVICE_ID..."

resp=$(curl -s -X POST "https://api.render.com/v1/services/${RENDER_SERVICE_ID}/deploys" \
  -H "Authorization: Bearer ${RENDER_API_KEY}" \
  -H "Accept: application/json")

echo "$resp"
echo "If the response contains an 'id' field the deploy was created. Check Render dashboard for progress."
