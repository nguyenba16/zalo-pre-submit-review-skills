# skill-claude — Bộ skill AI-agent hỗ trợ QA Zalo Mini App

> Tài liệu tổng hợp để trình bày/chia sẻ nội bộ công ty.
> Trạng thái: **bản nháp — chưa qua review thủ công, chưa test trên project thật của công ty.** Đọc kỹ mục "Giới hạn & rủi ro đã biết" trước khi cam kết dùng cho khách hàng.

---

## 1. Vấn đề

Team làm Zalo Mini App đang đối mặt 2 việc lặp lại tốn thời gian, dễ sai sót nếu làm thủ công:

1. **Trước khi nộp Zalo xét duyệt** — mỗi vòng duyệt mất **3–7 ngày làm việc**. Bị từ chối vì 1 lỗi nhỏ (thiếu khai báo quyền, tên app sai quy định, quên giấy phép ngành nghề...) nghĩa là mất thêm 1 vòng 3-7 ngày nữa. Checklist chính thức của Zalo dài, rải rác nhiều trang tài liệu, dễ bỏ sót.
2. **Đối chiếu bản build với thiết kế/nghiệp vụ** — BA giao mockup Figma + file `.md` mô tả logic, dev code xong nhưng không có bước kiểm tra có hệ thống xem UI có khớp Figma, logic có khớp mô tả BA hay không trước khi đưa QA.

Cả 2 việc đều **làm được bằng AI agent có công cụ phù hợp** (đọc tài liệu, chạy trình duyệt, so sánh ảnh, đọc code) — mục tiêu của bộ skill này là đóng gói quy trình đó thành thứ **dùng lại được trên mọi project**, không phải làm tay lại từ đầu mỗi lần.

## 2. Giải pháp — 2 skill

| Skill | Dùng khi nào | Input cần có |
|---|---|---|
| **`zalo-pre-submit-review`** | Trước khi bấm "Gửi xét duyệt" 1 Zalo Mini App (mới hoặc bản cập nhật) | Chỉ cần source code project |
| **`figma-logic-conformance-test`** | Sau khi dev code xong, trước khi đưa QA — kiểm UI khớp Figma + logic khớp mô tả BA | File Figma (key + token), file `logic.md` của BA, app chạy được, bảng ánh xạ frame↔route |

Cả 2 đóng gói theo chuẩn **Agent Skills** (`SKILL.md` + script + tài liệu đi kèm) — bất kỳ AI agent nào hỗ trợ managed skills (Claude Code, omp, ckit...) đọc vào là tự biết cách chạy, không cần hướng dẫn lại từ đầu mỗi lần dùng.

### 2.1 `zalo-pre-submit-review` hoạt động thế nào

- Checklist đầy đủ **217 mục**, chia 6 nhóm (A–F: chính sách nội dung, pháp lý, kỹ thuật, UI/UX, khai báo quyền, quy trình nộp), mỗi mục có nguồn (URL#anchor tài liệu chính thức Zalo) + hậu quả nếu vi phạm.
- Thống kê mức tự động hoá: **~42% agent tự quyết được** (`Automatable: yes`), **~35% agent chỉ cảnh báo** (`partial`), **~23% thuần thủ công/pháp lý** (`no`) — dùng để ước lượng effort trước khi cam kết thời gian review với khách hàng.
- `scripts/scan_static_checklist.py` — scanner tất định (regex/JSON, **không dùng LLM phán đoán**) cho các mục có thể kiểm bằng static scan (tên app viết hoa toàn bộ, link trong mô tả, SDK đăng nhập bên thứ 3, gọi `http://` thay vì `https://`...) — kết quả PASS/FAIL/WARN/SKIP lặp lại y hệt mỗi lần chạy, dùng được làm CI gate.
- `TESTING.md` — playbook 2 tầng test: browser-preview (Playwright, tự động hoá được) + real-device (QR scan vào Zalo app thật, GIF/video bằng chứng cho các flow chỉ chạy được trên thiết bị thật như login).

### 2.2 `figma-logic-conformance-test` hoạt động thế nào

- **Lane A (UI đối chiếu Figma)**: gọi Figma REST API xuất ảnh từng frame, dùng `browser` tool chụp app thật ở cùng route, so sánh 2 ảnh bằng **vision model định tính** (không pixel-diff toán học — nội dung thật khác Lorem Ipsum sẽ luôn khác biệt, pixel-diff báo lỗi tràn lan vô nghĩa).
- **Lane B (Logic đối chiếu `.md`)**: `scripts/extract_logic_rules.py` tách rule nguyên tử từ file BA viết (bullet/số/Given-When-Then), agent tìm code liên quan qua `lsp`/`codegraph`/grep, đối chiếu công thức/điều kiện với mô tả.
- Cần 1 file `figma-route-map.json` ánh xạ tên frame Figma ↔ route trong app — **thủ công, không suy đoán tự động** (tên BA đặt và tên route dev đặt hiếm khi khớp chữ).

## 3. Cách phân phối & cài đặt (2 cách)

Repo GitHub công khai: `github.com/nguyenba16/zalo-pre-submit-review-skills` — nguồn duy nhất (single source of truth).

| | **Cách A — global (`sync.sh`)** | **Cách B — vendor project-local (`install-local.sh`)** |
|---|---|---|
| Cài vào đâu | `~/.omp/agent/managed-skills/` (dùng chung mọi project trên máy) | `<project>/.omp/skills/<skill>/` (đi theo git repo của chính project đó) |
| Phù hợp khi | Dùng skill trên nhiều project khác nhau, không cần biết trước sẽ làm project nào | Muốn ai clone project đó cũng có sẵn skill, không ai phải tự cài |
| Lệnh | `curl -fsSL .../sync.sh \| bash` | `bash install-local.sh <project> [skill-name]` rồi `git commit` |

## 4. Cơ chế cập nhật — làm sao biết khi có bản mới

**Vấn đề:** Cách B copy file tĩnh 1 lần, sau đó project đích không còn liên kết gì với repo gốc — không ai tự biết khi nào cần lấy bản mới.

**Giải pháp đã build:**
- Mỗi lần vendor, `install-local.sh` tự ghi `.vendor-meta.json` (commit gốc + thời điểm copy) vào từng skill.
- `check-local-updates.sh <project>` — đọc `.vendor-meta.json`, so với commit mới nhất trên GitHub, **chỉ báo lỗi thời khi có commit thật sự đổi đúng skill đó** (không báo nhiễu nếu người khác sửa skill khác không liên quan). Có xử lý lỗi mạng (timeout 20s, message rõ ràng nếu firewall/VPN chặn).
- Cách A: `sync.sh` tự so SHA cũ/mới mỗi lần chạy lại.
- Cả 2 đều **chủ động, không push-notify tự động** — khuyến nghị chạy định kỳ hàng tháng.

## 5. Cơ chế phản hồi/báo lỗi — 2 nguồn, cùng 1 kênh

1. **User tự phát hiện** — mở [GitHub Issue](https://github.com/nguyenba16/zalo-pre-submit-review-skills/issues/new/choose) bằng template có sẵn (chọn đúng skill, điền ID mục/rule sai, bằng chứng, đề xuất sửa — không cần tự nhớ format).
2. **Agent tự phát hiện trong lúc chạy thật** — nếu agent thấy checklist/scanner báo sai khi đang review 1 project thật:
   - Luôn **hỏi user xác nhận trước**, không tự ý mở Issue.
   - Tìm Issue trùng trước khi tạo mới (tránh spam trùng lặp).
   - **Không đính bằng chứng chứa dữ liệu thật của khách hàng** (repo này để public) — mô tả bằng văn bản trung tính thay vì screenshot/log gốc.
   - Tự gắn commit đang vendor để dev dễ tra bug thuộc bản nào.
3. Fix được duyệt qua Pull Request vào `main`, các project khác nhận qua vòng lặp cập nhật ở mục 4.

## 6. Khi Zalo đổi chính sách chính thức

`check_updates.py` lưu content-hash của 27 trang tài liệu gốc Zalo (baseline). Chạy định kỳ (khuyến nghị hàng tháng) → tự fetch lại, báo trang nào đã đổi nội dung → người/agent đọc lại, sửa đúng mục trong `checklist.md`, ghi `CHANGELOG.md`, cập nhật hash baseline.

## 7. Giới hạn & rủi ro đã biết (thẳng thắn, không giấu)

- **Chưa test trên project thật của công ty** — mới verify bằng fixture giả lập. Bắt buộc pilot trên 1 project thật trước khi dùng cho khách hàng/release chính thức.
- **Repo GitHub để công khai (public)** — quyết định đã chốt giữ nguyên; rủi ro bù lại bằng quy tắc "không tự đính bằng chứng nhạy cảm" ở cơ chế agent tự-report, nhưng vẫn cần con người cẩn trọng khi tự tay report qua GitHub UI.
- **`check_updates.py` chỉ theo dõi 27 URL đã biết** — nếu Zalo ra hẳn 1 trang chính sách mới ngoài danh sách này, script không tự phát hiện được (chưa xử lý — mở nếu cần bổ sung).
- **Nhóm B (pháp lý) — 58 mục — chưa có ai chuyên môn pháp lý review.** Dùng để tham khảo, không dùng làm căn cứ pháp lý chính thức.
- **Không có branch protection trên `main`** — quy tắc "sửa phải qua PR" hiện là quy ước bằng văn bản, GitHub chưa enforce kỹ thuật.
- **So sánh UI bằng vision model là định tính**, không pixel-perfect — không bắt được sai lệch 1-2px, chỉ bắt sai lệch rõ ràng.
- **Mapping frame↔route (`figma-route-map.json`) là thủ công** — sai mapping tạo FAIL giả, phải xác nhận lại mỗi khi BA thêm màn hình mới.

## 8. Đề xuất bước tiếp theo

1. Chạy pilot thật: 1 project dùng `zalo-pre-submit-review` (đã có checklist + scanner hoàn chỉnh) trước, thu thập false positive/negative thật để vá.
2. Chuẩn bị 1 cặp Figma file + `logic.md` thật để verify `figma-logic-conformance-test` bằng dữ liệu công ty thay vì fixture giả lập.
3. Không share kết quả với khách hàng như "đã qua kiểm duyệt chắc chắn" — đây là công cụ hỗ trợ nội bộ, Zalo vẫn có quyết định cuối cùng.
