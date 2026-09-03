---
name: zalo-pre-submit-review
description: "Run a pre-submit QA review on a Zalo Mini App (zmp-sdk/zmp-ui + Vite, any project) BEFORE submitting to Zalo's review/censorship process — checks the project against the full official checklist (censorship policy, developer agreement, legal/regulated-industry licensing, technical pitfalls, UI/UX, permission declarations, submission flow) bundled as checklist.md/checklist.docx in this skill's directory, to catch rejection causes before the 3-7 day review cycle."
---

## Khi nào dùng skill này

Trước khi bấm "Gửi xét duyệt" (submit) một Zalo Mini App — bản mới hoặc bản cập nhật — trên BẤT KỲ dự án Mini App nào (zmp-sdk + zmp-ui + Vite). Mỗi vòng xét duyệt của Zalo mất 3–7 ngày làm việc; mục tiêu của skill này là bắt trước các lỗi khiến hồ sơ bị từ chối/chậm duyệt, thay vì phát hiện sau khi Zalo trả về.

## Tài nguyên đi kèm

- `checklist.md` — checklist đầy đủ 217 mục, chia 6 nhóm (A–F), mỗi mục có nguồn (URL#anchor tài liệu chính thức Zalo), lý do/hậu quả, và nhãn `Automatable: yes/partial/no`. Bảng thống kê đầu file: 92 yes / 75 partial / 50 no.
- `checklist.docx` — bản Word cùng nội dung, dùng để gửi cho người phụ trách nội dung/pháp lý không dùng Markdown.

6 nhóm trong checklist:
- **Nhóm A** — Chính sách nội dung & kiểm duyệt (logo, tên, mô tả, điều hướng, xin quyền, quảng cáo, hiệu suất)
- **Nhóm B** — Pháp lý: KYB/eKYC, giấy phép ngành nghề có điều kiện (10 nhóm ngành, 24+69 mục hàng hoá/dịch vụ), Nghị định 13 (dữ liệu cá nhân), nghĩa vụ Solution Partner
- **Nhóm C** — Lỗi kỹ thuật dev/build/runtime (CORS, HTTPS, ảnh, server-to-server API, quota deploy, size limit, CI/CD, ES2015, app-config.json)
- **Nhóm D** — UI/UX, điều hướng, xác thực người dùng (navigation bar, back gesture, splash, luồng đăng nhập Zalo chuẩn)
- **Nhóm E** — Quy trình nộp duyệt & khai báo quyền (4 nhóm permission chính thức, Partner API tự động hoá: getAppPermissions/requestAppPermission/requestPublishMiniApp/publishMiniApp/webhook)
- **Nhóm F** — Bổ sung (dung lượng app, xác thực Mini App, thay đổi thông tin sau khi tạo)

## Cách chạy pre-submit review trên một dự án Mini App (bản tối ưu token — dùng từ 2026-09-03)

**KHÔNG** đọc toàn bộ `checklist.md` (405 dòng) rồi tự grep tuần tự từng mục — tốn token gấp nhiều lần vì đọc lặp lại cùng file source cho nhiều mục riêng lẻ, và giữ toàn bộ context checklist trong 1 phiên. Quy trình chuẩn:

1. **Đọc `checklist.md` MỘT LẦN** (có thể theo range nếu file lớn — dùng selector `:N-M` thay vì đọc lại toàn bộ ở bước sau) để nắm nội dung 6 nhóm A–F + nhãn Automatable của từng mục.
2. **Đọc nhanh cấu trúc dự án đích** (root listing + package.json + app-config.json + .env.example + 1-2 file kiến trúc như PROJECT.md/AGENTS.md) để biết stack, feature module, vị trí auth/permission service — dùng info này làm `context` chung cho các subagent, KHÔNG để mỗi subagent tự dò cấu trúc lại.
3. **Chia các mục `Automatable: yes/partial` thành nhóm A/C/D/E theo checklist gốc, dispatch SONG SONG 4 `scout` subagent trong MỘT lệnh `task` (KHÔNG tuần tự)** — mỗi subagent nhận:
   - Bối cảnh dự án đã tóm tắt sẵn ở bước 2 (KHÔNG bắt subagent tự khám phá lại repo).
   - Danh sách mục checklist cụ thể của nhóm đó, kèm **grep pattern/API name/regex đã trích sẵn** từ cột "Automatable" trong checklist (copy nguyên văn gợi ý kiểm tra, không diễn giải lại mơ hồ).
   - Yêu cầu output PASS/FAIL/WARN/N/A + bằng chứng `file:line` cho từng mục, KHÔNG paste toàn bộ nội dung file đã đọc.
4. **Nhóm B và F (chủ yếu `Automatable: no` — pháp lý/eKYC/giấy phép ngành nghề)**: KHÔNG dispatch subagent quét code (source không trả lời được các mục này). Tự đối chiếu trực tiếp từ checklist + 1-2 lần grep có mục tiêu (vd tìm trang "Quản lý quyền"/business info) nếu cần xác nhận nhanh; phần còn lại liệt kê thẳng làm checklist thủ công cho người phụ trách.
5. Sau khi 4 subagent hoàn tất, **đọc `agent://<id>` cho từng job** (không phải preview rút gọn) rồi tự tổng hợp — KHÔNG yêu cầu subagent tự viết báo cáo Markdown dài; JSON có cấu trúc (summary/files/architecture) dễ tổng hợp và rẻ hơn prose.
6. **Xuất báo cáo cuối** theo format: WARN/FAIL cần xử lý trước (kèm bằng chứng + hành động cụ thể) → mục cần xác nhận thủ công → danh sách quyền cần xin duyệt → PASS gộp ngắn gọn theo nhóm → phần B/F pháp lý tóm tắt (không liệt kê lại cả 50 mục no, trỏ về `checklist.md:<dòng>` để người đọc tự mở).

Hiệu quả đã đo: 1 lần chạy full 4 nhóm (~90 mục automatable) trên 1 Mini App cỡ trung (30+ file feature) tốn ~5 tool-call rounds (2 batch read song song + 1 dispatch 4-agent + 2 wait/collect) thay vì phải tự đọc từng file nguồn cho từng mục tuần tự.


## Giới hạn quan trọng — đọc trước khi trình bày/cam kết với khách hàng

- Đây là **pre-flight QA trước khi nộp**, KHÔNG thay thế đội kiểm duyệt của Zalo — Zalo vẫn có quyết định cuối cùng, đặc biệt với các mục chủ quan (nội dung, tên/logo phù hợp thương hiệu, giấy phép ngành nghề thật).
- Checklist bám sát tài liệu tại thời điểm 2026-09-03 — Zalo có thể cập nhật chính sách; nếu phát hiện nội dung checklist lệch với tài liệu chính thức khi dùng, cập nhật lại `checklist.md`/`checklist.docx` trong skill này và ghi rõ ngày cập nhật mới ở đầu file.
- 217 mục, ~42% `yes` (agent tự quyết được), ~35% `partial` (agent chỉ cảnh báo), ~23% `no` (thuần thủ công/pháp lý) — xem bảng thống kê đầu `checklist.md` để ước lượng effort trước khi cam kết thời gian review với khách hàng.

## Cơ chế phản hồi & cập nhật (feedback/update mechanism)

Skill này còn ở trạng thái **bản nháp — chưa qua review thủ công, chưa test trên project thật**. Cơ chế dưới đây tồn tại để (a) người dùng report được mục sai, (b) phát hiện khi Zalo đổi tài liệu, (c) có audit trail thay vì sửa âm thầm.

### 1. Báo lỗi một mục checklist (dành cho người dùng skill)

Không sửa trực tiếp `checklist.md` khi chưa chắc chắn. Report kèm đủ 3 thông tin:
- **Định danh mục sai**: dòng "— Nguồn: <URL#anchor>" của mục đó (mỗi mục đã có sẵn anchor riêng, dùng làm ID thay vì đánh số lại toàn bộ 217 mục).
- **Bằng chứng**: screenshot/link trang Zalo hiện tại cho thấy nội dung khác với checklist, hoặc log cho thấy checklist báo sai (false positive/negative) khi chạy trên project thật.
- **Đề xuất sửa** (nếu có).

Kênh report chính thức: [GitHub Issues của repo này](https://github.com/nguyenba16/zalo-pre-submit-review-skills/issues) — tạo issue mới, dán đủ 3 thông tin trên vào mô tả. Muốn tự sửa: fork/branch, sửa theo quy trình mục 3, mở Pull Request (không push thẳng lên `main`).

### 2. Phát hiện tài liệu Zalo đã đổi — `check_updates.py`

`sources.json` lưu content-hash của 27 trang tài liệu gốc (baseline chụp lúc 2026-09-03). Chạy định kỳ (khuyến nghị: hàng tháng, hoặc bắt buộc trước khi dùng skill cho 1 dự án lớn/khách hàng mới):

```
cd ~/.omp/agent/managed-skills/zalo-pre-submit-review
pip install requests beautifulsoup4   # 1 lần
python3 check_updates.py              # chỉ báo cáo, KHÔNG tự sửa gì
```

Script tự fetch lại 27 URL, tính hash nội dung text (đã strip script/style/svg), so với baseline, in ra 3 nhóm: **Không đổi** / **Đã thay đổi** (cần đọc lại + sửa checklist.md) / **Lỗi fetch** (URL có thể đã đổi đường dẫn). Script KHÔNG tự sửa `checklist.md` — chỉ báo hiệu cần người/agent đọc lại trang đó.

### 3. Quy trình cập nhật sau khi phát hiện thay đổi (người hoặc agent thực hiện)

1. Đọc lại đúng trang đã đổi bằng `read` tool trực tiếp trên URL (không đoán nội dung mới).
2. Sửa đúng mục tương ứng trong `checklist.md`, giữ nguyên format `- [ ] ... — Nguồn: ... Automatable: ...`.
3. Regenerate `checklist.docx` (xem script parse ở mục dưới) — không sửa tay file .docx.
4. Cập nhật dòng "Cập nhật lần cuối" ở đầu `checklist.md`.
5. Chạy `python3 check_updates.py --update` để ghi hash mới vào `sources.json` (chỉ chạy SAU KHI đã đối chiếu và sửa checklist — hash không tự xác nhận nội dung đúng, chỉ xác nhận "đã fetch lại").
6. Ghi 1 entry vào `CHANGELOG.md` (người sửa, ngày, lý do, mục nào đổi) — bắt buộc, để có audit trail khi nội dung pháp lý (Nhóm B) bị nghi ngờ sau này.

### 4. Giới hạn của cơ chế hiện tại (thẳng thắn)

- **[2026-09-03] Đã chuyển vào git repo**: https://github.com/nguyenba16/zalo-pre-submit-review-skills — feedback đi qua Issue/PR, không còn giới hạn "chỉ trên máy này". Bản cài đặt cục bộ tại `~/.omp/agent/managed-skills/zalo-pre-submit-review/` (để agent tự nạp skill mỗi phiên) cần đồng bộ thủ công với repo này sau mỗi lần merge PR (chưa có CI tự đồng bộ — xem "Bài học" bên dưới nếu cần bổ sung).
- `check_updates.py` chỉ phát hiện trang ĐÃ ĐỔI NỘI DUNG, không đánh giá được thay đổi đó có ảnh hưởng đến checklist hay không (vd Zalo sửa lỗi chính tả cũng bị đánh dấu "đã đổi") — vẫn cần người đọc diff.
- Nhóm B (pháp lý) chưa có ai có chuyên môn pháp lý review — hash-check kỹ thuật không thay được việc này.

## Regenerate checklist.docx từ checklist.md (chi tiết script parse)

Parse dòng bắt đầu `# `/`## `/`### ` thành heading level 0/1/3, `- [ ] ` thành List Bullet với glyph checkbox (\u2610), `- ` thành List Bullet 2, dòng `|...|` gom thành bảng (bỏ dòng separator `|---|`), `> ` thành đoạn in nghiêng thụt lề (bỏ qua dòng chỉ có `>` trơ trọi để tránh artifact rỗng), inline `**bold**` và `` `code` `` tách run riêng qua regex split `r'(\*\*.*?\*\*|`[^`]*?`)'`. Không sửa tay file .docx.

## Bài học build lần đầu (2026-09-03)

- Khi nghiên cứu nhiều cụm tài liệu độc lập, dùng `task` dispatch song song (docs-researcher agent) theo cụm chủ đề (censorship/legal/technical/UI-UX/submission/community) thay vì đọc tuần tự — tiết kiệm ~6x thời gian cho ~30 trang tài liệu.
- Sitemap.xml của Docusaurus site (mini.zalo.me/sitemap.xml) là cách nhanh nhất để liệt kê TOÀN BỘ URL doc pages thay vì đoán/crawl thủ công — dùng bash grep -o trên artifact raw content.
- `manage_skill create` chỉ tạo SKILL.md; để thêm resource file (checklist.md/.docx) vào managed skill, copy trực tiếp vào thư mục thật `~/.omp/agent/managed-skills/<name>/` bằng bash cp — managed skill dirs là filesystem thường, không giới hạn 1 file.
- Trên Windows, `find ... -path '*name*'` trả path có dấu `\` trộn `/` khiến `dirname` tính sai — luôn xây absolute path skill dir trực tiếp (`~/.omp/agent/managed-skills/<exact-name>`) thay vì suy ra từ `find`+`dirname`.
- python-docx có sẵn qua `bash`/python (không qua `eval` tool — eval Python backend có thể unavailable; dùng bash python3 heredoc thay thế).
