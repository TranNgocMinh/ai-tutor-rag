SCAFFOLDING = {

    1: """
MỨC 1 — GỢI Ý ĐỊNH HƯỚNG

- Không đưa đáp án hoàn chỉnh.
- Không viết code hoàn chỉnh.
- Chỉ xác định kiến thức liên quan.
- Đưa tối đa 2 manh mối.
- Đặt 1 câu hỏi dẫn dắt.
""",

    2: """
MỨC 2 — GỢI Ý CHIẾN LƯỢC

- Giải thích hướng giải.
- Có thể dùng pseudocode.
- Không đưa code hoàn chỉnh.
- Yêu cầu sinh viên tự làm bước tiếp theo.
""",

    3: """
MỨC 3 — KHUNG CODE

- Có thể đưa skeleton code.
- Dùng TODO hoặc ...
- Không hoàn thành toàn bộ bài.
- Chỉ rõ phần sinh viên phải tự viết.
""",

    4: """
MỨC 4 — SỬA LỖI CÓ MỤC TIÊU

- Có thể sửa đoạn code gây lỗi.
- Giải thích nguyên nhân.
- Đưa cách kiểm tra.
- Không làm phần không liên quan.
""",

    5: """
MỨC 5 — LỜI GIẢI CÓ GIẢI THÍCH

- Có thể đưa lời giải đầy đủ.
- Phải giải thích phần quan trọng.
- Cuối cùng đưa câu hỏi biến thể.
"""
}


def clamp_level(level):

    return max(
        1,
        min(
            5,
            int(level)
        )
    )
