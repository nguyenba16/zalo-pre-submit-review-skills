#!/usr/bin/env bash
# Kiểm tra skill đã vendor vào 1 project đích (qua install-local.sh) có đang
# lỗi thời so với repo skill-claude gốc trên GitHub không.
#
# Vì install-local.sh chỉ COPY file tĩnh (không phải git submodule), project
# đích không có cách nào tự biết repo skill-claude gốc đã đổi — script này
# là cơ chế bù cho khoảng trống đó: đọc commit đã vendor (ghi trong
# .vendor-meta.json), so với commit mới nhất trên GitHub, báo skill nào có
# thay đổi thật sự ảnh hưởng tới nó (không báo ồn ào nếu người khác chỉ sửa
# 1 skill khác không liên quan).
#
# Dùng:
#   bash check-local-updates.sh <target_project_dir>
#
# Chạy định kỳ (khuyến nghị hàng tháng, giống check_updates.py của skill
# zalo-pre-submit-review) hoặc trước khi dùng skill cho 1 dự án/khách hàng mới.

set -euo pipefail

REPO_URL="https://github.com/nguyenba16/zalo-pre-submit-review-skills.git"
CLONE_DIR="${SKILLS_CLONE_DIR:-$HOME/.cache/zalo-pre-submit-review-skills}"
TARGET_DIR="${1:-.}"

# `timeout` là GNU coreutils — macOS mặc định KHÔNG có (chỉ có nếu `brew
# install coreutils`, dưới tên `gtimeout`). Không dùng bash array cho lệnh
# timeout (rỗng dưới `set -u` sẽ vỡ trên bash 3.2 — bash mặc định của macOS,
# `/usr/bin/env bash` vẫn resolve về bản này). Dùng hàm wrapper string thay thế.
HAVE_TIMEOUT=""
if command -v timeout >/dev/null 2>&1; then
  HAVE_TIMEOUT="timeout"
elif command -v gtimeout >/dev/null 2>&1; then
  HAVE_TIMEOUT="gtimeout"
fi

run_git() {
  if [ -n "$HAVE_TIMEOUT" ]; then
    "$HAVE_TIMEOUT" 20 git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=20 "$@"
  else
    git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=20 "$@"
  fi
}

if [ ! -d "$TARGET_DIR" ]; then
  echo "error: '$TARGET_DIR' không phải thư mục tồn tại" >&2
  exit 2
fi
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"
SKILLS_DIR="$TARGET_DIR/.omp/skills"

if [ ! -d "$SKILLS_DIR" ]; then
  echo "error: không tìm thấy $SKILLS_DIR — project này chưa vendor skill nào qua install-local.sh" >&2
  exit 1
fi

if [ -d "$CLONE_DIR/.git" ]; then
  if ! run_git -C "$CLONE_DIR" fetch origin main --quiet; then
    echo "error: không fetch được '$REPO_URL' (mất mạng, chặn firewall/VPN công ty, hoặc GitHub không truy cập được từ máy này). Kiểm tra kết nối rồi chạy lại." >&2
    exit 4
  fi
else
  mkdir -p "$(dirname "$CLONE_DIR")"
  if ! run_git clone --quiet "$REPO_URL" "$CLONE_DIR"; then
    echo "error: không clone được '$REPO_URL' (mất mạng, chặn firewall/VPN công ty, hoặc GitHub không truy cập được từ máy này). Kiểm tra kết nối rồi chạy lại." >&2
    rm -rf "$CLONE_DIR"
    exit 4
  fi
fi
LATEST_SHA="$(git -C "$CLONE_DIR" rev-parse origin/main)"

FOUND_ANY=0
ANY_OUTDATED=0
for d in "$SKILLS_DIR"/*/; do
  name="$(basename "$d")"
  meta="$d/.vendor-meta.json"
  if [ ! -f "$meta" ]; then
    echo "[check]   $name: bỏ qua (không có .vendor-meta.json — vendor thủ công hoặc bản cũ trước khi có cơ chế này)"
    continue
  fi
  FOUND_ANY=1

  vendored_sha="$(grep -o '"commit"[[:space:]]*:[[:space:]]*"[a-f0-9]\{7,40\}"' "$meta" | grep -o '[a-f0-9]\{7,40\}' || true)"
  if [ -z "$vendored_sha" ]; then
    echo "[check]   $name: .vendor-meta.json không có commit hợp lệ (vendor từ bản không phải git repo) — không so sánh được, xem lại thủ công"
    continue
  fi

  if ! git -C "$CLONE_DIR" cat-file -e "$vendored_sha" 2>/dev/null; then
    echo "[check]   $name: commit đã vendor ($vendored_sha) không tìm thấy trong lịch sử repo (branch bị force-push/rebase?) — không so sánh được, xem lại thủ công"
    continue
  fi

  changed="$(git -C "$CLONE_DIR" log --oneline "${vendored_sha}..${LATEST_SHA}" -- "$name/" 2>/dev/null || true)"
  if [ -n "$changed" ]; then
    ANY_OUTDATED=1
    n="$(echo "$changed" | wc -l | tr -d ' ')"
    echo "[check]   $name: LỖI THỜI — $n commit đã đổi kể từ lúc vendor (${vendored_sha:0:7} -> ${LATEST_SHA:0:7})."
    echo "$changed" | sed 's/^/            /'
  else
    echo "[check]   $name: đã mới nhất (vendor tại ${vendored_sha:0:7}, remote hiện ${LATEST_SHA:0:7}, không có commit nào đổi skill này)."
  fi
done

if [ "$FOUND_ANY" -eq 0 ]; then
  echo "[check] Không có skill nào trong $SKILLS_DIR được vendor qua install-local.sh (thiếu .vendor-meta.json ở mọi thư mục con)" >&2
  exit 1
fi

if [ "$ANY_OUTDATED" -eq 1 ]; then
  echo
  echo "[check] Có skill lỗi thời. Chạy lại: bash install-local.sh '$TARGET_DIR' <skill-name>  rồi commit lại."
  exit 3
fi
