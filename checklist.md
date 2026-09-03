# Zalo Mini App — Checklist Pre-Submit Review

> Checklist tổng hợp từ tài liệu chính thức Zalo Mini App (mini.zalo.me / miniapp.zaloplatforms.com) để rà soát TRƯỚC khi nộp một Mini App (bản mới hoặc bản cập nhật) lên vòng xét duyệt của Zalo. Mục tiêu: bắt trước các lỗi khiến hồ sơ bị từ chối/chậm duyệt (3–7 ngày làm việc mỗi vòng), thay vì phát hiện sau khi Zalo trả về.
>
> **Cách đọc mỗi mục:** `- [ ] <yêu cầu cụ thể> — Nguồn: <URL#anchor>. <lý do/hậu quả nếu vi phạm>. Automatable: yes | partial | no — <cách một AI agent có thể kiểm tra>.`
>
> - **Automatable: yes** — có thể viết script/agent kiểm tra tự động 100% (static scan code, config, hoặc dynamic browser test có kết quả nhị phân rõ ràng).
> - **Automatable: partial** — agent kiểm tra được MỘT PHẦN (phát hiện dấu hiệu/nghi vấn), phần còn lại (nội dung, ngữ nghĩa, pháp lý) cần người review.
> - **Automatable: no** — hoàn toàn thủ công/pháp lý/hành chính, agent chỉ nhắc nhở trong checklist, không tự kiểm tra được.
>
> Cập nhật lần cuối: 2026-09-03. Nguồn tài liệu đầy đủ liệt kê ở Phụ lục cuối file.

## Thống kê mức độ tự động hoá theo Nhóm

| Nhóm | Tổng số mục | Automatable: yes | partial | no |
|---|---|---|---|---|
| Nhóm A — Chính sách nội dung & kiểm duyệt (Censorship Policy) | 53 | 21 | 20 | 12 |
| Nhóm B — Pháp lý, hợp đồng nhà phát triển & tuân thủ dữ liệu cá nhân | 58 | 23 | 10 | 25 |
| Nhóm C — Lỗi kỹ thuật (dev/build/runtime) | 24 | 15 | 7 | 2 |
| Nhóm D — UI/UX, điều hướng & xác thực người dùng | 23 | 6 | 17 | 0 |
| Nhóm E — Quy trình nộp duyệt & khai báo quyền (Submission & Permissions) | 55 | 26 | 19 | 10 |
| Nhóm F — Cộng đồng, thông báo & điều khoản bổ sung | 4 | 1 | 2 | 1 |
| **Tổng** | **217** | **92** | **75** | **50** |

`yes` = agent kiểm tra tự động hoàn toàn (static/dynamic scan có kết quả nhị phân). `partial` = agent phát hiện dấu hiệu/nghi vấn, người review quyết định cuối. `no` = thuần thủ công/pháp lý/hành chính, agent chỉ nhắc trong checklist.

Gợi ý vận hành: chạy phần `yes`/`partial` như một gate CI tự động trước mỗi lần submit (static scan + browser smoke test); phần `no` giữ nguyên là checklist thủ công cho người phụ trách pháp lý/nội dung điền tay trước khi nộp hồ sơ.

---

## Mục lục

- [Nhóm A — Chính sách nội dung & kiểm duyệt (Censorship Policy)](#nhóm-a--chính-sách-nội-dung--kiểm-duyệt-censorship-policy)
- [Nhóm B — Pháp lý, hợp đồng nhà phát triển & tuân thủ dữ liệu cá nhân](#nhóm-b--pháp-lý-hợp-đồng-nhà-phát-triển--tuân-thủ-dữ-liệu-cá-nhân)
- [Nhóm C — Lỗi kỹ thuật (dev/build/runtime)](#nhóm-c--lỗi-kỹ-thuật-devbuildruntime)
- [Nhóm D — UI/UX, điều hướng & xác thực người dùng](#nhóm-d--uiux-điều-hướng--xác-thực-người-dùng)
- [Nhóm E — Quy trình nộp duyệt & khai báo quyền (Submission & Permissions)](#nhóm-e--quy-trình-nộp-duyệt--khai-báo-quyền-submission--permissions)
- [Nhóm F — Cộng đồng, thông báo & điều khoản bổ sung](#nhóm-f--cộng-đồng-thông-báo--điều-khoản-bổ-sung)
- [Phụ lục — Nguồn tài liệu tham khảo đầy đủ](#phụ-lục--nguồn-tài-liệu-tham-khảo-đầy-đủ)

---

## Nhóm A — Chính sách nội dung & kiểm duyệt (Censorship Policy)

### A1. Logo Mini App

- [ ] Logo Mini App phải là logo chính chủ, không sử dụng logo của ứng dụng khác hoặc nhãn hàng khác — Nguồn: https://mini.zalo.me/documents/zalo-mini-app-censorship-policy/#11-logo-chính-chủ-không-giả-mạo. Dùng logo giả mạo/của bên khác bị coi là vi phạm và từ chối duyệt. Automatable: partial — so khớp hash/similarity của icon app với logo các thương hiệu phổ biến để cảnh báo nghi vấn; xác nhận "chính chủ" cần review thủ công.
- [ ] Mini App phải có logo (không được để trống logo) — Nguồn: cùng trang, #11. "Mini App không có logo" là vi phạm liệt kê rõ. Automatable: yes — kiểm tra field icon/logo trong app-config không rỗng.
- [ ] Logo phải liên quan trực tiếp đến chức năng/mục đích của Mini App, không dùng logo chung chung không liên quan — Nguồn: #12-logo-phù-hợp-với-chức-năng-mini-app. Automatable: no — cần đánh giá ngữ nghĩa/hình ảnh, phù hợp cho review thủ công hoặc AI vision review.
- [ ] Logo không được chứa số điện thoại hoặc QR code — Nguồn: #12. Automatable: partial — OCR/QR-detector quét file icon.
- [ ] Logo không được có nền trong suốt (background transparent) — Nguồn: #12. Automatable: yes — kiểm tra alpha channel của file icon (PNG).

### A2. Tên Mini App

- [ ] Tên phải thể hiện đúng chức năng thực tế, không gây hiểu lầm/sai lệch — Nguồn: #21-tên-phù-hợp-với-tính-năngchức-năng-của-mini-app. Automatable: no — cần LLM review đối chiếu tên với mô tả/chức năng thực tế.
- [ ] Tên không được viết hoa toàn bộ (ALL CAPS) — Nguồn: #22-quy-định-về-việc-đặt-tên-mini-app. Automatable: yes — regex kiểm tra chuỗi tên toàn uppercase.
- [ ] Tên không được dùng danh từ chung/từ khóa chung chung (cần tiền tố/hậu tố định danh đơn vị sở hữu) — Nguồn: #22. Automatable: no — cần đánh giá ngữ nghĩa (vd "Đặt vé", "Mua sắm" là vi phạm).
- [ ] Tên không được chứa các từ "App", "Mini App", "Zalo" — Nguồn: #22. Automatable: yes — regex case-insensitive.
- [ ] Tên không được chứa ký tự đặc biệt (#, $, @, !), emoji hoặc biểu tượng — Nguồn: #22. Automatable: yes — regex/unicode-category scan.
- [ ] Nếu tên trùng thương hiệu đã đăng ký bản quyền, phải chuẩn bị sẵn giấy tờ chứng minh quyền sở hữu thương hiệu để nộp kèm — Nguồn: #22. Automatable: no.

### A3. Mô tả Mini App (App Description)

- [ ] Mô tả phải phản ánh chính xác chức năng, đối tượng và mục đích sử dụng thực tế — Nguồn: #31-mô-tả-phù-hợp-với-tính-năngchức-năng-của-mini-app. Automatable: partial — LLM đối chiếu mô tả submit với chức năng thực tế app.
- [ ] Bắt buộc phải có mô tả (không được để trống) — Nguồn: #31. Automatable: yes.
- [ ] Mô tả không được chứa đường liên kết (link) ra ngoài — Nguồn: #32. Automatable: yes — regex quét URL pattern trong text mô tả.
- [ ] Mô tả không được chứa nội dung vi phạm thuần phong mỹ tục hoặc bị cấm theo pháp luật VN — Nguồn: #32. Automatable: partial — content-moderation model quét text, kết quả cần review thủ công.

### A4. Nội dung Mini App

- [ ] Không được điều hướng người dùng ra ngoài để tải một ứng dụng riêng khác — Nguồn: #41-điều-hướng-liên-kết-trang-thứ-3. Automatable: partial — quét text UI/CTA ("Tải app", App Store/CH Play link).
- [ ] Không được mời/điều hướng đăng nhập bằng Google, Facebook hoặc nền tảng bên thứ ba khác — Nguồn: #41. Automatable: yes — static scan tìm SDK/nút "Đăng nhập bằng Google/Facebook", `signInWithGoogle`, Facebook SDK.
- [ ] Không được điều hướng ra liên kết ngoài Mini App, TRỪ hiển thị Chính sách bảo mật/Điều khoản sử dụng — Nguồn: #41. Automatable: partial — scan `window.open`, `<a target=_blank>` trỏ domain ngoài, đối chiếu whitelist.
- [ ] Nếu hiển thị Chính sách bảo mật/Điều khoản, phải nhúng trực tiếp trong Mini App dưới dạng popup nội bộ, không mở trình duyệt ngoài — Nguồn: #41. Automatable: yes — browser test click link, xác nhận nội dung hiện trong popup/webview nội bộ.
- [ ] Nội dung không được sai lệch, lừa đảo, giả mạo hoặc bị cấm theo pháp luật — Nguồn: #42-nội-dung-đúng-pháp-luật. Automatable: no.
- [ ] Không được tự ý treo banner quảng cáo bên thứ ba kiếm tiền — Nguồn: #43-nội-dung-mang-tính-quảng-cáo-kiếm-tiền. Automatable: partial — scan iframe/script quảng cáo (AdSense, banner SDK).
- [ ] Không được chứa/tạo điều kiện mua bán vật phẩm ảo, đơn vị ảo của trò chơi điện tử — Nguồn: #44-vật-phẩm-ảo. Automatable: no.
- [ ] Không được liên quan giao dịch tiền điện tử/NFT chưa được cấp phép — Nguồn: #44. Automatable: no — có thể scan keyword "crypto"/"NFT"/"token" làm cảnh báo sơ bộ.
- [ ] Dịch vụ nội dung số/tiện ích số (khóa học online, gói nhạc/phim...) cần đối chiếu quy định riêng khác với dịch vụ gắn sử dụng thực tế — Nguồn: #44. Automatable: no.
- [ ] **Tuyệt đối cấm** tính năng Rút tiền/Trả thưởng (withdraw/cashout) — Nguồn: #45-mini-app-có-tính-năng-liên-quan-đến-rút-tiềntrả-thưởng (mục chỉ liệt kê "Vi phạm", không có "Đạt chuẩn"). Automatable: partial — scan keyword "rút tiền"/"withdraw"/"trả thưởng"/"cashout".
- [ ] **Tuyệt đối cấm** tính năng mạng xã hội (đăng post, video, like, comment...) — Nguồn: #46-mini-app-có-tính-năng-mạng-xã-hội-hoặc-các-tính-năng-cạnh-tranh-trực-tiếp-với-sản-phẩm-trong-hệ-thống-zalo. Automatable: partial — scan module/route "post"/"comment"/"like"/"feed".
- [ ] **Tuyệt đối cấm** tính năng cạnh tranh trực tiếp với sản phẩm trong hệ sinh thái Zalo (Zing MP3, Zalo, Video...) — Nguồn: #46. Automatable: no.
- [ ] Toàn bộ hình ảnh phải tải được, không lỗi/vỡ hình — Nguồn: #47-hình-ảnh-văn-bản-của-ứng-dụng. Automatable: yes — browser crawl mọi trang, kiểm tra network response ảnh 200 OK.
- [ ] Font chữ phải hiển thị đúng, rõ ràng, không lỗi/khó đọc — Nguồn: #47. Automatable: partial — screenshot + OCR/vision-model kiểm tra tofu box/mojibake.
- [ ] Trang Chính sách/Điều khoản (nếu có) phải nêu rõ tên Mini App trong tiêu đề, nội dung cụ thể (không chung chung) — Nguồn: #48-nội-dung-chính-sách---điều-khoản-của-mini-app. Automatable: partial — text scan tiêu đề + LLM review độ cụ thể.

### A5. Xin quyền người dùng (áp dụng: Tên & Ảnh đại diện, SĐT, Vị trí, Camera, Thông báo, Quan tâm OA, Tương tác OA)

- [ ] Không hiển thị popup xin quyền ngay khi vừa vào Mini App — phải có ngữ cảnh/giải thích rõ trước — Nguồn: #61-ngữ-cảnh-xin-quyền. Automatable: yes — browser test: load trang đầu, kiểm tra không gọi permission API trong N giây đầu/trước tương tác.
- [ ] Không xin quyền mà không giải thích rõ mục đích sử dụng — Nguồn: #61. Automatable: partial.
- [ ] Bắt buộc phải có lựa chọn "Từ chối", và app vẫn dùng được sau khi từ chối — Nguồn: #61. Automatable: yes — browser test chọn "Từ chối", xác nhận app vẫn điều hướng được.
- [ ] Không được thiết kế UI xin quyền giả mạo giao diện chuẩn nền tảng Zalo — Nguồn: #62-giả-mạo-giao-diện-nền-tảng. Automatable: partial — kiểm tra permission dialog gọi qua zmp-sdk chuẩn (`authorize`/`getSetting`), không phải modal HTML tự vẽ giả native.
- [ ] Không bắt buộc cấp quyền (vị trí/camera/thông báo...) để mới dùng được app hoặc một tính năng cụ thể — Nguồn: #63-cấp-quyền-để-sử-dụng-mini-app. Automatable: yes — browser test từ chối quyền, xác nhận flow không bị chặn cứng.
- [ ] Không ngừng cung cấp dịch vụ hoàn toàn khi user từ chối cấp quyền — Nguồn: #63. Automatable: yes.
- [ ] API truy xuất thông tin cá nhân (getUserInfo/getLocation/getPhoneNumber/camera) chỉ kích hoạt theo hành vi cụ thể của user (bấm nút), không tự động gọi khi mount — Nguồn: #63. Automatable: yes — static scan: API nằm trong onClick handler hay trong useEffect mount không điều kiện.
- [ ] Không bắt buộc user đăng ký tài khoản mới để sử dụng — Nguồn: #64-đăng-nhập-để-sử-dụng-mini-app. Automatable: yes — browser test ở trạng thái ẩn danh, xác nhận không bị redirect bắt buộc.
- [ ] Không bắt buộc user đăng nhập để sử dụng (trừ app nội bộ trường học/công ty/tổ chức được duyệt riêng) — Nguồn: #64. Automatable: yes.
- [ ] Nếu thuộc ngoại lệ bắt buộc đăng nhập, phải giải thích rõ lý do cần quyền trước khi xin, không gây nhầm lẫn — Nguồn: #64. Automatable: partial.
- [ ] Nếu liên kết SĐT Zalo với tài khoản có sẵn qua đăng nhập truyền thống (username/password): chức năng phải label rõ **"Liên kết tài khoản"**, và chỉ thực hiện SAU KHI đã đăng nhập thành công bằng tài khoản truyền thống (không trước/thay thế bước đăng nhập) — Nguồn: #65-liên-kết-tài-khoản. Automatable: partial — browser flow test xác nhận thứ tự UI đúng; label chính xác cần review/LLM check.

### A6. Quyền riêng tư và bảo mật (Data Collection & Privacy)

- [ ] Không thu thập dữ liệu cá nhân mà không có sự đồng ý rõ ràng (explicit consent) trước đó — Nguồn: #7-quyền-riêng-tư-và-bảo-mật. Automatable: partial — scan lệnh gọi API thu thập dữ liệu có đứng sau consent dialog hay không.
- [ ] Không chứa mã độc, hoặc dẫn người dùng qua liên kết chứa mã độc — Nguồn: #7. Automatable: partial — static malware/dependency scan (npm audit, virus scan domain ngoài).
- [ ] Không chia sẻ dữ liệu cá nhân cho bên thứ ba mà không thông báo/xin phép; nếu có, phải có đồng ý rõ ràng + bên thứ ba tuân thủ chuẩn bảo mật tương đương — Nguồn: #7. Automatable: partial — network traffic scan liệt kê request gửi dữ liệu cá nhân tới domain ngoài.

### A7. Tích hợp Checkout SDK (Thanh toán)

- [ ] Nếu có phát sinh đơn hàng, thanh toán và hiển thị giá tiền trực tiếp, bắt buộc tích hợp Zalo Checkout SDK — Nguồn: #8-tích-hợp-checkout-sdk (chi tiết: https://mini.zalo.me/documents/checkout-sdk). Automatable: yes — scan package.json tìm Checkout SDK, đối chiếu UI có hiển thị giá + nút mua hàng mà thiếu SDK.
- [ ] Nếu chưa dùng Checkout SDK, KHÔNG hiển thị giá tiền trực tiếp — đổi nút mua/thanh toán thành "Liên hệ"/"Tư vấn" — Nguồn: #8. Automatable: yes — UI text scan giá tiền + CTA label.

### A8. Hiệu suất Mini App

- [ ] Mọi tính năng phải hoạt động bình thường, không ở trạng thái Demo/không dùng được khi nộp xét duyệt — Nguồn: #51-tính-năng-hoạt-động-bình-thường. Automatable: partial — browser crawl route chính, kiểm tra lỗi console/404, placeholder "Coming soon"/"Demo".
- [ ] Không được treo, màn hình trắng hoặc tối trong khi sử dụng — Nguồn: #52-sự-cố-khi-sử-dụng. Automatable: yes — browser smoke test bắt uncaught exception / blank-screen detector.
- [ ] Thời gian tải không vượt quá 10 giây; **LCP < 2.5s**; **PageLoad Time < 1.5s** — Nguồn: #53-thời-gian-load-ứng-dụng. Automatable: yes — Lighthouse/Web Vitals đo LCP & PageLoad trên các trang chính.

### A9. Nội dung theo ngành đặc thù, thời hạn và duy trì hoạt động

- [ ] Ngành đặc thù (Dược, Mỹ phẩm, TPCN...) hoặc kinh doanh có điều kiện phải nộp đầy đủ xác thực/giấy tờ liên quan — Nguồn: #93-xét-duyệt-mini-app-nhóm-ngành-đặc-thù-và-kinh-doanh-có-điều-kiện. Automatable: no.
- [ ] Nếu có campaign/sự kiện có thời hạn, phải thể hiện rõ thời gian bắt đầu/kết thúc trong mô tả version hoặc trên UI — Nguồn: #94-mini-app-triển-khai-có-thời-hạn. Automatable: partial.
- [ ] Phải xác thực qua OA hoặc giấy phép/tài liệu hợp lệ tùy loại hình sở hữu & ngành nghề để duy trì hoạt động — Nguồn: #92-duy-trì-hoạt-động-của-mini-app. Automatable: no.
- [ ] Phải duy trì tối thiểu **10 lượt truy cập/tháng** để tránh bị hạn chế hiển thị/vô hiệu hóa (nếu không đáp ứng liên tục 3 tháng) — Nguồn: #92. Automatable: no — cần dữ liệu analytics thật từ Zalo Developer Portal.

---

## Nhóm B — Pháp lý, hợp đồng nhà phát triển & tuân thủ dữ liệu cá nhân

### B1. Đăng ký, xác thực chủ sở hữu Mini App (KYB/eKYC)

- [ ] Cá nhân: tài khoản Zalo phải đã eKYC thành công trước khi phát hành — Nguồn: https://mini.zalo.me/documents/zalo-mini-app-developer-program-agreement/mini-app-verification/#2-quy-định-xác-thực (mục 2.1). Thiếu eKYC → từ chối/hạn chế hiển thị kể từ 15/10/2025. Automatable: no.
- [ ] Doanh nghiệp/Hộ kinh doanh: xác thực qua OA doanh nghiệp HOẶC nộp Giấy chứng nhận ĐKKD/Hộ kinh doanh + CMND/CCCD/Hộ chiếu người đại diện pháp luật — Nguồn: mini-app-verification/#21. Automatable: no.
- [ ] Cơ quan nhà nước/Đơn vị sự nghiệp: xác thực qua OA cơ quan nhà nước/tiện ích công — Nguồn: mini-app-verification/#21. Automatable: no.
- [ ] Mỗi bản cập nhật (kể cả chỉ đổi tính năng/giao diện) phải thẩm định lại từ đầu — Nguồn: developer-program-agreement/#5-thẩm-định-và-phê-duyệt-mini-app (5.2.b). Automatable: partial — cảnh báo dựa trên diff bản build trước khi submit.
- [ ] Hồ sơ thẩm định phải mô tả trung thực; nếu app có hệ thống tài khoản riêng, phải cung cấp đầy đủ tài khoản/mật khẩu test và bật toàn bộ tính năng cho tài khoản đó — Nguồn: #5 (5.2.a). Automatable: yes — kiểm tra field "tài khoản test"/"mật khẩu test" đã điền.

### B2. Xác thực giấy phép ngành nghề kinh doanh có điều kiện (theo lĩnh vực)

- [ ] Xác định trước khi nộp: app có thuộc 1 trong 10 nhóm ngành có điều kiện không (Cơ quan nhà nước, Tài chính, Y tế, Giáo dục, Bất động sản, Thương mại, F&B, GTVT, Tiện ích đời sống, Truyền thông) — Nguồn: mini-app-verification/#22. Automatable: partial — phân loại ngành dựa trên mô tả sản phẩm, xác nhận giấy phép cần người review.
- [ ] Cơ quan nhà nước: Quyết định thành lập + Công văn yêu cầu xác thực theo mẫu — Nguồn: #22. Automatable: no.
- [ ] Tài chính (Bảo hiểm/Ngân hàng/Trung gian thanh toán): (a) Giấy xác nhận ngành nghề, (b) Due Diligence theo mẫu, (c) Giấy CN đăng ký nhãn hiệu/quyền tác giả, (d) Giấy phép chuyên ngành tương ứng — Nguồn: #22. Automatable: no — liên hệ support@fiza.ai cho case riêng.
- [ ] Dược phẩm/Thiết bị y tế: Giấy xác nhận mã ngành 4649/4772 + Giấy CN đủ điều kiện kinh doanh dược + Giấy xác nhận nội dung quảng cáo (nếu có) — Nguồn: #22. Automatable: no.
- [ ] Bệnh viện/Phòng khám/Y tế dự phòng: mỗi cơ sở (kể cả chi nhánh) phải có giấy phép hoạt động riêng — Nguồn: #22. Automatable: no.
- [ ] Giáo dục (mọi cấp): Quyết định thành lập/Giấy phép hoạt động — Nguồn: #22. Automatable: no.
- [ ] Bất động sản: Giấy xác nhận ngành nghề + tối thiểu 1 người có chứng chỉ hành nghề môi giới BĐS — Nguồn: #22. Automatable: no.
- [ ] Mỹ phẩm & Làm đẹp: mã ngành 4649/4772 + Phiếu công bố sản phẩm mỹ phẩm (Bộ Y tế) + chứng từ nguồn gốc + chứng từ chất lượng — Nguồn: #22. Automatable: no.
- [ ] Thực phẩm & FMCG: Giấy xác nhận mã ngành + Giấy CN cơ sở đủ điều kiện ATTP — Nguồn: #22. Automatable: no.
- [ ] Đồ uống có cồn: Giấy xác nhận mã ngành + giấy phép phân phối/bán buôn/bán lẻ/tiêu dùng tại chỗ tương ứng (đồng thời thuộc danh mục HẠN CHẾ — xem B3) — Nguồn: #22. Automatable: no.
- [ ] Vàng, bạc, đá quý: Giấy xác nhận mã ngành + (Giấy phép KD vàng miếng HOẶC Giấy CN đủ điều kiện sản xuất vàng trang sức) — Nguồn: #22. Automatable: no.
- [ ] Thực phẩm chức năng: Xác nhận công bố phù hợp ATTP + Giấy xác nhận bản công bố sản phẩm + chứng từ đại lý/hoá đơn nhập khẩu (nếu có) + Giấy xác nhận nội dung quảng cáo (nếu có); mô tả BẮT BUỘC ghi "Sản phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh"; KHÔNG dùng hình ảnh/trang phục/tên bác sĩ-dược sĩ-nhân viên y tế hay thư cảm ơn bệnh nhân để quảng cáo; không bán hàng xách tay — Nguồn: regulated-products-and-services/#i-hàng-hoá-2 (mục 25). Automatable: yes (phần câu chữ mô tả bắt buộc + phát hiện hình ảnh/tên bác sĩ scan được) / no (phần giấy phép).
- [ ] Sàn TMĐT đa ngành: cần Giấy phép sàn TMĐT riêng — Nguồn: #22. Automatable: no.
- [ ] F&B: Giấy xác nhận ngành nghề + Giấy CN cơ sở đủ điều kiện ATTP — Nguồn: #22. Automatable: no.
- [ ] GTVT (vận chuyển hành khách/hàng hoá): Giấy xác nhận ngành nghề + Giấy phép kinh doanh vận tải — Nguồn: #22. Automatable: no.
- [ ] Du lịch: Giấy xác nhận ngành nghề + Giấy phép kinh doanh dịch vụ lữ hành (trong nước/quốc tế) — Nguồn: #22. Automatable: no.
- [ ] Viễn thông/Điện lực/Cấp nước/Báo chí/Trang tin điện tử/Xuất bản: Công văn yêu cầu xác thực theo mẫu + giấy phép chuyên ngành tương ứng — Nguồn: #22. Automatable: no.
- [ ] Ngành mới không nằm trong danh mục hoặc cần chứng minh SHTT (tên/logo): chuẩn bị chủ động tài liệu bổ sung khi Zalo yêu cầu — Nguồn: mini-app-verification/ (mục "Tài liệu bổ sung khác"). Automatable: no.
- [ ] Timeline: xét duyệt xác thực mất **3–5 ngày làm việc** kể từ khi nhận đủ tài liệu — chuẩn bị đủ hồ sơ trước khi nộp — Nguồn: mini-app-verification/ (mục "Thời gian xử lý"). Automatable: yes — checklist đối chiếu danh sách tài liệu bắt buộc theo ngành trước khi submit.

### B3. Danh mục hàng hoá/dịch vụ cấm, hạn chế, có điều kiện

- [ ] Rà soát KHÔNG có 17 nhóm hàng hoá cấm: vũ khí quân dụng/quân trang; ma tuý; hoá chất bảng 1; văn hoá phẩm phản động/đồi truỵ/mê tín; pháo; đồ chơi nguy hiểm/game bạo lực có hại trẻ em; thuốc thú y/BVTV cấm; động thực vật hoang dã quý hiếm cấm khai thác; thuỷ sản cấm khai thác/có độc tố; phân bón ngoài danh mục; giống cây trồng ngoài danh mục/gây hại; giống vật nuôi ngoài danh mục/gây hại; khoáng sản đặc biệt độc hại; phế liệu nhập khẩu gây ô nhiễm; thiết bị y tế chưa được phép; phụ gia thực phẩm/TPCN/thực phẩm biến đổi gen chưa được phép; vật liệu chứa amiăng nhóm amfibole — Nguồn: https://mini.zalo.me/documents/zalo-mini-app-developer-program-agreement/regulated-products-and-services/#i-hàng-hoá (17 mục). Vi phạm → gỡ app, có thể khoá tài khoản vĩnh viễn (Điều 11). Automatable: yes (partial) — quét keyword/NLP phát hiện mặt hàng cấm rõ ràng.
- [ ] Rà soát KHÔNG có 5 nhóm dịch vụ cấm: mại dâm/buôn người; đánh bạc/gá bạc; điều tra bí mật xâm phạm lợi ích nhà nước/cá nhân; môi giới kết hôn có yếu tố nước ngoài vì lợi nhuận; môi giới nhận con nuôi có yếu tố nước ngoài vì lợi nhuận — Nguồn: regulated-products-and-services/#ii-dịch-vụ. Automatable: partial.
- [ ] KHÔNG được là game/trò chơi điện tử; KHÔNG cạnh tranh trực tiếp với Zalo Ads/Zalo/Báo Mới/Zing MP3/Zing TV — Nguồn: regulated-products-and-services/#iii-các-quy-định-khác. Automatable: partial.
- [ ] Rà soát 7 nhóm hàng hoá hạn chế (súng săn/vũ khí thể thao/công cụ hỗ trợ; hàng chứa phóng xạ; vật liệu nổ công nghiệp/Nitrat Amôn ≥98.5%; hoá chất bảng 2&3; động thực vật hoang dã quý hiếm; thuốc lá/xì gà; rượu bia) + 1 dịch vụ hạn chế (karaoke/vũ trường) — có sẽ **tự động bị hạn chế hiển thị dù đã được duyệt** — Nguồn: regulated-products-and-services/#danh-mục-hàng-hoá-dịch-vụ-hạn-chế-kinh-doanh-trên-zalo-mini-app. Automatable: yes — quét keyword.
- [ ] Đối chiếu danh mục **24 nhóm hàng hoá + 69 nhóm dịch vụ kinh doanh có điều kiện** (xăng dầu, khí đốt, thực phẩm nguy cơ cao, cổ vật, phim/băng đĩa, hoá chất độc, thiết bị y tế, ngư cụ, giống vật nuôi/cây trồng, phân bón, vật liệu xây dựng, than mỏ, thiết bị viễn thông, vàng, dược phẩm/vắc-xin, mỹ phẩm, TPCN, dịch vụ y tế, thuốc, thú y, viễn thông/Internet/bưu chính, điện lực, biểu diễn nghệ thuật, phim, vận tải đa phương thức, bảo hiểm, chứng khoán, xuất khẩu lao động, pháp lý/luật sư, khắc dấu, bảo vệ, lữ hành quốc tế, giết mổ, đại lý bưu chính/viễn thông, xuất bản, quảng cáo, lưu trú, cầm đồ, in ấn, bản đồ, kiểm định ATLĐ, dạy nghề, giới thiệu việc làm, vận tải ô tô/đường sắt/thuỷ/biển, đại lý tàu biển, hải quan, kế toán/kiểm toán/thẩm định giá, xây dựng, cho thuê nhà người nước ngoài, lữ hành nội địa, hướng dẫn viên, giám định thương mại) — Nguồn: regulated-products-and-services/# (mục I & II). Vi phạm → chế tài Điều 11. Automatable: partial.
- [ ] Dược phẩm/vắc-xin/sinh phẩm y tế/hoá chất diệt côn trùng-khuẩn: KHÔNG được có chức năng mua bán trực tiếp (đặt hàng/thanh toán) — Nguồn: regulated-products-and-services/#i-hàng-hoá-2 (ghi chú mục 23). Automatable: yes — quét UI flow/route đặt hàng-thanh toán gắn danh mục dược phẩm.

### B4. Nghĩa vụ hợp đồng nhà phát triển (Điều khoản Dịch vụ)

- [ ] Nhà phát triển thương mại phải có tư cách pháp nhân hợp lệ (doanh nghiệp) hoặc giấy CN ĐK hộ kinh doanh trước khi cung cấp hàng hoá/dịch vụ — Nguồn: developer-program-agreement/#4-sử-dụng-tài-khoản-và-dịch-vụ-của-zalo-mini-app (4.1). Automatable: no.
- [ ] Duy trì thông tin đăng ký chính xác/cập nhật (tên pháp lý, địa chỉ, người đại diện, giấy phép); mọi thay đổi phải cập nhật kịp thời với Zalo — Nguồn: #4 (4.2). Automatable: partial — đối chiếu ngày hết hạn giấy phép với ngày hiện tại.
- [ ] Bắt buộc hiển thị công khai trên Mini App: tên/mã số doanh nghiệp (hoặc CCCD cá nhân), địa chỉ, SĐT liên hệ, mô tả hàng hoá/dịch vụ, số phiên bản, phương thức hỗ trợ/khiếu nại — Nguồn: #5-thẩm-định-và-phê-duyệt-mini-app (5.5.a). Automatable: yes — scan trang "Giới thiệu/Liên hệ" xác nhận đủ 6 trường.
- [ ] Nếu thuê/uỷ quyền bên thứ ba (thiết kế, vận hành, marketing, CSKH, xử lý đơn hàng, thanh toán, vận chuyển, xử lý dữ liệu cá nhân), Nhà phát triển vẫn chịu trách nhiệm cuối cùng, phải ràng buộc bên thứ ba tuân thủ — Nguồn: #8-quyền-và-nghĩa-vụ-của-nhà-phát-triển (8.2.g). Automatable: no.
- [ ] Lưu trữ log giao dịch/vận hành tối thiểu **12 tháng**, sẵn sàng cung cấp khi thẩm định/hậu kiểm/khiếu nại — Nguồn: #8 (8.2.e). Automatable: yes — kiểm tra cấu hình retention log backend.
- [ ] Không điều hướng user ra ngoài Mini App trừ mục đích cung cấp tài liệu (chính sách/điều khoản); mọi link ngoài phải mở được trên trình duyệt thứ ba — Nguồn: #5 (5.5) + #7-các-hành-vi-bị-nghiêm-cấm (7.3). Automatable: yes — quét external link, phân loại + test mở được.
- [ ] Tên Mini App: chỉ viết hoa ký tự đầu/tên riêng/địa danh, không ký tự đặc biệt/emoji, không chứa nhãn hiệu/tên app khác chưa được uỷ quyền, không gây nhầm lẫn — Nguồn: #5 (5.3.1). Automatable: yes.

### B5. Nghĩa vụ dữ liệu cá nhân theo Thoả Thuận Xử Lý Dữ Liệu Công Khai (Nghị định 13/2023/NĐ-CP)

- [ ] Trước khi xử lý bất kỳ dữ liệu cá nhân nào, phải có đầy đủ căn cứ pháp lý và có thể xuất trình cho Zalo khi yêu cầu — Nguồn: developer-program-agreement/public-dpa/#2-nghĩa-vụ-chung-của-bạn-khi-xử-lý-dữ-liệu-trên-nền-tảng (2.1.1). Automatable: no.
- [ ] Không xử lý dữ liệu trẻ em trái pháp luật — cần xác minh chủ thể, xác minh giám hộ, thu thập đồng ý giám hộ, có cơ chế xoá — Nguồn: public-dpa/#2 (2.1.3). Automatable: partial — kiểm tra cơ chế xác minh tuổi/giám hộ trong luồng đăng ký.
- [ ] Ghi/lưu audit log cho MỌI hoạt động xử lý dữ liệu cá nhân, sẵn sàng cung cấp khi yêu cầu — Nguồn: public-dpa/#2 (2.1.5). Automatable: yes.
- [ ] Khi User yêu cầu thực hiện quyền (cung cấp/xoá/hạn chế/phản đối xử lý), phải xử lý VÀ thông báo/phối hợp Zalo **không trễ hơn 72 giờ** — Nguồn: public-dpa/#2 (2.1.6), #3 (3.4), #4 (4.4). Automatable: yes — đo timestamp yêu cầu vs xử lý.
- [ ] Vai trò Bên Kiểm Soát: nếu nghi ngờ vi phạm bảo vệ dữ liệu, thông báo Bộ Công An trong **72 giờ** — Nguồn: public-dpa/#3 (3.5). Automatable: no.
- [ ] Vai trò Bên Xử Lý: nếu nghi ngờ vi phạm, thông báo Zalo Platforms **không trễ hơn 24 giờ** — Nguồn: public-dpa/#4 (4.8). Automatable: yes — theo dõi timestamp phát hiện vs thông báo.
- [ ] Chỉ nhận dữ liệu từ Zalo Platforms trong phạm vi lãnh thổ Việt Nam; chuyển ra nước ngoài phải qua thủ tục pháp lý VN (DTIA) — Nguồn: public-dpa/#2 (2.2.3) + tutorial/update-information-about-compliance-with-decree/#2. Automatable: yes — kiểm tra region server/API endpoint lưu dữ liệu (DNS lookup, cloud region config).
- [ ] Chỉ định Bên Thứ Ba xử lý dữ liệu chuyển giao từ Zalo: phải thông báo NGAY LẬP TỨC cho Zalo và chỉ cho tham gia sau khi Zalo đồng ý — Nguồn: public-dpa/#2 (2.2.4). Automatable: partial — liệt kê third-party SDK/API chạm dữ liệu cá nhân Zalo, đối chiếu danh sách đã khai báo.
- [ ] Biện pháp bảo mật kỹ thuật bắt buộc: mã hoá dữ liệu lưu trữ & truyền tải, hàm băm SHA-256, ẩn danh hoá/che dữ liệu, quản lý khoá mã hoá, theo dõi & vá lỗ hổng — Nguồn: public-dpa/#6-điều-khoản-chung (6.1). Automatable: yes — scan encryption at rest, TLS, thuật toán hash mật khẩu (không MD5/SHA1 trần).
- [ ] Sau khi ngừng vận hành: hoàn trả dữ liệu cho Zalo VÀ xoá không thể khôi phục toàn bộ dữ liệu User trong **24 giờ** (trừ có văn bản đồng ý giữ lại), cung cấp bằng chứng xoá — Nguồn: developer-program-agreement/#5 (5.3.3.d) + #6-quyền-riêng-tư-và-bảo-vệ-dữ-liệu-cá-nhân-người-dùng (6.9). Automatable: partial — kiểm tra job/audit trail xoá dữ liệu tự động.

### B6. Cơ chế cấp quyền/thu hồi đồng ý & xoá dữ liệu cho User

- [ ] Cấu hình "Điều khoản sử dụng" trong trang quản lý Mini App và bật UI xin quyền đồng ý (consent UI) trước khi truy cập dữ liệu cá nhân — Nguồn: https://mini.zalo.me/documents/tutorial/update-information-about-compliance-with-decree/granting-permission-consent/. Automatable: yes — kiểm tra cờ "hiển thị xác nhận cấp quyền" đã bật qua trang quản trị.
- [ ] API nhạy cảm (SĐT, Follow OA, Request Notification...) chỉ gọi SAU KHI có đồng ý rõ ràng, không tự động gọi khi chưa cấp phép — Nguồn: developer-program-agreement/#5 (5.3.3.a). Automatable: yes — trace network call xác nhận thứ tự sau consent event.
- [ ] Khi User từ chối cấp quyền, app KHÔNG được tự đóng/thoát/xoá ứng dụng, và không tiếp tục xử lý dữ liệu của User đó — Nguồn: #5 (5.3.3.b). Automatable: yes — test tương tác: từ chối quyền, quan sát app có tự đóng/crash hay không.
- [ ] Phải có trang "Quản lý quyền" cho phép User tự tắt quyền đã cấp và xoá dữ liệu bất kỳ lúc nào — Nguồn: https://mini.zalo.me/documents/tutorial/update-information-about-compliance-with-decree/revoke-and-remove-user-data/. Automatable: yes — kiểm tra tồn tại + click-test màn "Quản lý quyền".
- [ ] Cấu hình Webhook URL tại mục "Open APIs" để nhận sự kiện User rút đồng ý/xoá dữ liệu, và xử lý sự kiện để tự xoá dữ liệu trên backend riêng — Nguồn: revoke-and-remove-user-data/. Automatable: yes — kiểm tra field Webhook URL đã điền + endpoint phản hồi 2xx với event mẫu.
- [ ] Khi nhận webhook xoá dữ liệu, backend phải **hard-delete thật sự** (không chỉ đánh dấu "inactive") — Nguồn: revoke-and-remove-user-data/ + developer-program-agreement/#6 (6.9). Automatable: partial — kiểm tra code xử lý webhook gọi hard-delete/purge thay vì set flag.

### B7. Nghĩa vụ đối tác trong Chương Trình Đối Tác Giải Pháp (Solution Partner — nếu agency là Solution Partner)

- [ ] Không dùng chứng nhận Đối Tác Giải Pháp theo cách ngụ ý là nhân viên/đại lý Zalo, hoặc Zalo bảo trợ/chịu trách nhiệm dịch vụ, hoặc quan hệ độc quyền — Nguồn: https://mini.zalo.me/documents/solution-partner/policy/#2-sử-dụng-chứng-nhận (mục 4). Automatable: yes — scan trang marketing agency tìm ngôn từ vi phạm.
- [ ] Không chỉnh sửa thiết kế/màu sắc chứng nhận; tài liệu điện tử phải link đúng trang hồ sơ Danh Mục Đối Tác Zalo Mini App — Nguồn: solution-partner/policy/#2 (mục 2–3). Automatable: yes.
- [ ] Thông báo văn bản cho Zalo + khách hàng trước **60 ngày** nếu dự định dừng cung cấp dịch vụ đã chứng nhận — Nguồn: solution-partner/policy/#iv-thông-báo-bắt-buộc (mục 1). Automatable: no.
- [ ] Thông báo văn bản cho Zalo trong **60 ngày** về sáp nhập/mua lại công ty — Nguồn: #iv (mục 2). Automatable: no.
- [ ] Chia sẻ ngay dấu hiệu bất thường về API (giá/kỹ thuật/lượng user/traffic) cho đội Zalo Mini App trong **3 giờ** từ khi phát hiện — Nguồn: #iv (mục 3). Automatable: yes — nếu có monitoring/alerting, đo thời gian alert vs báo cáo.

---

## Nhóm C — Lỗi kỹ thuật (dev/build/runtime)

- [ ] Server API phải trả header `Access-Control-Allow-Origin: https://h5.zdn.vn` chính xác (không wildcard `*` không kiểm tra, không nhiều origin nối dấu phẩy) — Nguồn: https://mini.zalo.me/documents/intro/frequently-solved-issues/#11-cors. Automatable: partial — dynamic test gọi API thật, kiểm tra response header.
- [ ] Server phải trả CORS header cho CẢ preflight `OPTIONS`, không chỉ GET/POST/PUT/DELETE — Nguồn: #một-số-biến-thể-khác-của-cors-bao-gồm. Automatable: partial — dynamic test gửi OPTIONS tới từng endpoint.
- [ ] Không set `Access-Control-Allow-Origin` nhiều giá trị cách nhau dấu phẩy — server phải check origin rồi echo lại đúng 1 giá trị — Nguồn: #ví-dụ-cụ-thể. Automatable: partial.
- [ ] Mọi API call (fetch/axios) bắt buộc `https://` domain hợp lệ SSL còn hạn — cấm gọi bằng IP trực tiếp, cấm `http://` — Nguồn: #12-gọi-api-không-có-domain-không-có-https-hoặc-domain-hết-hạn-ssl. Automatable: yes — regex scan `fetch(`/`axios(` với literal `http://` hoặc IP.
- [ ] Không import ảnh/asset qua path string trỏ `public` (`src="/coffee.jpg"`) — phải dùng `import` ES module (`import coffee from "./coffee.jpg"`) — Nguồn: #3-hình-ảnh-không-hiển-thị. Automatable: yes — AST scan JSX/TSX tìm `src="/..."` literal string không qua import.
- [ ] Cấm gọi trực tiếp từ client các API Server-to-Server (decode token→SĐT/vị trí, gửi thông báo OA, toàn bộ nhóm OpenAPI, `getOrderStatus`/`updateOrderStatus` của Checkout SDK) — chỉ gọi từ backend — Nguồn: #4-gọi-các-api-server-server-từ-mini-app. Automatable: yes — static scan client code tìm gọi các endpoint này hoặc chuỗi "app_secret"/"private_key" trong bundle.
- [ ] Không hardcode app secret/private key/access token dài hạn trong client bundle — Nguồn: #4 (suy luận). Automatable: yes — secret-scan trên build output.
- [ ] API cần môi trường Zalo thật (`getAccessToken`, `createOrder`...) phải test qua Device Mode, không phải browser dev server — Nguồn: #5-api-được-gọi-thành-công-nhưng-không-có-dữ-liệu-trong-quá-trình-phát-triển. Automatable: no.
- [ ] Trước khi submit, xin cấp quyền cho Mini App ID nếu dùng: `getPhoneNumber`, `getLocation`, `openMediaPicker`, `requestCameraPermission`, `keepScreen`, nhóm Native Storage — thiếu quyền chỉ lỗi với user thật ngoài Developer/Admin (QA nội bộ không phát hiện) — Nguồn: #7-lỗi-chỉ-xảy-ra-với-người-dùng-ngoài-tập-developeradmin. Automatable: yes — scan code gọi các API này, đối chiếu quyền đã khai báo.
- [ ] KHÔNG hiển thị form đăng nhập truyền thống (username/password) trừ (1) app nội bộ (trường/công ty) VÀ (2) chỉ truy cập qua Deeplink/QR/Shortcut ghim màn hình — Nguồn: #10-không-tìm-thấy-mini-app-trên-zalo-mini-app-store-hoặc-thanh-tìm-kiếm-của-zalo. Vi phạm → app biến mất khỏi Store dù vẫn Live. Automatable: partial — browser test trạng thái chưa đăng nhập.
- [ ] Quota deploy: tối đa **300 lần/tháng** (Development), tối đa **60 lần/tháng** (Testing) — Nguồn: #13-you-have-reached-your-30-day-deployment-limit-please-try-again-later. Automatable: partial — audit CI/CD trigger frequency.
- [ ] Giới hạn dung lượng: tổng app tối đa **10MB**, mỗi file tối đa **3MB** — Nguồn: #14-the-file-size-is-too-large. Automatable: yes — scan kích thước file build output.
- [ ] CI/CD: `ZALO_APP_SECRET`/`ZALO_REFRESH_TOKEN` phải khớp đúng `ZALO_APP_ID` (không lấy nhầm token của Zalo App khác) — Nguồn: #15-lỗi-cicd. Automatable: partial.
- [ ] CI/CD: không nhầm `MINI_APP_ID` với `ZALO_APP_ID` — Nguồn: #15. Automatable: no.
- [ ] CI/CD: `ZMP_TOKEN` trong `.env` không bị ghi đè bởi env var cùng tên trong CI runner — Nguồn: #15. Automatable: yes — scan CI workflow YAML tìm biến `ZMP_TOKEN` set ở job/runner level.
- [ ] Build target mặc định ES2015 — không dùng tính năng JS không tương thích ngược (async generator, for-await) mà không xử lý; nâng `target` lên `esnext` trong vite.config nếu cần, hoặc thay lib tương thích hơn — Nguồn: #16-lỗi-es2015. Automatable: yes — chạy `vite build` thử, grep log lỗi ES2015 transform.
- [ ] Không dùng `openWebview` để mở PDF trực tiếp (hành vi khác nhau Android/iOS tuỳ `Content-Disposition`) — dùng `react-pdf@5.x` để hiển thị PDF trong UI (không dùng bản ≥6) — Nguồn: #17-viewdownload-file-pdf. Automatable: partial — scan `openWebview` trỏ `.pdf` + version `react-pdf`.
- [ ] Cocos Creator: import `zmp-sdk` phải kèm `import "reflect-metadata"` + dùng `SDKCreator` — Nguồn: #18-import-zmp-sdk-từ-cocos-creator. Automatable: yes — scan file .ts thiếu `reflect-metadata` khi có `from "zmp-sdk"`.
- [ ] TailwindCSS + Device Mode (không Kết nối trực tiếp): dùng Vite `^2.9+`, không dùng 2.6.x — Nguồn: #19-tailwindcss-không-apply-style-mới-khi-sử-dụng-chế-độ-device. Automatable: yes — scan package.json version vite khi có tailwindcss.
- [ ] Máy dev dùng Kết nối trực tiếp (Device Mode) phải có `adb` trong PATH — Nguồn: #20-adb-is-not-recognized-hoặc-command-not-found-adb-khi-sử-dụng-kết-nối-trực-tiếp-với-device-mode. Automatable: yes — `adb version` check trên máy dev/CI.
- [ ] Trước khi báo lỗi lạ, xác nhận dùng bản MỚI NHẤT: ZMP SDK, ZaUI, Zalo Mini App CLI, Extension, app Zalo trên điện thoại test — Nguồn: #21-các-lỗi-khác. Automatable: yes — so version package.json với npm registry.
- [ ] `app-config.json` phải ở root project, bắt buộc có `app.title` (string) — Nguồn: https://docs.zaloplatforms.com/docs/MA/devtools/app-config. Automatable: yes.
- [ ] Field yêu cầu minimum SDK/Zalo version cao hơn (`statusBar`, `actionBarHidden`, `hideAndroidBottomNavigationBar`, `hideIOSSafeAreaBottom` → API ≥2.25.0/Zalo ≥23.02.01.r2; `selfControlLoading` → API ≥2.17.0) phải kiểm tra tương thích ngược — Nguồn: app-config docs (bảng Minimum Version). Automatable: yes — đối chiếu key dùng với bảng minimum-version.
- [ ] Nếu `selfControlLoading: true`, code BẮT BUỘC gọi `closeLoading` — thiếu sẽ treo Splash Loading vĩnh viễn — Nguồn: app-config docs. Automatable: yes — grep source có gọi `closeLoading` khi flag bật.

---

## Nhóm D — UI/UX, điều hướng & xác thực người dùng

### D1. Điều hướng & thanh trạng thái

- [ ] Không tự ý ẩn/loại bỏ thanh điều hướng hệ thống — Nguồn: https://mini.zalo.me/documents/intro/zalo-mini-app-design-guidelines/#2-rõ-ràng-mạch-lạc. Automatable: partial.
- [ ] Android: giữ nút "trở lại" ở góc trên-trái cho trang phụ, không di chuyển vị trí — Nguồn: cùng trang. Automatable: partial — screenshot + kiểm tra vị trí custom back button.
- [ ] iOS: không chặn thao tác vuốt từ mép trái ("swipe back") bằng overlay/`preventDefault` — Nguồn: cùng trang. Automatable: partial — dynamic test swipe-back trên simulator iOS + scan `preventDefault()` trên touch listener toàn màn hình.
- [ ] Không đặt button/thông tin quan trọng bị che khuất dưới Zalo Mini App menu (góc trên-phải, cố định, không tuỳ chỉnh được) — Nguồn: cùng trang. Automatable: partial — screenshot test vùng góc trên-phải (~44x44px).
- [ ] Theme sáng/tối phải chọn đúng phương án màu cho Zalo Mini App menu, đủ độ tương phản — Nguồn: cùng trang. Automatable: partial.
- [ ] Bottom navigation (tab bar): không quá **4 tab** — Nguồn: cùng trang. Automatable: yes — đếm tab trong app-config/router.
- [ ] Touch target trong khoảng **7mm–9mm** quy đổi theo pixel density — Nguồn: #3-sự-tiện-lợi-và-thanh-lịch. Automatable: partial — đo width/height CSS control, so ngưỡng ~28–34px@96dpi.

### D2. Trạng thái tải trang, phản hồi kết quả và thông báo lỗi

- [ ] Không ẩn/thay thế/tuỳ biến splash/loading mặc định của nền tảng (logo + tên thương hiệu) — Nguồn: #2-rõ-ràng-mạch-lạc. Automatable: partial.
- [ ] Mọi thao tác có độ trễ phải có phản hồi trạng thái rõ ràng (loading indicator) — Nguồn: cùng trang. Automatable: partial — mock delay, kiểm tra UI hiển thị loading state.
- [ ] Phải thông báo rõ khi lỗi/mất kết nối mạng (không màn trắng/im lặng) — Nguồn: cùng trang. Automatable: partial — mock lỗi API/offline, xác nhận UI hiển thị modal/toast lỗi.
- [ ] Khi hoàn tất luồng quan trọng, phải có trang/màn hình kết quả hướng dẫn bước tiếp theo — Nguồn: cùng trang. Automatable: partial.

### D3. Nhập liệu & khả năng sử dụng trên di động

- [ ] Ưu tiên dùng API sẵn có (vị trí, camera, gợi ý chọn) thay vì bắt gõ tay — Nguồn: #3-sự-tiện-lợi-và-thanh-lịch. Automatable: partial — scan form input tự do cho trường có thể thay bằng API.

### D4. Đăng nhập / xác thực người dùng (Zalo Account Login)

- [ ] Luồng đăng nhập chuẩn 3 bước: (1) `getAccessToken` (zmp-sdk client), (2) gửi token về server → server gọi Zalo Open API lấy Zalo Profile, (3) dùng Zalo Profile tạo/đăng nhập tài khoản hệ thống — Nguồn: https://mini.zalo.me/documents/intro/authen-user/#login-process. Automatable: partial — scan `getAccessToken` + xác nhận không gọi `graph.zalo.me` trực tiếp từ client.
- [ ] Backend gọi `GET https://graph.zalo.me/v2.0/me` phải kèm header/param `appsecret_proof` (bắt buộc từ 01/01/2024) — Nguồn: authen-user/#hướng-dẫn-truy-xuất-zalo-profile-từ-access-token-qua-zalo-open-api-step-21. Automatable: yes — scan backend code có tính `appsecret_proof` (HMAC-SHA256).
- [ ] Field `id` từ `/v2.0/me` phải dùng làm định danh duy nhất của user theo mỗi Zalo App ID — không tự suy đoán ID khác — Nguồn: cùng trang. Automatable: partial.
- [ ] **Không dùng đăng nhập username/password tự tạo làm phương thức chính** khi có thể định danh qua Zalo — ưu tiên `getAccessToken` + Zalo Profile, trừ lý do nghiệp vụ chính đáng (vẫn phải liên kết tài khoản Zalo) — Nguồn: authen-user/#sử-dụng-tài-khoản-zalo-đăng-nhập-và-định-danh-tài-khoản. Automatable: partial — scan UI form `type="password"` không kèm luồng Zalo Login.
- [ ] Định danh bằng SĐT: dùng `getPhoneNumber` (zmp-sdk), không tự thu thập qua form nhập tay khi có thể dùng API — Nguồn: authen-user/#hướng-dẫn-liên-kết-tài-khoản-cho-các-hệ-thống-sử-dụng-số-điện-thoại-để-định-danh. Automatable: partial.
- [ ] Nếu SĐT chỉ cần cho tính năng cụ thể (đặt hàng, đăng ký...), **cấm** xin ngay khi vừa vào app — chỉ gọi `getPhoneNumber` đúng lúc user bắt đầu dùng tính năng cần nó — Nguồn: authen-user/#trường-hợp-chỉ-yêu-cầu-cung-cấp-số-điện-thoại-khi-sử-dụng-một-số-tính-năng-nhất-định (có minh hoạ "cách dùng KHÔNG hợp lệ"). Automatable: partial — dynamic test: fresh state, xác nhận không gọi `getPhoneNumber` ngay ở màn hình đầu.
- [ ] Nếu SĐT bắt buộc để dùng app: phải có UI Onboarding giải thích rõ lý do bắt buộc + mục đích sử dụng, TRƯỚC khi gọi API xin quyền — Nguồn: authen-user/#trường-hợp-bắt-buộc-cung-cấp-số-điện-thoại-để-sử-dụng-ứng-dụng. Automatable: partial.

### D5. Điểm truy cập (entry point) & điều hướng liên-app

- [ ] Link vào Mini App từ ngoài Zalo phải đúng cấu trúc `https://zalo.me/s/{appId}/?variable=value` — Nguồn: https://mini.zalo.me/documents/intro/mini-app-navigation-mechanisms/#mở-zalo-mini-app-từ-ứng-dụng-bên-ngoài-zalo, entry-point-access/#với-người-dùng-ngoài-nền-tảng-zalo. Automatable: yes — regex kiểm tra link marketing/landing page.
- [ ] Mở Mini App khác: dùng `openMiniApp` (zmp-sdk) với xử lý `success`/`fail`, không thao túng URL/`window.location` — Nguồn: mini-app-navigation-mechanisms/#mở-zalo-mini-app-từ-một-zalo-mini-app-khác. Automatable: yes.
- [ ] Mở website ngoài: dùng `openWebview` (zmp-sdk), không `window.open`/redirect trực tiếp — Nguồn: mini-app-navigation-mechanisms/#mở-webview-trong-zalo-mini-app. Automatable: yes.
- [ ] Tạo shortcut màn hình chính: dùng `createShortcut` (zmp-sdk) chuẩn, không tự chế PWA/manifest install — Nguồn: entry-point-access/#với-người-dùng-trên-nền-tảng-zalo. Automatable: yes.

---

## Nhóm E — Quy trình nộp duyệt & khai báo quyền (Submission & Permissions)

### E1. Tài khoản & cấu trúc ứng dụng nhà phát triển

- [ ] Đã đăng ký tài khoản + tạo Ứng dụng (App) trên Zalo for Developers trước khi tạo Mini App — Nguồn: https://mini.zalo.me/documents/intro/mini-app-account/. Automatable: no.
- [ ] Hiểu rõ: 1 Ứng dụng Zalo Platform → nhiều Mini App; User ID mã hoá theo từng Ứng dụng cha (khác App cha → ID khác nhau cho cùng user) — không dùng chung userId cross-app — Nguồn: cùng trang. Automatable: partial — scan code so sánh/lưu userId cross-app.
- [ ] Mini App chỉ gọi Open API qua đúng Ứng dụng cha tương ứng — Nguồn: cùng trang. Automatable: yes — grep appId/secret hard-code đối chiếu `.env`.

### E2. Deploy & thử nghiệm trước khi nộp duyệt

- [ ] Chọn đúng chế độ deploy trước khi test: **Development** (QR only) vs **Testing** (bản lưu DB, trả cho tập tester) — Nguồn: https://mini.zalo.me/documents/intro/testing-on-zalo/#phát-hành-phiên-bản-thử-nghiệm-trên-zalo. Automatable: partial.
- [ ] Trước khi gửi xét duyệt, phiên bản phải ở trạng thái **Testing** trên Mini App Center — Nguồn: https://mini.zalo.me/documents/intro/public-mini-app/. Automatable: no.
- [ ] Đã test đầy đủ qua QR (Development)/tập tester (Testing), bao gồm Hot Reload trực tiếp trên Zalo thật (`zmp start`) — không chỉ test trên browser — Nguồn: testing-on-zalo/#chạy-test-trên-ứng-dụng-zalo-của-bạn-với-chế-độ-hot-reload. Automatable: no.

### E3. Danh sách quyền (permission) — 4 nhóm chính thức

**Nhóm 1 — User Device Permission** (Nguồn: https://mini.zalo.me/documents/intro/request-permission/#2-danh-sách-quyền)
- [ ] Mở màn hình cuộc gọi Native — **Mặc định**. Automatable: yes.
- [ ] Mở màn hình tin nhắn Native — **Mặc định**. Automatable: yes.
- [ ] Shortcut (tạo lối tắt màn hình chính) — **Zalo** (cần xin duyệt). Automatable: partial.
- [ ] Hiển thị toast — **Mặc định**. Automatable: yes.
- [ ] Lấy thông tin network device — **Zalo** (cần xin duyệt). Automatable: partial.
- [ ] Giữ màn hình luôn bật (`keepScreen`) — **Zalo** (cần xin duyệt). Automatable: partial.
- [ ] Native Storage — **Zalo** (cần xin duyệt). Automatable: partial.
- [ ] Lưu ảnh vào điện thoại — **Zalo** (cần xin duyệt). Automatable: partial.
- [ ] Ẩn bàn phím — **Mặc định**. Automatable: yes.
- [ ] Rung thiết bị — **Zalo** (cần xin duyệt). Automatable: partial.
- [ ] Vị trí (`getLocation`) — **Zalo & User** (cần cả Zalo duyệt lẫn user đồng ý runtime). Automatable: partial.
- [ ] Camera (`requestCameraPermission`) — **Zalo** (cần xin duyệt trước; thiết bị hỏi user sau). Automatable: partial.

**Nhóm 2 — User Information Permission** (Nguồn: request-permission/#user-information-permission)
- [ ] Số điện thoại (`getPhoneNumber`) — **Zalo & User**; quyền có hiệu lực giới hạn thời gian rồi bị thu hồi — code phải xử lý hết hạn/từ chối. Automatable: yes/partial — grep gọi API + catch lỗi permission-denied/expired.

**Nhóm 3 — Zalo Permission** (Nguồn: request-permission/#zalo-permission)
- [ ] Mở chia sẻ lên nhật ký Zalo — **Mặc định**. Automatable: yes.
- [ ] Mở Scan QR Code trên Zalo — **Zalo** (cần xin duyệt). Automatable: partial.
- [ ] Mở Share với bạn bè trên Zalo — **Mặc định**. Automatable: yes.
- [ ] Hiển thị QR OA — **Mặc định**. Automatable: yes.
- [ ] Yêu cầu theo dõi/bỏ theo dõi OA — **Mặc định**. Automatable: yes.
- [ ] Màn hình chọn bạn bè Zalo — **Mặc định**. Automatable: yes.
- [ ] Mở profile User/OA — **Mặc định**. Automatable: yes.
- [ ] Mở cửa sổ chat trên Zalo — **Mặc định**. Automatable: yes.

**Nhóm 4 — Mini App Permission** (Nguồn: request-permission/#mini-app-permission)
- [ ] Thay đổi màu navigation bar — **Mặc định**. Automatable: yes.
- [ ] Thay đổi title navigation bar — **Mặc định**. Automatable: yes.
- [ ] Mở Mini App khác — **Mặc định**. Automatable: yes.
- [ ] Đóng Mini App — **Mặc định**. Automatable: yes.

- [ ] **Quy tắc chung**: quyền cột "Cần sự cho phép từ" = Zalo hoặc Zalo & User BẮT BUỘC phải được duyệt trước khi dùng ổn định ở Testing/Production; quyền Mặc định dùng ngay không cần xin — Nguồn: request-permission/#2-danh-sách-quyền. Automatable: partial — grep toàn bộ API 4 nhóm, đối chiếu kết quả `getAppPermissions` (E5) để lập danh sách "đang dùng nhưng chưa APPROVED".

### E4. Quy trình khai báo & xin duyệt quyền

- [ ] Quyền cần "Zalo" cấp: vào Mini App Center → Quyền Mini App → chọn quyền → nhập mô tả lý do + hình ảnh minh hoạ (+ consent text tuỳ chọn) → Gửi xét duyệt — Nguồn: https://mini.zalo.me/documents/intro/request-permission/#hướng-dẫn-xin-cấp-quyền-từ-zalo-mini-app. Automatable: no (UI thủ công; có thể automation qua Partner API — xem E5).
- [ ] Yêu cầu cấp quyền được xét duyệt CÙNG LÚC với xét duyệt phiên bản mới (không tách rời) — Nguồn: cùng trang. Automatable: no.
- [ ] Kết quả xét duyệt thông báo qua CẢ OA lẫn Mini App Center — theo dõi cả 2 kênh — Nguồn: #6-sau-khi-bộ-phận-xét-duyệt-xong-sẽ-có-thông-báo-qua-oa--mini-app-center-cho-nhà-phát-triển. Automatable: no.
- [ ] Quyền cần "User" cấp (SĐT, vị trí...): chỉ xin đúng lúc, đúng ngữ cảnh sử dụng — không xin tràn lan lúc mở app — Nguồn: #xin-quyền-đúng-ngữ-cảnh. Automatable: partial — phát hiện pattern gọi API xin quyền trong useEffect/hàm khởi tạo trang đầu.

### E5. Quản lý quyền qua Partner API (tự động hoá cho agency)

- [ ] API `getAppPermissions` (cần `appId`) trả trạng thái từng quyền: `UNREGISTERED`/`WAITING_APPROVAL`/`APPROVED` — dùng để CI/CD kiểm tra trước khi build production — Nguồn: https://mini.zalo.me/documents/open-apis/partner/app-permission/#1-lấy-danh-sách-permission. Automatable: yes.
- [ ] API `requestAppPermission` (`appId`, `permissions[]` gồm `permissionId`+`consentText` tuỳ chọn+`note`) chỉ áp dụng permission `UNREGISTERED`; vòng đời `UNREGISTERED→WAITING_APPROVAL→APPROVED`; kết quả có thể **thành công một phần** — PHẢI kiểm tra field `successPermissions` — Nguồn: app-permission/#2-đăng-ký-permission. Automatable: yes.
- [ ] API `requestPublishMiniApp` bắt buộc `miniAppId`, `versionId`, và **`description` là trường bắt buộc** — Nguồn: https://mini.zalo.me/documents/open-apis/partner/request-publish-mini-app/#parameters. Automatable: yes — grep CI script kiểm tra `description` non-empty khi gọi.
- [ ] API `publishMiniApp` (`miniAppId`, `versionId`) chỉ dùng được SAU KHI phiên bản đã **Đã duyệt** — gọi sớm sẽ lỗi — Nguồn: https://mini.zalo.me/documents/open-apis/partner/publish-mini-app/. Automatable: yes — kiểm tra CI không gọi `publishMiniApp` ngay sau `requestPublishMiniApp` mà không chờ webhook.
- [ ] Webhook `versions.review.done`: payload `event, appId, versionId, status (0=duyệt,-1=reject), description, timestamp`, có header `X-ZEvent-Signature` cần verify — Nguồn: https://mini.zalo.me/documents/open-apis/partner/event-review-mini-app/. Automatable: yes — grep webhook handler verify signature + xử lý rẽ nhánh status=-1 + không gọi `publishMiniApp` khi status≠0.
- [ ] State machine đúng: **Testing → Chờ xét duyệt → Đã duyệt/Reject** — Nguồn: public-mini-app/ + event-review-mini-app/. Automatable: yes — kiểm tra release script/CI theo đúng transition.

### E6. Nội dung/tiêu chí khi nộp phiên bản xét duyệt

- [ ] Tên/Logo/Mô tả đúng chức năng thực tế, nhất quán, không vi phạm bản quyền, không nội dung cấm — Nguồn: https://mini.zalo.me/documents/intro/public-mini-app/. Automatable: no.
- [ ] Category khai báo phải phù hợp danh mục đã đăng ký khi tạo app — Nguồn: cùng trang. Automatable: partial.
- [ ] Tính năng đúng mô tả đã khai, không điều hướng bên thứ 3 chưa được Zalo chấp thuận — Nguồn: cùng trang. Automatable: yes — grep `window.open`/deep link ngoài.
- [ ] Không nội dung khuyến khích chia sẻ/tải app riêng — Nguồn: cùng trang. Automatable: partial — text scan "tải app"/"download app".
- [ ] Không nội dung sai lệch/gian lận/lừa đảo/giả mạo/cấm pháp luật — Nguồn: cùng trang. Automatable: no.
- [ ] Không quảng cáo/kiếm tiền chưa được Zalo chấp thuận — Nguồn: cùng trang. Automatable: yes — grep SDK ads/thanh toán.
- [ ] Không mua/bán vật phẩm ảo, nội dung số trái phép — Nguồn: cùng trang. Automatable: partial.
- [ ] Hoạt động ổn định — không crash, không gây crash Zalo App — Nguồn: cùng trang. Automatable: partial — smoke test + kiểm tra error boundary.
- [ ] Đạt chuẩn performance & thời gian load Zalo (xem ngưỡng cụ thể ở Nhóm A8: LCP<2.5s, PageLoad<1.5s) — Nguồn: cùng trang. Automatable: partial.
- [ ] Đạt chuẩn UI/UX theo quy chuẩn Zalo (xem Nhóm D) — Nguồn: cùng trang. Automatable: no.
- [ ] Đảm bảo quyền riêng tư/bảo mật, không mã độc/link mã độc — Nguồn: cùng trang. Automatable: partial — dependency vulnerability scan.
- [ ] Định danh user theo chuẩn Authentication Zalo cung cấp (xem Nhóm D4), không tự chế cơ chế thay thế — Nguồn: cùng trang. Automatable: yes/partial.
- [ ] Trang `public-mini-app` chỉ là TÓM TẮT — bản đầy đủ nằm ở Thỏa Thuận Chương Trình Zalo Mini App (Nhóm B) — Nguồn: public-mini-app/ (dòng "Lưu ý"). Automatable: no.

---

## Nhóm F — Cộng đồng, thông báo & điều khoản bổ sung

> Trang cộng đồng `https://miniapp.zaloplatforms.com/community` không có nội dung tĩnh render sẵn (cần login/JS) — không trích xuất được rule cụ thể. Kênh hỗ trợ công khai: nhóm Facebook chính thức `https://www.facebook.com/groups/zalominiapp`. Các mục dưới đây lấy từ trang giới thiệu/getting-started, không trùng lặp Nhóm A/B.

- [ ] Tổng dung lượng gói Mini App (mã nguồn + asset đóng gói) phải nhỏ hơn **10MB** — Nguồn: https://mini.zalo.me/documents/intro/what-is-miniapp/#dễ-dàng-phát-triển. Vượt giới hạn → build/deploy/submit bị chặn ngay ở bước đóng gói. Automatable: yes — script đo tổng size thư mục build sau khi zip đúng định dạng nộp.
- [ ] Mini App phải được xác thực trước khi phát hành: qua Zalo OA đã duyệt HOẶC giấy tờ pháp lý doanh nghiệp — Nguồn: https://mini.zalo.me/documents/intro/getting-started/#2-xác-thực-mini-app. Automatable: partial — nhắc checklist thủ công.
- [ ] Mọi permission (truy cập hệ thống hoặc dữ liệu user) phải khai báo & được Zalo duyệt trước khi dùng thực tế — nhắc lại nguyên tắc nền tảng áp dụng toàn vòng đời app — Nguồn: https://mini.zalo.me/documents/intro/what-is-miniapp/#bảo-mật-và-quyền-hạn. Automatable: partial — scan code đối chiếu app-config.json.
- [ ] Sau khi tạo Mini App (tên, ID, thông tin cơ bản), mọi thay đổi thông tin phải qua ticket hỗ trợ + chờ xác nhận — không tự sửa trực tiếp; kiểm tra kỹ trước khi tạo — Nguồn: https://mini.zalo.me/documents/intro/getting-started/#12-tạo-mini-app-trong-zalo-app. Automatable: no.

---

## Phụ lục — Nguồn tài liệu tham khảo đầy đủ

- Chính sách kiểm duyệt: https://mini.zalo.me/documents/zalo-mini-app-censorship-policy/
- Thỏa thuận Chương trình Nhà phát triển: https://mini.zalo.me/documents/zalo-mini-app-developer-program-agreement/
  - Xác thực Mini App (KYB/eKYC): .../mini-app-verification/
  - Thỏa thuận xử lý dữ liệu công khai (DPA): .../public-dpa/
  - Danh mục hàng hoá/dịch vụ có điều kiện: .../regulated-products-and-services/
- Chính sách Đối tác Giải pháp: https://mini.zalo.me/documents/solution-partner/policy/
- Tuân thủ Nghị định 13 (dữ liệu cá nhân): https://mini.zalo.me/documents/tutorial/update-information-about-compliance-with-decree/
  - Cấp quyền & consent: .../granting-permission-consent/
  - Thu hồi & xoá dữ liệu user: .../revoke-and-remove-user-data/
- Lỗi kỹ thuật thường gặp: https://mini.zalo.me/documents/intro/frequently-solved-issues/
- Cấu hình app-config.json: https://docs.zaloplatforms.com/docs/MA/devtools/app-config
- Thiết kế/UI-UX guidelines: https://mini.zalo.me/documents/intro/zalo-mini-app-design-guidelines/
- Cơ chế điều hướng Mini App: https://mini.zalo.me/documents/intro/mini-app-navigation-mechanisms/
- Entry point / truy cập từ ngoài: https://mini.zalo.me/documents/intro/entry-point-access/
- Xác thực người dùng (Zalo Login): https://mini.zalo.me/documents/intro/authen-user/
- Xin cấp quyền (permission): https://mini.zalo.me/documents/intro/request-permission/
- Publish Mini App / tiêu chí duyệt: https://mini.zalo.me/documents/intro/public-mini-app/
- Testing trên Zalo: https://mini.zalo.me/documents/intro/testing-on-zalo/
- Tài khoản Mini App: https://mini.zalo.me/documents/intro/mini-app-account/
- Partner API — quản lý quyền: https://mini.zalo.me/documents/open-apis/partner/app-permission/
- Partner API — sự kiện xét duyệt: https://mini.zalo.me/documents/open-apis/partner/event-review-mini-app/
- Partner API — gửi yêu cầu xét duyệt: https://mini.zalo.me/documents/open-apis/partner/request-publish-mini-app/
- Partner API — publish: https://mini.zalo.me/documents/open-apis/partner/publish-mini-app/
- Giới thiệu Mini App: https://mini.zalo.me/documents/intro/what-is-miniapp/
- Bắt đầu / xác thực ban đầu: https://mini.zalo.me/documents/intro/getting-started/
- Checkout SDK: https://mini.zalo.me/documents/checkout-sdk/
