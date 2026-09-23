# skill-claude — bộ skill AI-agent nội bộ công ty

Bộ skill (Claude Code/omp managed skill format) để clone 1 lần, đồng bộ tất cả bằng `sync.sh`, dùng chung cho cả team. Mỗi skill nằm trong 1 thư mục con ở root repo, tự chứa (SKILL.md + tài nguyên riêng) — thêm skill mới chỉ cần thêm 1 thư mục con, không phải sửa cơ chế đồng bộ.

## Danh sách skill

| Skill | Thư mục | Dùng khi nào |
|---|---|---|
| **zalo-pre-submit-review** | [`zalo-pre-submit-review/`](./zalo-pre-submit-review/) | Trước khi nộp xét duyệt 1 Zalo Mini App — pre-flight QA đối chiếu 217 mục chính sách kiểm duyệt/pháp lý/kỹ thuật Zalo, kèm scanner tự động + playbook test browser-preview & real-device. |
| **figma-logic-conformance-test** | [`figma-logic-conformance-test/`](./figma-logic-conformance-test/) | Khi BA giao Figma mockup + file `.md` logic nghiệp vụ cho dev — đối chiếu UI đã build với Figma (Lane A) và logic đã code với `.md` (Lane B). |

## Trạng thái

⚠️ **Cả 2 skill đều là bản nháp** — chưa qua review thủ công/pháp lý, chưa chạy trên project thật của công ty. Xem mục "Giới hạn quan trọng" trong `SKILL.md` của từng skill trước khi dùng cho khách hàng/dự án thật. Đóng góp/report lỗi qua [Issues](https://github.com/nguyenba16/zalo-pre-submit-review-skills/issues).

## Hướng dẫn sử dụng (HDSD)

### Yêu cầu môi trường
- Git + Bash để chạy `sync.sh`. Trên **Windows dùng Git Bash** (đi kèm Git for Windows) — không chạy `sync.sh` bằng CMD/PowerShell thuần.
- Python 3 + `pip install -r requirements.txt` bên trong từng thư mục skill (mỗi skill có `requirements.txt` riêng, dependency khác nhau).
- Một AI agent hỗ trợ managed skills (Claude Code / omp / ckit) — các skill này không phải app chạy độc lập, đó là tài liệu + script để agent đọc và tự thực hiện review/test.

### Bước 1 — Cài lần đầu (2 cách, chọn 1 theo nhu cầu)

**Cách A — cài global (`sync.sh`)**: dùng skill trên nhiều project khác nhau, không cần biết trước sẽ làm project nào.
```bash
curl -fsSL https://raw.githubusercontent.com/nguyenba16/zalo-pre-submit-review-skills/main/sync.sh | bash
```
Tự clone repo về cache (`~/.cache/zalo-pre-submit-review-skills`), tự phát hiện mọi thư mục con có `SKILL.md`, copy từng skill vào `~/.omp/agent/managed-skills/<tên-skill>/`. Cài 1 lần trên máy, dùng được cho MỌI project mở trên máy đó — nhưng riêng máy, người khác clone project không tự có skill.

**Cách B — vendor project-local (`install-local.sh`)**: gắn skill trực tiếp vào 1 project cụ thể, để ai clone project đó cũng có sẵn skill (không ai phải tự cài gì).
```bash
git clone https://github.com/nguyenba16/zalo-pre-submit-review-skills.git /tmp/skill-claude
bash /tmp/skill-claude/install-local.sh /đường/dẫn/project-đích           # copy tất cả skill
bash /tmp/skill-claude/install-local.sh /đường/dẫn/project-đích zalo-pre-submit-review   # chỉ 1 skill cụ thể
cd /đường/dẫn/project-đích && git add .omp/skills && git commit -m "vendor AI skill(s) into project"
```
Script copy vào `<project-đích>/.omp/skills/<tên-skill>/` (đúng convention project-local skill của công ty). Sau khi commit, `.omp/skills/` là 1 phần của repo project đích — clone project đích về là agent tự nạp skill ngay, không cần chạy `sync.sh`/cài gì thêm trên máy mới. Cập nhật khi repo skill đổi: chạy lại `install-local.sh` rồi commit lại vào project đích.

### Bước 2 — Dùng skill
Mở agent (Claude Code/omp/ckit) tại thư mục dự án, yêu cầu theo đúng tên skill cần dùng, ví dụ:
- *"chạy pre-submit review theo skill zalo-pre-submit-review trước khi nộp duyệt"* — xem chi tiết quy trình trong [`zalo-pre-submit-review/SKILL.md`](./zalo-pre-submit-review/SKILL.md).
- *"kiểm tra UI/logic theo skill figma-logic-conformance-test với file logic.md và Figma file này"* — xem chi tiết trong [`figma-logic-conformance-test/SKILL.md`](./figma-logic-conformance-test/SKILL.md).

**Đọc kỹ trước khi trình bày kết quả với khách hàng/nội bộ**: mục "Giới hạn quan trọng" ở cuối `SKILL.md` của từng skill — cả 2 đều là bản nháp.

### Bước 3 — Cập nhật khi repo có thay đổi
Repo GitHub là nguồn duy nhất (single source of truth).

**Nếu cài theo Cách A** (global): bản trong `~/.omp/agent/managed-skills/` chỉ là bản copy cục bộ, KHÔNG tự đồng bộ — mỗi thành viên team tự chạy lại đúng lệnh ở Bước 1 trên máy mình:
```bash
curl -fsSL https://raw.githubusercontent.com/nguyenba16/zalo-pre-submit-review-skills/main/sync.sh | bash
# hoặc nếu đã clone repo sẵn: bash sync.sh
```
Script so sánh commit SHA cũ/mới: nếu chưa đổi gì → báo "đã ở bản mới nhất" và dừng (an toàn chạy lại nhiều lần/nhiều máy). Nếu có đổi → đồng bộ lại toàn bộ nội dung mọi skill, in ra SHA cũ→mới + log các commit đã đổi. Không có push-notify tự động — team phải chủ động chạy lệnh trên (hoặc tự đặt lịch cron/Task Scheduler chạy `sync.sh` định kỳ).

**Nếu cài theo Cách B** (vendor project-local) — đây là vấn đề khó hơn: sau khi copy tĩnh vào project đích, project đó **không còn liên kết gì với repo skill gốc**, nên không ai tự biết khi nào cần cập nhật. Giải quyết bằng `check-local-updates.sh` — mỗi skill được vendor sẽ có kèm `.vendor-meta.json` ghi lại đúng commit gốc tại thời điểm copy; script này so sánh commit đó với `main` mới nhất trên GitHub, CHỈ báo lỗi thời khi có commit thật sự đổi đúng thư mục skill đó (không báo ồn ào nếu người khác chỉ sửa skill khác không liên quan):
```bash
bash check-local-updates.sh /đường/dẫn/project-đích
```
Exit code `3` nếu có skill lỗi thời (dùng được làm CI job định kỳ/cron cảnh báo), `0` nếu mọi skill đã vendor đều mới nhất. Thấy lỗi thời → chạy lại `install-local.sh` cho đúng skill đó rồi commit lại vào project đích. Chạy định kỳ (khuyến nghị hàng tháng, giống lịch chạy `check_updates.py` của skill zalo-pre-submit-review) — không có push-notify tự động, đây vẫn là cơ chế cần chủ động chạy, không phải theo dõi nền.

### Bước 4 — Báo lỗi / đề xuất sửa nội dung 1 skill
Mở [Issue](https://github.com/nguyenba16/zalo-pre-submit-review-skills/issues/new/choose) mới bằng template **"Báo lỗi / đề xuất sửa 1 skill"** (`.github/ISSUE_TEMPLATE/skill-bug-report.yml`) — form đã có sẵn field bắt buộc (skill nào, ID mục/rule sai, bằng chứng) + field tuỳ chọn (đề xuất sửa, commit đang vendor nếu cài theo Cách B). Không cần tự nhớ format tay.

**Không chỉ user mới report được** — cả 2 SKILL.md đều có mục "Agent tự phát hiện sai trong lúc chạy thật": nếu agent phát hiện checklist/scanner báo sai ngay trong lúc đang chạy review cho 1 project thật, agent tự hỏi user có muốn mở Issue luôn không (qua `gh issue create`, tự điền sẵn bằng chứng), thay vì để user tự nhớ làm sau. Chi tiết quy trình đầy đủ cho từng skill nằm trong `SKILL.md` tương ứng (mục "Cơ chế phản hồi & cập nhật").

## Giới hạn quan trọng

Đây là bộ tài liệu/script **hỗ trợ nội bộ**, KHÔNG thay thế review của người có chuyên môn (Zalo review team cho compliance, BA/QA cho logic nghiệp vụ). Nội dung pháp lý (Nhóm B trong `zalo-pre-submit-review`) chưa được người có chuyên môn pháp lý review — dùng để tham khảo, không dùng làm căn cứ pháp lý chính thức.
