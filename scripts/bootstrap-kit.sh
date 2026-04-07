#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME_OVERRIDE=""
DOCTOR_JSON=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --codex-home)
      CODEX_HOME_OVERRIDE="$2"
      shift 2
      ;;
    --doctor-json)
      DOCTOR_JSON=1
      shift
      ;;
    *)
      echo "[error] unknown option: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -n "$CODEX_HOME_OVERRIDE" ]]; then
  export CODEX_HOME="$CODEX_HOME_OVERRIDE"
fi

echo "[OK] installing Salesforce Codex kit links"
"$ROOT_DIR/scripts/install-to-codex-home.sh"

echo "[OK] running doctor"
DOCTOR_ARGS=()
if [[ -n "${CODEX_HOME:-}" ]]; then
  DOCTOR_ARGS+=(--codex-home "$CODEX_HOME")
fi
if [[ "$DOCTOR_JSON" -eq 1 ]]; then
  if [[ "${#DOCTOR_ARGS[@]}" -gt 0 ]]; then
    python3 "$ROOT_DIR/scripts/doctor.py" --json "${DOCTOR_ARGS[@]}"
  else
    python3 "$ROOT_DIR/scripts/doctor.py" --json
  fi
else
  if [[ "${#DOCTOR_ARGS[@]}" -gt 0 ]]; then
    python3 "$ROOT_DIR/scripts/doctor.py" "${DOCTOR_ARGS[@]}"
  else
    python3 "$ROOT_DIR/scripts/doctor.py"
  fi
fi
