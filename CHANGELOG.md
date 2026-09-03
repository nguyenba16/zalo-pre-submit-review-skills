# Changelog — zalo-pre-submit-review

Ghi lại mọi thay đổi nội dung checklist (không ghi log hash-only từ check_updates.py --update trừ khi kèm sửa nội dung thật).

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
