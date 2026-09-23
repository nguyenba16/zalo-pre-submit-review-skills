#!/usr/bin/env python3
"""
scan_static_checklist.py — deterministic static scanner for the
"Automatable: yes" items of checklist.md (Nhóm A/C/D/E) on a real
Zalo Mini App project (zmp-sdk + zmp-ui + Vite, any project).

Why this script exists
-----------------------
SKILL.md's original workflow re-derives the same ~90 "yes" checks by hand
every run via 4 parallel scout subagents reading grep patterns out of
checklist.md. That is correct but non-deterministic (LLM judgment on a
mechanical regex/JSON check) and costs tool-call rounds every single time.
This script turns the subset that is TRULY mechanical (string/regex/JSON/
file-size checks — no semantic judgment) into a fast, repeatable, CI-able
pass. It does NOT replace the subagent dispatch step for "partial" items
(those need judgment) — it only removes the "yes" items from that queue.

Usage
-----
    python3 scan_static_checklist.py <project_root> [--build-dir dist]

Output: Markdown report to stdout with PASS/FAIL/WARN/SKIP per check ID,
each ID traceable back to a `checklist.md` heading (Nhóm + section number)
so a human/agent can look up the source URL and remediation text.

Exit code: 1 if any FAIL, 0 otherwise (WARN/SKIP do not fail the run) —
safe to wire into a pre-submit CI gate with `|| true` if you only want the
report, or without it to hard-block on FAIL.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    from PIL import Image  # optional — only needed for the logo alpha check
except ImportError:
    Image = None

STATUS_ORDER = {"FAIL": 0, "WARN": 1, "SKIP": 2, "PASS": 3}


@dataclass
class Result:
    check_id: str
    group: str
    title: str
    status: str  # PASS | FAIL | WARN | SKIP
    evidence: str = ""


@dataclass
class Ctx:
    root: Path
    build_dir: Path | None
    src_files: list[Path] = field(default_factory=list)
    app_config: dict | None = None
    app_config_path: Path | None = None
    package_json: dict | None = None
    results: list[Result] = field(default_factory=list)

    def add(self, check_id, group, title, status, evidence=""):
        self.results.append(Result(check_id, group, title, status, evidence))


SRC_EXT = {".ts", ".tsx", ".js", ".jsx", ".vue"}
SKIP_DIRS = {"node_modules", "dist", "www", ".git", "build", "coverage"}


def collect_src_files(root: Path) -> list[Path]:
    out = []
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix in SRC_EXT:
            out.append(p)
    return out


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def grep(files: list[Path], pattern: str, flags=re.IGNORECASE) -> list[tuple[Path, int, str]]:
    rx = re.compile(pattern, flags)
    hits = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if rx.search(line):
                hits.append((f, i, line.strip()[:160]))
    return hits


def rel(root: Path, p: Path) -> str:
    try:
        return str(p.relative_to(root))
    except ValueError:
        return str(p)


# ---------------------------------------------------------------------------
# Nhóm A — Chính sách nội dung & kiểm duyệt
# ---------------------------------------------------------------------------

def check_group_a(ctx: Ctx):
    cfg = ctx.app_config or {}
    app = cfg.get("app", {}) if isinstance(cfg, dict) else {}
    title = app.get("title", "") if isinstance(app, dict) else ""
    icon = cfg.get("icon") or app.get("icon") or ""

    # A1 — logo present
    if icon:
        ctx.add("A1.logo-present", "A", "Mini App có logo (không để trống)", "PASS", f"icon={icon}")
    else:
        ctx.add("A1.logo-present", "A", "Mini App có logo (không để trống)", "FAIL",
                "app-config.json thiếu field icon")

    # A1 — logo not transparent background (needs Pillow + the icon file present)
    if icon:
        icon_path = ctx.root / icon.lstrip("/")
        if not icon_path.exists():
            ctx.add("A1.logo-no-alpha", "A", "Logo không có nền trong suốt", "WARN",
                    f"không tìm thấy file icon tại {icon}")
        elif Image is None:
            ctx.add("A1.logo-no-alpha", "A", "Logo không có nền trong suốt", "SKIP",
                    "cần `pip install Pillow` để kiểm tra alpha channel")
        else:
            try:
                img = Image.open(icon_path)
                has_alpha = img.mode in ("RGBA", "LA") and img.getchannel("A").getextrema()[0] < 255
                ctx.add("A1.logo-no-alpha", "A", "Logo không có nền trong suốt",
                        "WARN" if has_alpha else "PASS",
                        f"mode={img.mode}" + (" (có pixel trong suốt)" if has_alpha else ""))
            except Exception as e:
                ctx.add("A1.logo-no-alpha", "A", "Logo không có nền trong suốt", "SKIP", str(e))
    else:
        ctx.add("A1.logo-no-alpha", "A", "Logo không có nền trong suốt", "SKIP", "không có icon để kiểm tra")

    # A2 — name checks
    if title:
        ctx.add("A2.name-not-empty", "A", "Tên Mini App không để trống", "PASS", f"title={title!r}")
        if title.isupper() and any(c.isalpha() for c in title):
            ctx.add("A2.name-not-allcaps", "A", "Tên không viết hoa toàn bộ (ALL CAPS)", "FAIL", title)
        else:
            ctx.add("A2.name-not-allcaps", "A", "Tên không viết hoa toàn bộ (ALL CAPS)", "PASS", title)
        forbidden = re.search(r"\b(app|mini app|zalo)\b", title, re.IGNORECASE)
        ctx.add("A2.name-no-forbidden-words", "A", 'Tên không chứa "App"/"Mini App"/"Zalo"',
                "FAIL" if forbidden else "PASS", title)
        special = re.search(r"[#$@!\U0001F300-\U0001FAFF\u2600-\u27BF]", title)
        ctx.add("A2.name-no-special-chars", "A", "Tên không chứa ký tự đặc biệt/emoji",
                "FAIL" if special else "PASS", title)
    else:
        for cid, label in [
            ("A2.name-not-empty", "Tên Mini App không để trống"),
            ("A2.name-not-allcaps", "Tên không viết hoa toàn bộ (ALL CAPS)"),
            ("A2.name-no-forbidden-words", 'Tên không chứa "App"/"Mini App"/"Zalo"'),
            ("A2.name-no-special-chars", "Tên không chứa ký tự đặc biệt/emoji"),
        ]:
            ctx.add(cid, "A", label, "SKIP", "app-config.json thiếu app.title")

    # A3 — description checks (Zalo Developer Portal description is out-of-repo;
    # this only checks an in-repo description field if the project keeps one,
    # e.g. app-config.json `description` some teams add as a convention).
    desc = app.get("description") or cfg.get("description")
    if desc:
        ctx.add("A3.description-not-empty", "A", "Mô tả không để trống", "PASS")
        has_link = re.search(r"https?://", desc)
        ctx.add("A3.description-no-link", "A", "Mô tả không chứa link ra ngoài",
                "FAIL" if has_link else "PASS", desc[:120])
    else:
        ctx.add("A3.description-not-empty", "A", "Mô tả không để trống", "SKIP",
                "Mô tả submit khai trên Mini App Center, không nằm trong repo — kiểm tra thủ công")

    # A4 — no Google/Facebook third-party login SDK
    fb_google_hits = grep(ctx.src_files, r"signInWithGoogle|GoogleAuthProvider|FB\.login|react-facebook-login|@react-oauth/google")
    ctx.add("A4.no-3rd-party-login", "A", "Không mời đăng nhập Google/Facebook/bên thứ 3",
            "FAIL" if fb_google_hits else "PASS",
            "; ".join(f"{rel(ctx.root, f)}:{ln}" for f, ln, _ in fb_google_hits[:5]))

    # A4 — Checkout SDK vs displayed price heuristic
    has_checkout_sdk = bool((ctx.package_json or {}).get("dependencies", {}).get("zmp-checkout-sdk") or
                             (ctx.package_json or {}).get("dependencies", {}).get("zmp-sdk"))
    price_hits = grep(ctx.src_files, r"(VNĐ|đ\b|₫)\s*[\d.,]{3,}|[\d.,]{3,}\s*(VNĐ|đ\b|₫)")
    if price_hits and not has_checkout_sdk:
        ctx.add("A7.checkout-sdk-required", "A", "Hiển thị giá tiền phải tích hợp Checkout SDK", "WARN",
                f"{len(price_hits)} chỗ hiển thị giá nhưng không thấy zmp-sdk trong dependencies — "
                "xác nhận thủ công có dùng Checkout SDK hay đã đổi CTA thành Liên hệ/Tư vấn")
    else:
        ctx.add("A7.checkout-sdk-required", "A", "Hiển thị giá tiền phải tích hợp Checkout SDK", "PASS")

    # A8 — no leftover Demo/Coming soon placeholders
    demo_hits = grep(ctx.src_files, r"coming soon|demo mode|placeholder|chưa hoàn thiện|tính năng đang phát triển")
    ctx.add("A8.no-demo-placeholder", "A", "Không còn tính năng ở trạng thái Demo/chưa dùng được", "WARN" if demo_hits else "PASS",
            "; ".join(f"{rel(ctx.root, f)}:{ln}" for f, ln, _ in demo_hits[:5]))


# ---------------------------------------------------------------------------
# Nhóm C — Lỗi kỹ thuật (dev/build/runtime)
# ---------------------------------------------------------------------------

def check_group_c(ctx: Ctx):
    # C — no http:// or bare-IP API calls
    insecure = grep(ctx.src_files, r"(fetch|axios(?:\.\w+)?)\(\s*[\"'`]http://")
    ip_calls = grep(ctx.src_files, r"(fetch|axios(?:\.\w+)?)\(\s*[\"'`]https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    bad = insecure + ip_calls
    ctx.add("C.https-only", "C", "Mọi API call dùng https:// domain, không IP trần", "FAIL" if bad else "PASS",
            "; ".join(f"{rel(ctx.root, f)}:{ln}" for f, ln, _ in bad[:8]))

    # C — image asset via public-path string instead of ES import
    public_img = grep(ctx.src_files, r"""src\s*=\s*["'`]/[^"'`]+\.(png|jpe?g|gif|svg|webp)["'`]""")
    ctx.add("C.image-es-import", "C", "Ảnh dùng ES import, không path string trỏ public/", "WARN" if public_img else "PASS",
            "; ".join(f"{rel(ctx.root, f)}:{ln}" for f, ln, _ in public_img[:8]))

    # C — hardcoded secrets in client bundle
    secret_hits = grep(
        ctx.src_files,
        r"""(app_secret|appSecret|private_key|privateKey|refresh_token|refreshToken)\s*[:=]\s*["'`][A-Za-z0-9_\-]{12,}["'`]""",
    )
    ctx.add("C.no-hardcoded-secrets", "C", "Không hardcode app secret/private key/token trong client bundle",
            "FAIL" if secret_hits else "PASS",
            "; ".join(f"{rel(ctx.root, f)}:{ln}" for f, ln, _ in secret_hits[:8]))

    # C — server-to-server API called directly from client
    s2s_hits = grep(
        ctx.src_files,
        r"graph\.zalo\.me|openapi\.zalo\.me.*(sendMessage|getOrderStatus|updateOrderStatus)",
    )
    ctx.add("C.no-client-s2s-calls", "C", "Không gọi trực tiếp API Server-to-Server từ client", "FAIL" if s2s_hits else "PASS",
            "; ".join(f"{rel(ctx.root, f)}:{ln}" for f, ln, _ in s2s_hits[:8]))

    # C — app-config.json exists with app.title
    if ctx.app_config_path is None:
        ctx.add("C.app-config-exists", "C", "app-config.json ở root, có app.title", "FAIL", "không tìm thấy app-config.json ở root")
    else:
        ok = bool((ctx.app_config or {}).get("app", {}).get("title"))
        ctx.add("C.app-config-exists", "C", "app-config.json ở root, có app.title",
                "PASS" if ok else "FAIL", rel(ctx.root, ctx.app_config_path))

    # C — selfControlLoading requires closeLoading()
    cfg = ctx.app_config or {}
    if cfg.get("app", {}).get("selfControlLoading") or cfg.get("selfControlLoading"):
        has_close = bool(grep(ctx.src_files, r"closeLoading\s*\("))
        ctx.add("C.self-control-loading-closes", "C", "selfControlLoading=true phải gọi closeLoading()",
                "PASS" if has_close else "FAIL", "" if has_close else "flag bật nhưng không tìm thấy lời gọi closeLoading()")
    else:
        ctx.add("C.self-control-loading-closes", "C", "selfControlLoading=true phải gọi closeLoading()", "SKIP",
                "selfControlLoading không bật")

    # C — CI/CD ZMP_TOKEN not clobbered by runner-level env with same name
    workflows = list((ctx.root / ".github" / "workflows").glob("*.yml")) if (ctx.root / ".github" / "workflows").exists() else []
    zmp_token_hits = grep(workflows, r"ZMP_TOKEN")
    ctx.add("C.ci-zmp-token", "C", "ZMP_TOKEN trong .env không bị ghi đè bởi CI runner env",
            "WARN" if zmp_token_hits else "SKIP",
            "; ".join(f"{rel(ctx.root, f)}:{ln}" for f, ln, _ in zmp_token_hits[:5]) or "không có GitHub Actions workflow để kiểm tra")

    # C — bundle size limits (needs a real build output dir)
    if ctx.build_dir and ctx.build_dir.exists():
        total = 0
        oversized = []
        for f in ctx.build_dir.rglob("*"):
            if f.is_file():
                size = f.stat().st_size
                total += size
                if size > 3 * 1024 * 1024:
                    oversized.append((f, size))
        total_mb = total / (1024 * 1024)
        ctx.add("C.bundle-total-10mb", "C", "Tổng dung lượng build ≤ 10MB",
                "FAIL" if total_mb > 10 else "PASS", f"{total_mb:.2f}MB tại {ctx.build_dir}")
        ctx.add("C.bundle-per-file-3mb", "C", "Mỗi file build ≤ 3MB",
                "FAIL" if oversized else "PASS",
                "; ".join(f"{rel(ctx.root, f)} ({s/1024/1024:.2f}MB)" for f, s in oversized[:8]))
    else:
        ctx.add("C.bundle-total-10mb", "C", "Tổng dung lượng build ≤ 10MB", "SKIP",
                "chạy `zmp build`/`vite build` rồi truyền --build-dir để kiểm tra")
        ctx.add("C.bundle-per-file-3mb", "C", "Mỗi file build ≤ 3MB", "SKIP", "cần --build-dir")


# ---------------------------------------------------------------------------
# Nhóm D — UI/UX, điều hướng
# ---------------------------------------------------------------------------

def check_group_d(ctx: Ctx):
    cfg = ctx.app_config or {}
    tabs = None
    app = cfg.get("app", {}) if isinstance(cfg, dict) else {}
    for key in ("bottomNavigation", "tabBar", "navigateBottom"):
        val = app.get(key) or cfg.get(key)
        if isinstance(val, list):
            tabs = val
            break
    if tabs is not None:
        ctx.add("D1.max-4-tabs", "D", "Bottom navigation không quá 4 tab", "FAIL" if len(tabs) > 4 else "PASS",
                f"{len(tabs)} tab")
    else:
        ctx.add("D1.max-4-tabs", "D", "Bottom navigation không quá 4 tab", "SKIP",
                "không tìm thấy cấu hình bottom nav trong app-config.json (có thể định nghĩa qua router thay vì config)")

    # D4 — getPhoneNumber not called unconditionally on first mount (heuristic:
    # call appears inside a useEffect with an empty/no dependency array AND no
    # surrounding onClick — flagged for human confirmation, never auto-PASS).
    phone_hits = grep(ctx.src_files, r"getPhoneNumber\s*\(")
    if phone_hits:
        ctx.add("D4.phone-not-on-mount", "D", "getPhoneNumber không gọi ngay khi vào app", "WARN",
                "; ".join(f"{rel(ctx.root, f)}:{ln}" for f, ln, _ in phone_hits[:8]) +
                " — xác nhận thủ công lời gọi nằm trong handler user action, không trong useEffect mount vô điều kiện")
    else:
        ctx.add("D4.phone-not-on-mount", "D", "getPhoneNumber không gọi ngay khi vào app", "SKIP", "app không dùng getPhoneNumber")


# ---------------------------------------------------------------------------
# Nhóm E — Quy trình nộp duyệt & khai báo quyền
# ---------------------------------------------------------------------------

def check_group_e(ctx: Ctx):
    dotenv = ctx.root / ".env"
    ids_in_src = set(m for _, _, line in grep(ctx.src_files, r"appId\s*[:=]\s*[\"'`]([\w-]+)[\"'`]")
                      for m in re.findall(r"appId\s*[:=]\s*[\"'`]([\w-]+)[\"'`]", line, re.IGNORECASE))
    hardcoded = grep(ctx.src_files, r"""appId\s*[:=]\s*["'`][\w-]{6,}["'`]""")
    ctx.add("E1.no-hardcoded-app-id", "E", "Mini App chỉ gọi Open API qua đúng Ứng dụng cha (không hardcode appId)",
            "WARN" if hardcoded else "PASS",
            "; ".join(f"{rel(ctx.root, f)}:{ln}" for f, ln, _ in hardcoded[:8]))

    # E5 — Partner API usage present for CI automation (informational, not a gate)
    partner_api_hits = grep(ctx.src_files + list((ctx.root / ".github").rglob("*")) if (ctx.root / ".github").exists() else ctx.src_files,
                             r"getAppPermissions|requestAppPermission|requestPublishMiniApp|publishMiniApp")
    ctx.add("E5.partner-api-automation", "E", "Dùng Partner API tự động hoá khai báo quyền/publish (tuỳ chọn)",
            "PASS" if partner_api_hits else "SKIP",
            "; ".join(f"{rel(ctx.root, f)}:{ln}" for f, ln, _ in partner_api_hits[:5]) or "không dùng — vẫn hợp lệ nếu làm thủ công qua Mini App Center")


def build_report(ctx: Ctx) -> str:
    lines = ["# Zalo Mini App — Static Checklist Scan\n"]
    lines.append(f"Project: `{ctx.root}`\n")
    by_group: dict[str, list[Result]] = {}
    for r in ctx.results:
        by_group.setdefault(r.group, []).append(r)

    counts = {"PASS": 0, "FAIL": 0, "WARN": 0, "SKIP": 0}
    for r in ctx.results:
        counts[r.status] += 1
    lines.append(f"**Tổng: {len(ctx.results)} mục** — "
                 f"PASS {counts['PASS']} / FAIL {counts['FAIL']} / WARN {counts['WARN']} / SKIP {counts['SKIP']}\n")

    for group in sorted(by_group):
        lines.append(f"\n## Nhóm {group}\n")
        for r in sorted(by_group[group], key=lambda r: STATUS_ORDER[r.status]):
            icon = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "SKIP": "⏭️"}[r.status]
            lines.append(f"- {icon} **[{r.status}]** `{r.check_id}` — {r.title}"
                         + (f"\n  - Evidence: {r.evidence}" if r.evidence else ""))
    lines.append("\n---\n_Đây chỉ là các mục `Automatable: yes/partial` kiểm tra được bằng static scan. "
                 "Các mục còn lại (nội dung, pháp lý, dynamic/runtime) xem `checklist.md` Nhóm B/F và "
                 "phần dynamic-only trong Nhóm A/D — cần review thủ công hoặc browser/real-device test "
                 "(xem `TESTING.md`)._")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project_root", type=Path, help="Root của dự án Zalo Mini App cần scan")
    ap.add_argument("--build-dir", type=Path, default=None,
                    help="Thư mục build output (vd dist/ hoặc www/) để kiểm tra size limit")
    ap.add_argument("--json", action="store_true", help="In thêm kết quả dạng JSON ra stderr (cho tool khác parse)")
    args = ap.parse_args()

    root = args.project_root.resolve()
    if not root.exists():
        print(f"error: {root} không tồn tại", file=sys.stderr)
        sys.exit(2)

    app_config_path = root / "app-config.json"
    ctx = Ctx(
        root=root,
        build_dir=(root / args.build_dir).resolve() if args.build_dir else None,
        src_files=collect_src_files(root),
        app_config=load_json(app_config_path) if app_config_path.exists() else None,
        app_config_path=app_config_path if app_config_path.exists() else None,
        package_json=load_json(root / "package.json") if (root / "package.json").exists() else None,
    )

    check_group_a(ctx)
    check_group_c(ctx)
    check_group_d(ctx)
    check_group_e(ctx)

    print(build_report(ctx))

    if args.json:
        print(json.dumps([r.__dict__ for r in ctx.results], ensure_ascii=False, indent=2), file=sys.stderr)

    sys.exit(1 if any(r.status == "FAIL" for r in ctx.results) else 0)


if __name__ == "__main__":
    main()
