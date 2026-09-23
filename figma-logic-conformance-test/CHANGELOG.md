# Changelog — figma-logic-conformance-test

## [1.0.0] — 2026-09-23
- Khởi tạo skill: Lane A (UI vs Figma mockup, qua `scripts/export_figma_frames.py` + vision-model so sánh định tính) + Lane B (logic vs `logic.md` BA cung cấp, qua `scripts/extract_logic_rules.py` + subagent dispatch đối chiếu code).
- 2 script đã smoke-test bằng fixture giả lập (cây document Figma giả, file `.md` structured/prose mẫu) — **chưa chạy trên Figma file/logic.md thật của công ty**.
- **Trạng thái: BẢN NHÁP** — chưa có ai dùng trên project thật, mapping frame↔route và ngưỡng `structured_ratio` (0.5) chưa được hiệu chỉnh bằng dữ liệu thật.
