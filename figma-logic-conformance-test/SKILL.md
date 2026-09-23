---
name: figma-logic-conformance-test
description: "Verify a built app screen matches its Figma mockup (Lane A) and its implemented business logic matches a BA-authored logic.md file (Lane B) — use when a BA hands off a Figma design + a markdown logic spec to dev, and you need to check the implementation against both sources of truth before QA/release. Not for Zalo censorship/policy compliance — see the separate zalo-pre-submit-review skill for that."
---

## Khi nào dùng skill này

Quy trình công ty: BA thiết kế mockup trên **Figma**, viết luồng nghiệp vụ vào **1 file `.md` logic**, đưa cả 2 cho dev làm. Skill này kiểm tra bản build thật có khớp CẢ HAI nguồn sự thật đó không — tách bạch rõ ràng 2 việc khác nhau (giao diện vs nghiệp vụ), KHÔNG gộp chung 1 lượt kiểm mơ hồ.

**Không phải** để kiểm tra chính sách kiểm duyệt Zalo (dùng skill `zalo-pre-submit-review` riêng cho việc đó) và **không** test backend độc lập (API, DB) — phạm vi ở đây là UI + logic nghiệp vụ hiển thị/xử lý ở tầng ứng dụng.

## Input cần có trước khi chạy

1. **Figma file key** (đoạn trong URL `figma.com/file/<file_key>/...`) + **Figma personal access token** (`FIGMA_TOKEN` env, tạo ở Figma → Settings → Personal access tokens).
2. **File `logic.md`** BA cung cấp.
3. **App chạy được** (dev server browser-preview, xem skill `zalo-mini-app-browser-testing` nếu là Zalo Mini App; với web app thường thì chỉ cần URL dev server).
4. **Bảng ánh xạ frame Figma ↔ route trong app** (`figma-route-map.json`, tự tạo — KHÔNG có cách suy đoán tự động đáng tin, vì tên frame BA đặt và tên route dev đặt hiếm khi khớp chữ). Format:
   ```json
   [
     { "frame": "Trang chủ", "route": "/" },
     { "frame": "Chi tiết SP", "route": "/product/:id", "sample": "/product/123" }
   ]
   ```
   Nếu chưa có file này, việc đầu tiên là hỏi dev/BA để lập — KHÔNG tự đoán mapping rồi báo cáo sai.

## Lane A — UI đối chiếu Figma

1. Export ảnh tham chiếu từ Figma:
   ```bash
   export FIGMA_TOKEN=figd_xxx
   python3 scripts/export_figma_frames.py <file_key> /tmp/figma-refs --page "Flows"
   ```
   Ghi ra `manifest.json` (tên frame, node id, đường dẫn PNG). `--page` lọc đúng 1 canvas nếu file Figma có nhiều page (flows/components/archive).
2. Với mỗi dòng trong `figma-route-map.json`: mở route tương ứng bằng `browser` tool (tab.goto), chụp screenshot ở cùng viewport width với ảnh Figma export (đọc `manifest.json` để biết kích thước gốc nếu cần).
3. So sánh 2 ảnh (ảnh Figma export vs screenshot thật) bằng **vision model định tính**, KHÔNG pixel-diff toán học — nội dung thật (data, hình ảnh) và font-rendering luôn khác mockup, pixel-diff sẽ báo lỗi tràn lan vô nghĩa. Hỏi vision model cụ thể: *"So sánh 2 ảnh: ảnh 1 là mockup thiết kế, ảnh 2 là app thật. Liệt kê CHỈ khác biệt về bố cục/thành phần thiếu-thừa/màu sắc sai lệch rõ ràng. Bỏ qua khác biệt do nội dung dữ liệu thật khác Lorem Ipsum, và khác biệt do font-rendering nhỏ."*
4. Phân loại mỗi route: **PASS** (khớp, không khác biệt đáng kể) / **WARN** (khác nhẹ — cần người xác nhận có chấp nhận được không) / **FAIL** (thiếu thành phần, sai bố cục rõ, sai màu thương hiệu).

## Lane B — Logic đối chiếu file `.md`

1. Trích rule nguyên tử từ file logic BA:
   ```bash
   python3 scripts/extract_logic_rules.py <logic.md> --json /tmp/logic-rules.json
   ```
   Đọc `structured_ratio` trong output: nếu **< 0.5** (script tự cảnh báo ra stderr), file BA viết dạng văn xuôi — KHÔNG tin danh sách rule tự động, tự đọc file gốc và trích rule bằng tay/LLM trước khi qua bước 2.
2. Với mỗi rule đã trích (có `id` + `line` + `text` để trace ngược về đúng dòng trong `logic.md`), xác định cách kiểm:
   - **Rule tính toán** ("giảm X%", "tính giá = ...") → tìm hàm liên quan qua `lsp`/`codegraph`/grep theo từ khoá trong rule, đối chiếu công thức trong code với mô tả.
   - **Rule điều kiện hiển thị/ẩn** ("chỉ hiện khi...", "ẩn nếu...") → tìm điều kiện render tương ứng trong component, xác nhận logic if/else khớp đúng điều kiện mô tả (kể cả trường hợp biên: =, >, >= khác nhau BA hay viết mơ hồ).
   - **Rule luồng nhiều bước** → dùng `browser` tool thực hiện đúng chuỗi thao tác mô tả, xác nhận kết quả cuối khớp.
3. Dispatch song song theo section (giống pattern `zalo-pre-submit-review`): mỗi subagent nhận 1 section + rule cụ thể + bối cảnh project (đã tóm tắt sẵn, không để subagent tự dò cấu trúc), trả PASS/FAIL/WARN + bằng chứng `file:line` (code) — **không suy luận PASS nếu không tìm thấy code liên quan**, phải trả `N/A — không tìm thấy implementation, xác nhận với dev` thay vì đoán.

## Báo cáo cuối — luôn trình bày dạng bảng, gộp Lane A + Lane B, không tách 2 báo cáo rời

Mỗi route/section 1 dòng trong bảng, để user quét mắt nắm toàn bộ kết quả trong vài giây thay vì đọc văn xuôi dài. Format bắt buộc:

```markdown
### Tóm tắt: X PASS · Y WARN · Z FAIL · W N/A (chưa tìm thấy implementation)

| Route/Rule | Lane | Trạng thái | Bằng chứng | Nguồn (Figma node / logic.md) |
|---|---|---|---|---|
| `/` (Trang chủ) | A — UI | PASS | Khớp mockup, không khác biệt đáng kể | node `12:34` |
| `/` (Trang chủ) | B — Logic | WARN | Điều kiện ẩn banner dùng `>` nhưng mô tả dùng `>=` — cần BA xác nhận biên | `logic.md:18` |
| `/product/:id` | A — UI | FAIL | Thiếu nút "Thêm giỏ hàng" so với mockup | node `12:56` |
| `/product/:id` | B — Logic | FAIL | Giá giảm tính `price * 0.9` nhưng mô tả là giảm 15% | `logic.md:42`, `src/features/product/usePrice.ts:31` |
| `/checkout` | B — Logic | N/A | Không tìm thấy implementation rule "giới hạn 5 sản phẩm/đơn" — xác nhận với dev có đúng route/file không | `logic.md:60` |
```

Quy tắc bắt buộc khi điền bảng:
- **1 dòng = 1 route/rule cụ thể**, không gộp nhiều route vào 1 dòng "chung chung" — user phải trace được thẳng từ dòng bảng về đúng route/rule.
- Cột **Lane** luôn ghi rõ `A — UI` hay `B — Logic`, không để trống — tránh user nhầm 1 route đã kiểm cả 2 lane hay mới 1.
- Cột **Bằng chứng** là 1 câu ngắn, cụ thể (không viết "sai" chung chung) — Lane A mô tả khác biệt UI cụ thể, Lane B trích công thức/điều kiện sai + đúng.
- Cột **Nguồn** luôn trỏ về được: node id Figma (Lane A) hoặc `file:line` trong `logic.md` + code liên quan (Lane B) — không bỏ trống.
- **N/A khác với FAIL** — N/A nghĩa là subagent không tìm được implementation (có thể do tìm sai chỗ), không phải chắc chắn thiếu tính năng. Liệt kê riêng thành 1 dòng, không tự suy luận thành FAIL.
- Dòng FAIL đặt lên đầu bảng (sort theo mức nghiêm trọng: FAIL → WARN → N/A → PASS) để user thấy việc cần sửa trước tiên ngay khi lướt mắt, không phải kéo hết bảng mới thấy.
- Dòng **Tóm tắt** ở đầu (đếm số lượng mỗi loại) — user không cần đếm tay qua cả bảng để biết tổng quan.

## Cơ chế phản hồi & cập nhật (feedback/update mechanism)

Skill này còn ở trạng thái **bản nháp — chưa qua review thủ công, chưa test trên file Figma/logic.md thật của công ty**. Cơ chế dưới đây tồn tại để (a) người dùng report được rule/mapping sai, (b) agent tự report ngay khi phát hiện lúc đang chạy, thay vì để lỡ quên.

### 1. Báo lỗi một rule/mapping sai (dành cho người dùng skill)

Không sửa trực tiếp `figma-route-map.json`/`logic.md` của dự án khi chưa chắc chắn đó là lỗi của skill. Report kèm đủ 3 thông tin:
- **Định danh sai**: node id Figma (Lane A) hoặc `id`/`line` của rule trong output `extract_logic_rules.py` (Lane B) — không cần đánh số lại thủ công, script đã gán sẵn.
- **Bằng chứng**: ảnh so sánh Figma vs app thật (Lane A), hoặc `file:line` code + trích đoạn `logic.md` cho thấy checklist báo sai (false positive/negative) khi chạy trên project thật (Lane B).
- **Đề xuất sửa** (nếu có — vd sửa prompt vision model, sửa regex trích rule trong `extract_logic_rules.py`).

Kênh report chính thức: [GitHub Issues của repo `skill-claude`](https://github.com/nguyenba16/zalo-pre-submit-review-skills/issues) — tạo issue mới, dán đủ 3 thông tin trên vào mô tả, gắn label `figma-logic-conformance-test`.

### 2. Agent tự phát hiện sai trong lúc chạy thật — tự đề nghị mở Issue ngay

Khi đang chạy Lane A/Lane B cho 1 project thật và phát hiện script (`export_figma_frames.py`, `extract_logic_rules.py`) hoặc hướng dẫn trong skill này cho kết quả rõ ràng sai (không phải lỗi của project đang test) — **KHÔNG chỉ sửa chữa tạm rồi bỏ qua**. Ngay trong phiên làm việc:
1. **[WARN] Repo này là PUBLIC.** Không tự ý đính ảnh Figma/screenshot app thật hoặc trích đoạn `logic.md` chứa thông tin nghiệp vụ nhạy cảm của khách hàng vào bằng chứng. Mô tả bằng chứng dưới dạng văn bản trung tính (vd "Lane A báo FAIL dù layout khớp — do vision-model prompt hiểu nhầm ảnh nền trang trí là thiếu component") — chỉ đính ảnh/trích đoạn gốc nếu user xác nhận rõ ràng nó không chứa thông tin nhạy cảm.
2. Trước khi tạo issue mới, tìm issue trùng: `gh issue list --repo nguyenba16/zalo-pre-submit-review-skills --search "<từ khoá mô tả lỗi>" --state all`. Có issue trùng → comment bổ sung bằng chứng vào issue đó (`gh issue comment <số> --body "..."`) thay vì tạo mới.
3. Không thấy trùng, hỏi user 1 câu ngắn: *"Phát hiện [mô tả lỗi ngắn, đã ẩn thông tin nhạy cảm] khi chạy skill figma-logic-conformance-test — có muốn tôi mở GitHub Issue report luôn không (repo public)?"*.
4. Nếu đồng ý, dùng `gh issue create --repo nguyenba16/zalo-pre-submit-review-skills --title "..." --label figma-logic-conformance-test --body "..."` — body tự điền đủ 3 thông tin ở mục 1, cộng thêm commit đang vendor (đọc `.vendor-meta.json` trong `.omp/skills/figma-logic-conformance-test/` của project hiện tại nếu cài theo Cách B, hoặc bỏ qua nếu cài Cách A/không tìm thấy file).
5. Không tự ý sửa `scripts/*.py` trong bản vendor cục bộ của project — sửa gốc phải qua PR vào repo `skill-claude`, theo đúng quy trình ở mục 1.

## Giới hạn quan trọng

- **Mapping frame↔route là thủ công, không có cách suy luận đáng tin** — sai mapping sẽ tạo FAIL giả (so sánh nhầm 2 màn hình không liên quan). Luôn xác nhận file `figma-route-map.json` còn đúng trước khi tin báo cáo, nhất là sau khi BA thêm màn hình mới.
- **So sánh UI bằng vision model là định tính**, không phải pixel-perfect — không dùng để bắt lỗi 1-2px, chỉ bắt sai lệch rõ ràng (thiếu section, sai màu chủ đạo, sai bố cục).
- **`extract_logic_rules.py` là structural parser, không phải LLM** — chỉ tách được rule đã viết rõ ràng dạng bullet/số/Given-When-Then. File BA viết văn xuôi sẽ cho `structured_ratio` thấp và rule list rỗng/thiếu — script tự cảnh báo, đừng bỏ qua cảnh báo đó.
- Chưa test trên file Figma/logic.md thật của công ty — mới verify bằng fixture giả lập (xem `scripts/*.py` docstring). Chạy thử trên 1 project thật trước khi tin dùng cho khách hàng/release thật.
