#!/usr/bin/env bash
# Đồng bộ TOÀN BỘ skill trong repo "skill-claude" (bộ skill công ty) từ GitHub
# về managed-skills local của agent, để agent luôn nạp bản mới nhất mỗi phiên.
#
# Dùng:
#   bash sync.sh                 # clone/pull repo + copy mọi skill vào managed-skills
#   SKILLS_CLONE_DIR=... SKILLS_TARGET_ROOT=... bash sync.sh   # override thư mục
#
# An toàn chạy lại nhiều lần (idempotent) — nếu đã là bản mới nhất sẽ báo và thoát,
# không ghi đè gì thêm.
#
# Cấu trúc repo: mỗi skill là 1 thư mục con ở root (vd zalo-pre-submit-review/,
# figma-logic-conformance-test/) với SKILL.md ở gốc thư mục đó. Thêm skill mới:
# tạo thư mục con mới có SKILL.md, không cần sửa file này (script tự phát hiện
# mọi thư mục con chứa SKILL.md).

set -euo pipefail

REPO_URL="https://github.com/nguyenba16/zalo-pre-submit-review-skills.git"
CLONE_DIR="${SKILLS_CLONE_DIR:-$HOME/.cache/zalo-pre-submit-review-skills}"
TARGET_ROOT="${SKILLS_TARGET_ROOT:-$HOME/.omp/agent/managed-skills}"

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

# Tự phát hiện mọi skill: bất kỳ thư mục con trực tiếp nào ở root repo có
# SKILL.md (không phải README/AGENTS.md/CLAUDE.md/agents/ ở root — đó là
# artefact của repo dev, không phải nội dung skill).
SKILL_NAMES=()
for d in "$CLONE_DIR"/*/; do
  name="$(basename "$d")"
  [ -f "$d/SKILL.md" ] && SKILL_NAMES+=("$name")
done

if [ "${#SKILL_NAMES[@]}" -eq 0 ]; then
  echo "[sync] ERROR: không tìm thấy thư mục skill nào (có SKILL.md) trong $CLONE_DIR" >&2
  exit 1
fi

# "Up to date" chỉ đúng nếu TẤT CẢ skill đã có mặt đầy đủ ở target — tránh
# trường hợp 1 lần chạy trước clone/fetch thành công nhưng copy dở dang (vd
# file bị khoá bởi chương trình khác) bị coi nhầm là "đã mới nhất" mãi mãi.
NEEDS_COPY=0
for name in "${SKILL_NAMES[@]}"; do
  [ -f "$TARGET_ROOT/$name/SKILL.md" ] || NEEDS_COPY=1
done

if [ -n "$OLD_SHA" ] && [ "$OLD_SHA" = "$NEW_SHA" ] && [ "$NEEDS_COPY" -eq 0 ]; then
  echo "[sync] Already up to date (commit ${NEW_SHA:0:7}) - nothing to update."
  exit 0
fi

for name in "${SKILL_NAMES[@]}"; do
  src="$CLONE_DIR/$name"
  dst="$TARGET_ROOT/$name"
  mkdir -p "$dst"
  # rsync-like copy via cp -a + xoá file mồ côi: đơn giản hoá bằng cách xoá
  # sạch dst rồi copy lại toàn bộ (an toàn vì dst chỉ chứa bản sync trước đó,
  # không phải nơi người dùng tự sửa tay).
  rm -rf "${dst:?}"/*
  if ! cp -a "$src"/. "$dst"/; then
    echo "[sync] ERROR: failed to copy skill '$name' to $dst (locked by another program? permissions?)" >&2
    exit 1
  fi
  echo "[sync]   synced skill: $name"
done

echo "[sync] Updated ${#SKILL_NAMES[@]} skill(s) under $TARGET_ROOT: ${SKILL_NAMES[*]}"
if [ -n "$OLD_SHA" ]; then
  echo "[sync] ${OLD_SHA:0:7} -> ${NEW_SHA:0:7}"
  echo "[sync] Content changes:"
  git -C "$CLONE_DIR" log --oneline "${OLD_SHA}..${NEW_SHA}" | sed 's/^/  /'
else
  echo "[sync] First-time install (${NEW_SHA:0:7})."
fi
