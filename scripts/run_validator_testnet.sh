#!/usr/bin/env bash
set -euo pipefail

export NETWORK="${NETWORK:-test}"
export NETUID="${NETUID:-9999}"
export ENVELOPE_ROOM_UID="${ENVELOPE_ROOM_UID:-0}"
export WALLET_NAME="${WALLET_NAME:-default}"
export HOTKEY_NAME="${HOTKEY_NAME:-default}"
export JOB_BOARD_URL="${JOB_BOARD_URL:-http://127.0.0.1:8088}"

python -m validator.validator \
  --network "$NETWORK" \
  --netuid "$NETUID" \
  --coldkey "$WALLET_NAME" \
  --hotkey "$HOTKEY_NAME" \
  --envelope-room-uid "$ENVELOPE_ROOM_UID" \
  --job-board-url "$JOB_BOARD_URL"
