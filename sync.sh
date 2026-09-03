#!/usr/bin/env bash
# Đồng bộ skill "zalo-pre-submit-review" từ GitHub repo về managed-skills local
# của agent, để agent luôn nạp bản checklist mới nhất mỗi phiên.
#
# Dùng:
#   bash sync.sh                 # clone/pull repo + copy file runtime vào managed-skills
#   ZPSR_CLONE_DIR=... ZPSR_TARGET_DIR=... bash sync.sh   # override thư mục
#
# An toàn chạy lại nhiều lần (idempotent) — nếu đã là bản mới nhất sẽ báo và thoát,
# không ghi đè gì thêm.

set -euo pipefail

REPO_URL="https://github.com/nguyenba16/zalo-pre-submit-review-skills.git"
CLONE_DIR="${ZPSR_CLONE_DIR:-$HOME/.cache/zalo-pre-submit-review-skills}"
TARGET_DIR="${ZPSR_TARGET_DIR:-$HOME/.omp/agent/managed-skills/zalo-pre-submit-review}"

# Các file thực sự được agent dùng khi chạy skill (không đồng bộ README/AGENTS.md/
# CLAUDE.md/agents/ — đó là artefact riêng của repo dev, không phải của managed skill).
RUNTIME_FILES=(SKILL.md checklist.md checklist.docx sources.json check_updates.py requirements.txt CHANGELOG.md)

if [ -d "$CLONE_DIR/.git" ]; then
  OLD_SHA="$(git -C "$CLONE_DIR" rev-parse HEAD)"
  git -C "$CLONE_DIR" fetch origin main --quiet
  git -C "$CLONE_DIR" reset --hard origin/main --quiet
else
  OLD_SHA=""
  mkdir -p "$(dirname "$CLONE_DIR")"
  git clone --quiet "$REPO_URL" "$CLONE_DIR"
fi
NEW_SHA="$(git -C "$CLONE_DIR" rev-parse HEAD)"

# "Up to date" only holds if the target dir is ALSO actually fully populated —
# guards against a prior run whose git clone/fetch succeeded but whose file
# copy step failed partway (e.g. a target file locked by another program),
# which would otherwise be masked as "nothing to update" forever.
NEEDS_COPY=0
for f in "${RUNTIME_FILES[@]}"; do
  [ -f "$TARGET_DIR/$f" ] || NEEDS_COPY=1
done

if [ -n "$OLD_SHA" ] && [ "$OLD_SHA" = "$NEW_SHA" ] && [ "$NEEDS_COPY" -eq 0 ]; then
  echo "[sync] Already up to date (commit ${NEW_SHA:0:7}) - nothing to update."
  exit 0
fi

mkdir -p "$TARGET_DIR"
for f in "${RUNTIME_FILES[@]}"; do
  if ! cp -f "$CLONE_DIR/$f" "$TARGET_DIR/$f"; then
    echo "[sync] ERROR: failed to copy $f to $TARGET_DIR (locked by another program? permissions?)" >&2
    exit 1
  fi
  echo "[sync]   copied $f"
done
echo "[sync] Updated $TARGET_DIR"
if [ -n "$OLD_SHA" ]; then
  echo "[sync] ${OLD_SHA:0:7} -> ${NEW_SHA:0:7}"
  echo "[sync] Checklist/skill content changes:"
  git -C "$CLONE_DIR" log --oneline "${OLD_SHA}..${NEW_SHA}" -- CHANGELOG.md checklist.md SKILL.md | sed 's/^/  /'
else
  echo "[sync] First-time install (${NEW_SHA:0:7})."
fi
