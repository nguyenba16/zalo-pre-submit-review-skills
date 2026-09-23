# Zalo Mini App — Testing Playbook (bổ sung cho `zalo-pre-submit-review`)

> Bổ sung tháng 2026-09: skill này ban đầu chỉ trả lời "hồ sơ có vi phạm chính sách kiểm duyệt không" (đọc tài liệu + scan code tĩnh). File này thêm câu hỏi thứ hai bắt buộc phải trả lời TRƯỚC khi trả lời câu hỏi thứ nhất: **"app có thực sự chạy đúng không"** — vì nhiều mục compliance (A8 hiệu suất, C runtime, D UI/UX, E2 "đã test qua Hot Reload trên Zalo thật") chỉ xác nhận được bằng cách CHẠY app, không đọc source.

## Hai tầng test — không được gộp lẫn

| Tầng | Môi trường | Cái gì kiểm được | Cái gì KHÔNG kiểm được |
|---|---|---|---|
| **1. Browser-preview** | `zmp start` / `npm run dev`, Playwright chạy chromium | Routing, render trang, form, business logic, ảnh vỡ, console error, Lighthouse (LCP/PageLoad — mục A8), splash/loading state (D2) | Đăng nhập Zalo thật, bất kỳ API zmp-sdk native nào (`getPhoneNumber`, `getLocation`, `getUserInfo`, Checkout SDK thật) — `zmp-sdk/browser.min.js` chỉ là stub, KHÔNG BAO GIỜ trả dữ liệu thật dù chạy Playwright hay real-device cloud grid (BrowserStack/Sauce Labs) vì các dịch vụ đó vẫn lái Safari/Chrome, không phải webview Zalo thật |
| **2. Real-device (Zalo thật)** | Quét QR từ `zmp start` bằng app Zalo thật trên điện thoại (Development) hoặc bản Testing trên Mini App Center | Login flow chuẩn (D4), mọi API native, xin quyền runtime thật (A5/E3), Checkout SDK thật, hiệu năng trên thiết bị thật | Không automate được — Zalo webview không expose remote-debugging protocol công khai cho CI |

**Hệ quả trực tiếp cho checklist.md**: mọi mục có ghi "Automatable: partial/no" kèm lý do "cần Device Mode"/"cần Zalo thật" (vd C: `#5-api-được-gọi-thành-công-nhưng-không-có-dữ-liệu`, E2, E3, D4) chỉ có thể đóng dấu PASS sau khi chạy Tầng 2 — KHÔNG được suy luận PASS từ việc code "trông đúng" ở Tầng 1.

## Tầng 1 — Browser-preview (Playwright), tự động hoá đầy đủ

Setup và pattern chi tiết đã có sẵn ở managed skill **`zalo-mini-app-browser-testing`** (không lặp lại ở đây — đọc `skill://zalo-mini-app-browser-testing` khi cần setup Playwright/xử lý quirk `DemoWelcomeModal`/xác định đúng port dev server). Tóm tắt phần liên quan trực tiếp đến checklist compliance:

- Chạy Playwright crawl mọi route chính → bắt lỗi console/404/ảnh vỡ (checklist A8 "màn hình trắng"/"ảnh vỡ") thay vì tự crawl thủ công.
- Chạy Lighthouse CI (`npx lighthouse <url> --output=json`) trên các trang chính để đo LCP/PageLoad (A8: LCP<2.5s, PageLoad<1.5s) — script này KHÔNG có trong repo, thêm nếu team cần gate CI; nếu chỉ cần một lần thì `npx lighthouse` trực tiếp là đủ, không cần cài thêm gì vào skill.
- Test flow "từ chối quyền" (A5/B6): mock permission API trả về denied, xác nhận app không tự đóng và vẫn điều hướng được.
- Test flow ẩn danh (A5 "không bắt buộc đăng nhập"): vào thẳng route chính ở trạng thái chưa auth, xác nhận không bị redirect cứng.

## Tầng 2 — Real-device, xác nhận thủ công có ghi lại bằng chứng

Setup chi tiết theo platform (Android via `scrcpy`, iOS via QuickTime AirPlay) đã có ở hai managed skill **`zalo-miniapp-real-device-gif-capture`** và **`mobile-device-test-record-gif`** — đọc `skill://zalo-miniapp-real-device-gif-capture` khi cần chạy. Checklist item nào cần Tầng 2 để đóng dấu PASS:

- **D4** (luồng đăng nhập 3 bước chuẩn) — quan sát network tab thật qua remote debug (Safari Web Inspector cho iOS, `chrome://inspect` cho Android WebView) trong lúc chạy trên Zalo thật.
- **A5/E3** (popup xin quyền đúng ngữ cảnh, không giả mạo UI native) — chụp/quay lại đúng thời điểm popup hiện ra.
- **A7** (Checkout SDK) — thực hiện một giao dịch test thật, xác nhận UI thanh toán là UI chuẩn Zalo, không phải form tự vẽ.
- **E2** (đã test qua Hot Reload trên Zalo thật trước khi chuyển Testing) — bằng chứng là chính bản ghi màn hình.

**Sản phẩm đầu ra bắt buộc của Tầng 2 khi báo cáo cho khách hàng/công ty**: 1 GIF/video ngắn (~10-20s) mỗi flow quan trọng (login, xin quyền, checkout), theo quy trình convert trong hai skill trên (`ffmpeg -vf "fps=12,scale=360:-1:flags=lanczos"`). Đính kèm GIF vào báo cáo thay vì mô tả bằng lời — nhất quán với quy ước dự án dùng `ckit shot`/ảnh thay vì dump text khi trình bày kết quả.

## Quy trình tổng hợp: chạy Compliance + Testing cho một lần release

Khi được yêu cầu "review trước khi nộp duyệt" đầy đủ (không chỉ đọc code), chạy theo đúng thứ tự — mỗi bước phụ thuộc bước trước nên KHÔNG song song hoá bước với bước:

1. **Static scan (giây, xác định)**: `python3 scripts/scan_static_checklist.py <project_root> --build-dir dist` — xem "Chạy scanner" bên dưới. Loại ngay các FAIL cơ học (tên ALL CAPS, http:// literal, secret hardcode...) trước khi tốn công người/agent đọc code.
2. **Subagent dispatch cho phần "partial" còn lại** — giữ nguyên quy trình 4-subagent song song đã mô tả trong `SKILL.md` (Nhóm A/C/D/E), nhưng bỏ khỏi danh sách các mục đã có kết quả PASS/FAIL từ bước 1 để không quét trùng.
3. **Tầng 1 Playwright** (song song được với bước 2 vì độc lập môi trường): crawl route + Lighthouse + permission-denied flow.
4. **Tầng 2 real-device** (SAU bước 3, cần người cầm điện thoại): login flow, xin quyền, checkout — ghi lại GIF bằng chứng.
5. **Nhóm B/F pháp lý**: vẫn thuần thủ công như mô tả gốc trong `SKILL.md`.
6. **Tổng hợp báo cáo cuối** theo format đã có trong `SKILL.md`, bổ sung mục "Bằng chứng real-device" (link/đính kèm GIF từ bước 4).

## Chạy scanner

```bash
pip install -r requirements.txt   # thêm Pillow cho check alpha-channel logo (tuỳ chọn)
python3 scripts/scan_static_checklist.py /path/to/mini-app-project --build-dir dist
```

- Không có `--build-dir` → 2 mục size-limit (C.bundle-total-10mb/C.bundle-per-file-3mb) sẽ SKIP thay vì PASS giả — script không bao giờ PASS một mục nó chưa thực sự kiểm tra được.
- Exit code `1` nếu có FAIL bất kỳ — dùng được làm CI gate: `python3 scripts/scan_static_checklist.py . --build-dir dist || echo "có FAIL cần xử lý trước khi submit"`.
- Script chỉ phủ một tập con của các mục "Automatable: yes" (những mục mang tính cơ học nhất — tên/logo/URL/secret/size/config). KHÔNG thay thế bước 2 (subagent dispatch) cho phần còn lại của 92 mục `yes` + 75 mục `partial` — nhiều mục "yes" trong checklist gốc (vd D "đếm tab trong router" khi router không định nghĩa qua app-config, hay E1 "userId không dùng chung cross-app") cần đọc cấu trúc project cụ thể hơn một regex chung có thể làm an toàn — subagent dispatch vẫn xử lý các mục đó.

## Giới hạn của tầng testing này

- Tầng 2 (real-device) không thể tự động hoá — không có remote-debugging protocol công khai cho Zalo webview; đừng hứa với khách hàng "CI tự chạy được toàn bộ test".
- Scanner (bước 1) là heuristic dựa trên regex/JSON field, KHÔNG parse AST — có thể bỏ sót cách viết khác thường (vd string bị nối/escape, dynamic import ảnh qua biến). Coi FAIL/WARN của nó là gợi ý cần xác nhận, PASS là "không phát hiện vi phạm rõ ràng", không phải "chắc chắn đạt chuẩn".
- Lighthouse/CORS/dynamic API test (mục C có ghi "dynamic test") cần server thật đang chạy — chưa có script sẵn trong repo này, xem gợi ý lệnh `npx lighthouse` ở Tầng 1.
