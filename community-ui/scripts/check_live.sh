#!/usr/bin/env bash
set -euo pipefail
# Example: WEBLATE_URL=https://translate.example.com bash scripts/check_live.sh
: "${WEBLATE_URL:?Set WEBLATE_URL, e.g. https://translate.example.com}"
WEBLATE_URL="${WEBLATE_URL%/}"
for path in / /projects/ /api/; do
  echo "Checking ${WEBLATE_URL}${path}"
  curl --fail --silent --show-error --max-time 20 --location --output /dev/null \
    --write-out 'HTTP %{http_code}, %{time_total}s\n' "${WEBLATE_URL}${path}"
done
printf '\nBasic GET probes completed. Translation, review, CSRF and Git flows require authenticated E2E tests.\n'
