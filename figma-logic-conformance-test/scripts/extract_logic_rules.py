#!/usr/bin/env python3
"""
extract_logic_rules.py — turn a BA-authored logic.md file into an atomic,
traceable rule list (same convention as zalo-pre-submit-review's
checklist.md: one rule, one ID, one source line).

This is a best-effort STRUCTURAL parser (headings + bullet/numbered lines +
Gherkin Given/When/Then blocks) — it does NOT use an LLM and does NOT judge
whether a rule is testable. BA docs are rarely as clean as official
platform docs, so the script also reports a `structured_ratio`: the
fraction of non-empty body lines that look like a rule (bullet/numbered/
Given-When-Then) vs prose. Below ~0.5, treat the file as prose — read it
yourself / dispatch an agent to extract rules by hand rather than trusting
this script's rule list, which will be sparse/wrong on prose input.

Usage
-----
    python3 extract_logic_rules.py <logic.md> [--json out.json]

Output: JSON to stdout (or --json file):
{
  "source": "<path>",
  "structured_ratio": 0.83,
  "warning": "..." | null,
  "sections": [
    {"heading": "2. Tính giá đơn hàng", "line": 12, "rules": [
        {"id": "2-tinh-gia-don-hang-1", "line": 14, "text": "..."}
    ]}
  ]
}
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
BULLET_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+(\S.*)$")
GWT_RE = re.compile(r"^\s*(Given|When|Then|And|But|Giả sử|Khi|Thì|Và)\b", re.IGNORECASE)


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\-]+", "-", text.strip(), flags=re.UNICODE).strip("-").lower()
    return s[:60] or "section"


def parse(md_text: str) -> dict:
    lines = md_text.splitlines()
    sections: list[dict] = []
    current = {"heading": "(mở đầu file — trước heading đầu tiên)", "line": 1, "rules": []}
    sections.append(current)

    rule_like_count = 0
    prose_count = 0

    for i, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        if not line.strip():
            continue

        h = HEADING_RE.match(line)
        if h:
            current = {"heading": h.group(2), "line": i, "rules": []}
            sections.append(current)
            continue

        b = BULLET_RE.match(line)
        g = GWT_RE.match(line)
        if b or g:
            rule_like_count += 1
            text = b.group(1) if b else line.strip()
            rule_id = f"{slugify(current['heading'])}-{len(current['rules']) + 1}"
            current["rules"].append({"id": rule_id, "line": i, "text": text})
        else:
            prose_count += 1

    total = rule_like_count + prose_count
    ratio = round(rule_like_count / total, 2) if total else 0.0
    warning = None
    if ratio < 0.5:
        warning = (
            f"Chỉ {ratio*100:.0f}% dòng nội dung trông giống rule (bullet/số/Given-When-Then) — "
            "file này có vẻ viết dạng văn xuôi. Danh sách rule dưới đây SẼ THIẾU/SAI — "
            "cần agent/người đọc trực tiếp file gốc để trích rule thay vì tin kết quả script này."
        )

    # Drop the synthetic leading section if it captured nothing (common case:
    # file starts directly with a heading).
    sections = [s for s in sections if s["rules"] or s is not sections[0] or s["rules"]]
    if sections and sections[0]["heading"].startswith("(mở đầu") and not sections[0]["rules"]:
        sections = sections[1:]

    return {"structured_ratio": ratio, "warning": warning, "sections": sections}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("logic_md", type=Path)
    ap.add_argument("--json", type=Path, default=None, help="Ghi JSON ra file thay vì stdout")
    args = ap.parse_args()

    if not args.logic_md.exists():
        print(f"error: {args.logic_md} không tồn tại", file=sys.stderr)
        sys.exit(2)

    result = parse(args.logic_md.read_text(encoding="utf-8"))
    result["source"] = str(args.logic_md)

    total_rules = sum(len(s["rules"]) for s in result["sections"])
    out = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json:
        args.json.write_text(out, encoding="utf-8")
        print(f"{total_rules} rule(s) trong {len(result['sections'])} section -> {args.json}", file=sys.stderr)
    else:
        print(out)

    if result["warning"]:
        print(f"\nWARNING: {result['warning']}", file=sys.stderr)


if __name__ == "__main__":
    main()
