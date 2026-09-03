# zalo-pre-submit-review

AI-agent skill (Claude/omp managed skill format) + checklist tài liệu để chạy pre-flight QA trên một Zalo Mini App **trước khi nộp xét duyệt** — bắt trước các lỗi khiến hồ sơ bị Zalo từ chối/chậm duyệt (mỗi vòng duyệt mất 3–7 ngày làm việc).

## Trạng thái

⚠️ **Bản nháp — chưa qua review thủ công, chưa test trên project thật.** Xem mục "Giới hạn" trong [`SKILL.md`](./SKILL.md) trước khi dùng cho khách hàng/dự án thật. Đóng góp/report lỗi qua [Issues](https://github.com/nguyenba16/zalo-pre-submit-review-skills/issues).

## Nội dung repo

| File | Mô tả |
|---|---|
| [`SKILL.md`](./SKILL.md) | Hướng dẫn dùng skill cho AI agent (khi nào dùng, cách chạy pre-submit review tối ưu token, cơ chế phản hồi/cập nhật, giới hạn). |
| [`checklist.md`](./checklist.md) | Checklist đầy đủ **217 mục**, chia 6 nhóm A–F, mỗi mục có nguồn (URL#anchor tài liệu chính thức Zalo) + hậu quả nếu vi phạm + nhãn `Automatable: yes/partial/no`. |
| [`checklist.docx`](./checklist.docx) | Bản Word cùng nội dung, dùng cho người phụ trách nội dung/pháp lý không quen Markdown. |
| [`sources.json`](./sources.json) | Baseline content-hash của 27 trang tài liệu gốc mini.zalo.me/docs.zaloplatforms.com — dùng để phát hiện khi Zalo đổi tài liệu. |
| [`check_updates.py`](./check_updates.py) | Script kiểm tra staleness: fetch lại 27 URL nguồn, so hash với baseline, báo cáo trang nào đã đổi. |
| [`CHANGELOG.md`](./CHANGELOG.md) | Lịch sử thay đổi nội dung checklist. |
| [`requirements.txt`](./requirements.txt) | Dependency cho `check_updates.py`. |

## 6 nhóm checklist

- **A** — Chính sách nội dung & kiểm duyệt (53 mục)
- **B** — Pháp lý: KYB/eKYC, giấy phép ngành nghề có điều kiện, Nghị định 13 (58 mục)
- **C** — Lỗi kỹ thuật dev/build/runtime (24 mục)
- **D** — UI/UX, điều hướng, xác thực người dùng (23 mục)
- **E** — Quy trình nộp duyệt & khai báo quyền (55 mục)
- **F** — Bổ sung (4 mục)

92 mục agent tự kiểm 100% được (`yes`), 75 mục agent chỉ cảnh báo (`partial`), 50 mục thuần thủ công/pháp lý (`no`) — xem bảng thống kê đầu `checklist.md`.

## Cách dùng

### Với AI agent hỗ trợ managed skills (Claude Code / omp / ckit)
Copy `SKILL.md` + các file đi kèm vào thư mục managed-skills của agent (vd `~/.omp/agent/managed-skills/zalo-pre-submit-review/`), agent sẽ tự nạp và biết cách dùng khi làm việc trên dự án Zalo Mini App.

### Kiểm tra checklist còn khớp tài liệu Zalo không
```bash
pip install -r requirements.txt
python3 check_updates.py
```

### Báo lỗi / đề xuất sửa
Mở [Issue](https://github.com/nguyenba16/zalo-pre-submit-review-skills/issues) mới, kèm: mục checklist bị sai (dòng "— Nguồn: ..."), bằng chứng, đề xuất sửa. Chi tiết quy trình đầy đủ ở mục "Cơ chế phản hồi & cập nhật" trong `SKILL.md`.

## Giới hạn quan trọng

Đây là **pre-flight QA hỗ trợ nội bộ**, KHÔNG thay thế đội kiểm duyệt của Zalo — Zalo vẫn có quyết định cuối cùng. Nội dung pháp lý (Nhóm B) chưa được người có chuyên môn pháp lý review — dùng để tham khảo, không dùng làm căn cứ pháp lý chính thức.
