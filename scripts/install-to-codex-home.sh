#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/skills"
TARGET_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
TOOLKIT_LINK="${CODEX_HOME:-$HOME/.codex}/salesforce-kit"

mkdir -p "$TARGET_DIR"

for skill_dir in "$SOURCE_DIR"/*; do
  [ -d "$skill_dir" ] || continue

  skill_name="$(basename "$skill_dir")"
  target_path="$TARGET_DIR/$skill_name"

  if [ -L "$target_path" ]; then
    current_target="$(readlink "$target_path")"
    if [ "$current_target" = "$skill_dir" ]; then
      echo "[skip] $skill_name already linked"
      continue
    fi
    echo "[error] $target_path points to a different location: $current_target" >&2
    exit 1
  fi

  if [ -e "$target_path" ]; then
    echo "[error] $target_path already exists and is not a symlink" >&2
    exit 1
  fi

  ln -s "$skill_dir" "$target_path"
  echo "[link] $skill_name -> $skill_dir"
done

if [ -L "$TOOLKIT_LINK" ]; then
  current_target="$(readlink "$TOOLKIT_LINK")"
  if [ "$current_target" = "$ROOT_DIR" ]; then
    echo "[skip] salesforce-kit already linked"
    exit 0
  fi
  echo "[error] $TOOLKIT_LINK points to a different location: $current_target" >&2
  exit 1
fi

if [ -e "$TOOLKIT_LINK" ]; then
  echo "[error] $TOOLKIT_LINK already exists and is not a symlink" >&2
  exit 1
fi

ln -s "$ROOT_DIR" "$TOOLKIT_LINK"
echo "[link] salesforce-kit -> $ROOT_DIR"
