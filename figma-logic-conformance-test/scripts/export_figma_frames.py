#!/usr/bin/env python3
"""
export_figma_frames.py — export every top-level FRAME node of a Figma file
as a PNG, plus a manifest mapping frame name -> node id -> local file path.

Why: Lane A (UI vs Figma) of the figma-logic-conformance-test skill needs a
reference screenshot per screen. This script is the deterministic half —
downloading images from Figma's REST API — it does NOT decide whether the
built app matches (that needs a vision model / human, see SKILL.md).

Usage
-----
    export FIGMA_TOKEN=figd_xxx   # personal access token, Figma > Settings > Personal access tokens
    python3 export_figma_frames.py <file_key> <output_dir> [--page "Page name"]

`file_key` is the id in the Figma URL: figma.com/file/<file_key>/...
`--page` restricts export to frames inside one canvas/page (BA files often
have multiple pages — flows, components, archive — you usually only want one).

Output
------
    <output_dir>/manifest.json   — [{"name": "...", "node_id": "...", "file": "..."}]
    <output_dir>/<slug>.png      — one PNG per frame, 2x scale
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import requests

API_ROOT = "https://api.figma.com/v1"


def slugify(name: str) -> str:
    s = re.sub(r"[^\w\-]+", "-", name.strip(), flags=re.UNICODE).strip("-").lower()
    return s or "frame"


def find_top_level_frames(node: dict, page_filter: str | None) -> list[dict]:
    """Walk the Figma document tree; a Figma file is document -> pages (CANVAS)
    -> top-level FRAME nodes (screens). We deliberately do NOT recurse inside a
    frame — nested frames are usually components/variants, not separate screens.
    """
    frames = []
    for page in node.get("children", []):
        if page.get("type") != "CANVAS":
            continue
        if page_filter and page.get("name") != page_filter:
            continue
        for child in page.get("children", []):
            if child.get("type") == "FRAME":
                frames.append({"name": child["name"], "id": child["id"], "page": page.get("name")})
    return frames


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file_key")
    ap.add_argument("output_dir", type=Path)
    ap.add_argument("--page", default=None, help="Chỉ export frame trong 1 page/canvas cụ thể (theo tên)")
    ap.add_argument("--token", default=None, help="Figma personal access token (mặc định đọc env FIGMA_TOKEN)")
    ap.add_argument("--scale", type=float, default=2.0)
    args = ap.parse_args()

    import os
    token = args.token or os.environ.get("FIGMA_TOKEN")
    if not token:
        print("error: cần Figma token — truyền --token hoặc set env FIGMA_TOKEN", file=sys.stderr)
        sys.exit(2)

    headers = {"X-Figma-Token": token}
    args.output_dir.mkdir(parents=True, exist_ok=True)

    doc_resp = requests.get(f"{API_ROOT}/files/{args.file_key}", headers=headers, params={"depth": 2}, timeout=30)
    doc_resp.raise_for_status()
    document = doc_resp.json()["document"]

    frames = find_top_level_frames(document, args.page)
    if not frames:
        print("error: không tìm thấy frame nào (kiểm tra --page hoặc file_key)", file=sys.stderr)
        sys.exit(1)

    ids = ",".join(f["id"] for f in frames)
    img_resp = requests.get(
        f"{API_ROOT}/images/{args.file_key}",
        headers=headers,
        params={"ids": ids, "format": "png", "scale": args.scale},
        timeout=60,
    )
    img_resp.raise_for_status()
    image_urls = img_resp.json().get("images", {})

    manifest = []
    for f in frames:
        url = image_urls.get(f["id"])
        if not url:
            print(f"warn: không có ảnh cho frame {f['name']!r} ({f['id']}) — có thể quá lớn/lỗi render", file=sys.stderr)
            continue
        slug = slugify(f["name"])
        out_path = args.output_dir / f"{slug}.png"
        img_bytes = requests.get(url, timeout=60).content
        out_path.write_bytes(img_bytes)
        manifest.append({"name": f["name"], "node_id": f["id"], "page": f["page"], "file": str(out_path)})
        print(f"exported: {f['name']} -> {out_path}")

    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{len(manifest)} frame(s) exported. manifest: {args.output_dir / 'manifest.json'}")
    print("Bước tiếp theo: điền route tương ứng cho từng frame vào 1 file "
          "figma-route-map.json (frame name/node_id -> route path trong app) trước khi chạy Lane A đầy đủ.")


if __name__ == "__main__":
    main()
