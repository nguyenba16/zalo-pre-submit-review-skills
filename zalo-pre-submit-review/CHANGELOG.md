# Changelog — zalo-pre-submit-review

Ghi lại mọi thay đổi nội dung checklist (không ghi log hash-only từ check_updates.py --update trừ khi kèm sửa nội dung thật).

## [1.2.0] — 2026-09-23
- Repo restructure: chuyển từ layout 1-skill-per-repo sang **monorepo nhiều skill** (`skill-claude`) — mọi file của skill này (SKILL.md, checklist.md/.docx, TESTING.md, scripts/, sources.json, check_updates.py, requirements.txt, file CHANGELOG này) chuyển vào thư mục con `zalo-pre-submit-review/` (dùng `git mv`, giữ lịch sử). Thêm skill thứ 2 `figma-logic-conformance-test/` cùng repo.
- `sync.sh` viết lại thành generic: tự phát hiện MỌI thư mục con có `SKILL.md` và đồng bộ tất cả vào `~/.omp/agent/managed-skills/<tên-skill>/` — không còn danh sách file cứng riêng cho skill này. Đã test end-to-end (fresh install + idempotency) bằng git remote/target tạm, không đụng GitHub thật/máy thật.
- Env var override đổi tên: `ZPSR_CLONE_DIR`/`ZPSR_TARGET_DIR` → `SKILLS_CLONE_DIR`/`SKILLS_TARGET_ROOT` (phạm vi rộng hơn, không còn riêng cho 1 skill).

## [1.1.0] — 2026-09-23
- Thêm `scripts/scan_static_checklist.py`: scanner tất định (regex/JSON, không LLM) cho tập con cơ học nhất của các mục `Automatable: yes` (Nhóm A/C/D/E — tên/logo/URL/secret/size/config), output PASS/FAIL/WARN/SKIP + evidence `file:line`, exit code 1 nếu FAIL (CI-gate được). Đã smoke-test trên project fixture tổng hợp (all-caps name, link trong mô tả, đăng nhập Google, `http://` literal) — đúng như kỳ vọng.
- Thêm `TESTING.md`: playbook 2 tầng test (browser-preview Playwright tự động hoá + real-device thủ công có GIF bằng chứng), trỏ tới 3 managed skill test chuyên biệt sẵn có (`zalo-mini-app-browser-testing`, `zalo-miniapp-real-device-gif-capture`, `mobile-device-test-record-gif`) thay vì trùng lặp nội dung setup của chúng.
- Cập nhật `SKILL.md`: thêm bước 0 "chạy scanner trước" và bước 6 "testing 2 tầng khi cần xác nhận app chạy đúng" vào quy trình chuẩn; mở rộng mô tả frontmatter cho đúng phạm vi mới.
- Cập nhật `sync.sh` (`RUNTIME_FILES`/`RUNTIME_DIRS`) và `requirements.txt` (thêm `Pillow` tuỳ chọn) để đồng bộ 2 artefact mới về managed-skills.
- **Chưa qua review pháp lý/manual test trên project thật** — scanner chỉ được smoke-test trên fixture tổng hợp, chưa chạy trên Mini App production thật của công ty.

## [1.0.0] — 2026-09-03
- Khởi tạo checklist 217 mục, 6 nhóm (A–F), tổng hợp từ 27 trang tài liệu chính thức mini.zalo.me / docs.zaloplatforms.com.
- Tạo `sources.json` baseline (content hash của 27 trang nguồn tại thời điểm 2026-09-03) + `check_updates.py` để phát hiện khi Zalo đổi tài liệu.
- **Trạng thái: BẢN NHÁP — chưa qua review thủ công, chưa chạy test trên project thật.** Xem "Giới hạn hiện tại" trong SKILL.md trước khi dùng cho khách hàng/team.

<!--
Template cho lần cập nhật tiếp theo:

## [Unreleased]
- Người sửa: <tên>
- Ngày: <yyyy-mm-dd>
- Lý do: <check_updates.py báo trang X đổi | người dùng báo mục Y sai | Zalo ra chính sách mới>
- Thay đổi: <mục nào trong checklist.md bị sửa, tóm tắt 1 dòng>
- Đã chạy `check_updates.py --update` sau khi đối chiếu: có/không
-->
