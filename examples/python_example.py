import viet_intent

def main():
    # Khởi tạo engine
    engine = viet_intent.IntentEngine()

    # Khởi tạo với model mặc định
    if not engine.initialize():
        print("Không thể khởi tạo engine!")
        return

    # Thêm intent tùy chỉnh
    engine.add_intent(
        "book_hotel",
        ["đặt phòng khách sạn", "tôi muốn book phòng", "đặt phòng nghỉ"],
        "Bạn muốn đặt phòng loại nào ạ?"
    )

    # Phát hiện ý định
    test_sentences = [
        "xin chào bạn",
        "tôi muốn đặt món phở",
        "cho hỏi giá bánh mì",
        "mấy giờ rồi bạn ơi",
        "đặt phòng khách sạn giúp tôi"
    ]

    for text in test_sentences:
        result = engine.detect(text)
        print(f"\nCâu: '{text}'")
        print(f"Ý định: {result.intent} ({result.confidence:.2f})")
        if result.entities:
            print(f"Thực thể: {result.entities}")
        if result.response_pattern:
            print(f"Phản hồi: {result.response_pattern}")

if __name__ == "__main__":
    main()
