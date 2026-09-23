#!/usr/bin/env python3
"""
Staleness checker cho skill zalo-pre-submit-review.

Re-fetch tat ca URL nguon trong sources.json, so sanh content_hash voi baseline.
In ra danh sach trang da THAY DOI (can nguoi doc lai + cap nhat checklist.md),
trang LOI (404/timeout - co the doi URL), va trang KHONG DOI.

Chay dinh ky (khuyen nghi: hang thang, hoac truoc khi dung skill cho 1 du an lon):
    python3 check_updates.py            # chi bao cao, khong ghi de sources.json
    python3 check_updates.py --update   # ghi de sources.json voi hash moi (sau khi da doi chieu checklist.md)

Yeu cau: pip install requests beautifulsoup4
"""
import re, json, hashlib, sys, time
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependency. Run: pip install requests beautifulsoup4")
    sys.exit(1)

HERE = Path(__file__).parent
SOURCES = HERE / "sources.json"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}


def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style', 'svg', 'img', 'nav', 'footer']):
        tag.decompose()
    main = soup.find('article') or soup.find('main') or soup
    text = main.get_text(separator='\n')
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return '\n'.join(lines)


def fetch_hash(url: str):
    r = requests.get(url, headers=HEADERS, timeout=20)
    text = extract_text(r.text)
    return hashlib.sha256(text.encode('utf-8')).hexdigest(), len(text), r.status_code


def main():
    update = '--update' in sys.argv
    baseline = json.loads(SOURCES.read_text(encoding='utf-8'))

    changed, unchanged, errored = [], [], []

    for url, meta in baseline.items():
        try:
            h, length, status = fetch_hash(url)
        except Exception as e:
            errored.append((url, str(e)))
            continue

        old_hash = meta.get("content_hash")
        if old_hash is None:
            errored.append((url, "no baseline hash (page errored last time)"))
        elif h != old_hash:
            changed.append((url, meta.get("last_checked", "?")))
            if update:
                baseline[url] = {
                    "content_hash": h, "text_length": length,
                    "http_status": status, "last_checked": time.strftime("%Y-%m-%d"),
                }
        else:
            unchanged.append(url)

    print(f"\n=== Staleness check result ({time.strftime('%Y-%m-%d')}) ===\n")
    print(f"Unchanged: {len(unchanged)}/{len(baseline)}")
    if changed:
        print(f"\n>>> CHANGED ({len(changed)}) - re-read and update checklist.md:")
        for url, last in changed:
            print(f"  - {url}  (baseline at: {last})")
    if errored:
        print(f"\n>>> ERROR fetching ({len(errored)}) - check if URL is still valid:")
        for url, err in errored:
            print(f"  - {url}: {err}")

    if update and changed:
        SOURCES.write_text(json.dumps(baseline, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"\nWrote sources.json with new hash for {len(changed)} page(s).")
        print("NOTE: a new hash only confirms 're-fetched', it does NOT auto-update checklist.md - read and edit it by hand/agent.")

    if not changed and not errored:
        print("\nAll sources match baseline - checklist.md is in sync with Zalo documentation.")


if __name__ == "__main__":
    main()
