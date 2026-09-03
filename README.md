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
| [`sync.sh`](./sync.sh) | Script team dùng để kéo bản mới nhất từ GitHub về `~/.omp/agent/managed-skills/zalo-pre-submit-review/` local — chạy lại được nhiều lần, tự báo nếu đã ở bản mới nhất. |

## 6 nhóm checklist

- **A** — Chính sách nội dung & kiểm duyệt (53 mục)
- **B** — Pháp lý: KYB/eKYC, giấy phép ngành nghề có điều kiện, Nghị định 13 (58 mục)
- **C** — Lỗi kỹ thuật dev/build/runtime (24 mục)
- **D** — UI/UX, điều hướng, xác thực người dùng (23 mục)
- **E** — Quy trình nộp duyệt & khai báo quyền (55 mục)
- **F** — Bổ sung (4 mục)

92 mục agent tự kiểm 100% được (`yes`), 75 mục agent chỉ cảnh báo (`partial`), 50 mục thuần thủ công/pháp lý (`no`) — xem bảng thống kê đầu `checklist.md`.

## Hướng dẫn sử dụng (HDSD)

### Yêu cầu môi trường
- Git + Bash để chạy `sync.sh`. Trên **Windows dùng Git Bash** (đi kèm Git for Windows) — không chạy `sync.sh` bằng CMD/PowerShell thuần.
- Python 3 (chỉ cần nếu muốn tự chạy `check_updates.py`).
- Một AI agent hỗ trợ managed skills (Claude Code / omp / ckit) — skill này không phải app chạy độc lập, nó là tài liệu + checklist để agent đọc và tự thực hiện review khi làm việc trên dự án Zalo Mini App.

### Bước 1 — Cài lần đầu
Chạy trong Git Bash (Windows) hoặc terminal (Mac/Linux):
```bash
curl -fsSL https://raw.githubusercontent.com/nguyenba16/zalo-pre-submit-review-skills/main/sync.sh | bash
```
Lệnh này tự clone repo về cache (`~/.cache/zalo-pre-submit-review-skills`) và copy 6 file runtime vào `~/.omp/agent/managed-skills/zalo-pre-submit-review/`. Sau bước này agent sẽ tự nhận diện skill ở phiên làm việc tiếp theo — không cần cấu hình thêm.

### Bước 2 — Chạy pre-submit review trên một dự án Mini App
Mở agent (Claude Code/omp/ckit) tại thư mục dự án Zalo Mini App, yêu cầu kiểu: *"chạy pre-submit review theo skill zalo-pre-submit-review trước khi nộp duyệt"*. Agent sẽ tự đọc `SKILL.md` để biết quy trình (đọc checklist 1 lần → tóm tắt cấu trúc dự án → dispatch song song các nhóm A/C/D/E tự kiểm được → tổng hợp báo cáo PASS/FAIL/WARN kèm bằng chứng `file:line`). Nhóm B/F (pháp lý) không tự kiểm bằng code — agent liệt kê thành checklist thủ công cho người phụ trách, không tự kết luận đạt/không đạt.

**Đọc kỹ trước khi trình bày kết quả với khách hàng**: mục "Trạng thái" (đầu file này) và "Giới hạn quan trọng" (cuối file này) — đây là bản nháp, chưa qua review pháp lý cho Nhóm B.

### Bước 3 — Cập nhật khi repo có thay đổi (mỗi thành viên team tự chạy trên máy mình)
Repo GitHub là nguồn duy nhất (single source of truth); bản trong `~/.omp/agent/managed-skills/` chỉ là bản copy cục bộ, KHÔNG tự đồng bộ. Sau khi có PR merge vào `main`, mỗi người trong team chạy lại đúng lệnh ở Bước 1:
```bash
curl -fsSL https://raw.githubusercontent.com/nguyenba16/zalo-pre-submit-review-skills/main/sync.sh | bash
# hoặc nếu đã clone repo sẵn: bash sync.sh
```
Script so sánh commit SHA cũ/mới: nếu chưa đổi gì → báo "đã ở bản mới nhất" và dừng, không ghi đè (an toàn chạy lại nhiều lần/nhiều máy). Nếu có đổi → copy đè `SKILL.md`, `checklist.md`, `checklist.docx`, `sources.json`, `check_updates.py`, `requirements.txt`, `CHANGELOG.md`, và in ra SHA cũ→mới + log các commit đổi nội dung checklist/skill để biết đổi gì.

Không có push-notify tự động — team phải chủ động chạy lệnh trên (hoặc tự đặt lịch cron/Task Scheduler chạy `sync.sh` định kỳ). Đây là cơ chế đồng bộ **nội dung repo này**, khác với `check_updates.py` ở Bước 4 (phát hiện khi **Zalo** đổi tài liệu gốc — nguồn ngoài repo).

### Bước 4 — Kiểm tra checklist còn khớp tài liệu Zalo không
```bash
cd ~/.omp/agent/managed-skills/zalo-pre-submit-review   # hoặc thư mục repo đã clone
pip install -r requirements.txt   # 1 lần
python3 check_updates.py
```
Chạy định kỳ (khuyến nghị hàng tháng, hoặc bắt buộc trước khi dùng cho dự án/khách hàng mới). Script fetch lại 27 trang tài liệu gốc, so hash với baseline trong `sources.json`, báo trang nào đã đổi nội dung. Script **không tự sửa `checklist.md`** — chỉ báo hiệu cần đọc lại trang đó; quy trình cập nhật sau khi phát hiện đổi nằm ở mục "Cơ chế phản hồi & cập nhật" trong [`SKILL.md`](./SKILL.md).

### Bước 5 — Báo lỗi / đề xuất sửa nội dung checklist
Mở [Issue](https://github.com/nguyenba16/zalo-pre-submit-review-skills/issues) mới, kèm: mục checklist bị sai (dòng "— Nguồn: ..." của mục đó, dùng làm ID), bằng chứng (screenshot/link trang Zalo hiện tại, hoặc log cho thấy checklist báo sai khi chạy trên project thật), đề xuất sửa nếu có. Chi tiết quy trình đầy đủ ở mục "Cơ chế phản hồi & cập nhật" trong `SKILL.md`.

## Giới hạn quan trọng

Đây là **pre-flight QA hỗ trợ nội bộ**, KHÔNG thay thế đội kiểm duyệt của Zalo — Zalo vẫn có quyết định cuối cùng. Nội dung pháp lý (Nhóm B) chưa được người có chuyên môn pháp lý review — dùng để tham khảo, không dùng làm căn cứ pháp lý chính thức.
