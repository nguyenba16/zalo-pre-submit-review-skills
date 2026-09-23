#!/usr/bin/env bash
# Vendor 1 hoặc nhiều skill từ repo này vào thư mục .omp/skills/ của MỘT
# project đích cụ thể — khác với sync.sh (cài global vào
# ~/.omp/agent/managed-skills/, dùng chung mọi project trên máy).
#
# Dùng cách này khi muốn skill đi kèm project đó trong chính git repo của nó:
# ai clone project đích về là có sẵn skill, không cần mỗi dev tự chạy lệnh cài
# riêng trên máy mình.
#
# Dùng:
#   bash install-local.sh <target_project_dir>                      # copy TẤT CẢ skill
#   bash install-local.sh <target_project_dir> <skill-name> [...]   # copy skill cụ thể
#
# Ví dụ:
#   bash install-local.sh ~/work/cty/mini-app-thuc-te
#   bash install-local.sh ~/work/cty/mini-app-thuc-te zalo-pre-submit-review
#
# Sau khi chạy: `git add .omp/skills` trong project đích rồi commit — từ đó
# skill là 1 phần của project đó, không phải cấu hình riêng của máy bạn.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-}"
shift || true
REQUESTED_SKILLS=("$@")

if [ -z "$TARGET_DIR" ]; then
  echo "usage: bash install-local.sh <target_project_dir> [skill-name ...]" >&2
  exit 2
fi
if [ ! -d "$TARGET_DIR" ]; then
  echo "error: '$TARGET_DIR' không phải thư mục tồn tại" >&2
  exit 2
fi
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

# Tự phát hiện mọi skill trong repo này (thư mục con có SKILL.md), giống
# logic sync.sh — thêm skill mới vào repo thì script này tự nhận, không cần sửa.
ALL_SKILLS=()
for d in "$REPO_ROOT"/*/; do
  name="$(basename "$d")"
  [ -f "$d/SKILL.md" ] && ALL_SKILLS+=("$name")
done

if [ "${#ALL_SKILLS[@]}" -eq 0 ]; then
  echo "error: không tìm thấy skill nào (thư mục con có SKILL.md) trong $REPO_ROOT" >&2
  exit 1
fi

SKILLS_TO_COPY=()
if [ "${#REQUESTED_SKILLS[@]}" -eq 0 ]; then
  SKILLS_TO_COPY=("${ALL_SKILLS[@]}")
else
  for want in "${REQUESTED_SKILLS[@]}"; do
    found=0
    for have in "${ALL_SKILLS[@]}"; do
      [ "$want" = "$have" ] && { found=1; break; }
    done
    if [ "$found" -eq 0 ]; then
      echo "error: skill '$want' không tồn tại trong repo. Có sẵn: ${ALL_SKILLS[*]}" >&2
      exit 2
    fi
    SKILLS_TO_COPY+=("$want")
  done
fi

REPO_URL="https://github.com/nguyenba16/zalo-pre-submit-review-skills.git"
SOURCE_SHA="unknown"
if git -C "$REPO_ROOT" rev-parse HEAD >/dev/null 2>&1; then
  SOURCE_SHA="$(git -C "$REPO_ROOT" rev-parse HEAD)"
else
  echo "warn: '$REPO_ROOT' không phải git repo (hoặc chưa có commit nào) — .vendor-meta.json sẽ ghi commit=unknown, check-local-updates.sh sẽ không so sánh được." >&2
fi

DEST_ROOT="$TARGET_DIR/.omp/skills"
mkdir -p "$DEST_ROOT"
for name in "${SKILLS_TO_COPY[@]}"; do
  dest="$DEST_ROOT/$name"
  mkdir -p "$dest"
  rm -rf "${dest:?}"/*
  cp -a "$REPO_ROOT/$name"/. "$dest"/
  cat > "$dest/.vendor-meta.json" <<EOF
{
  "skill": "$name",
  "source_repo": "$REPO_URL",
  "commit": "$SOURCE_SHA",
  "vendored_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
  echo "[install-local]   vendored: $name -> $dest (commit ${SOURCE_SHA:0:7})"
done

echo
echo "[install-local] Đã copy ${#SKILLS_TO_COPY[@]} skill vào $DEST_ROOT"
echo "[install-local] Bước tiếp theo (trong repo project đích, không phải repo này):"
echo "  cd '$TARGET_DIR' && git add .omp/skills && git commit -m 'vendor AI skill(s) into project'"
echo "[install-local] Sau khi commit, mở agent (Claude Code/omp/ckit) NGAY TRONG project đích — skill tự nạp, không cần cài gì thêm."
