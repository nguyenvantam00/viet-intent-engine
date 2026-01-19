# demo_chatbot.py
import viet_intent
import time

class VietnameseChatbot:
    def __init__(self):
        self.engine = viet_intent.IntentEngine()
        self.running = True

    def get_response(self, intent, entities, confidence):
        """Tạo phản hồi dựa trên intent"""
        responses = {
            "greeting": [
                "Xin chào! Tôi có thể giúp gì cho bạn?",
                "Chào bạn! Rất vui được gặp bạn!",
                "Hi! Bạn cần tôi giúp gì không?"
            ],
            "order_food": [
                "Bạn muốn đặt món gì ạ?",
                "Món nào bạn muốn đặt?",
                "Tôi có thể giúp bạn đặt đồ ăn!"
            ],
            "ask_price": [
                "Bạn muốn hỏi giá sản phẩm nào?",
                "Sản phẩm nào bạn muốn biết giá?",
                "Tôi có thể giúp bạn tra giá!"
            ],
            "ask_time": [
                f"Hiện tại là {time.strftime('%H:%M:%S')}",
                f"Bây giờ là {time.strftime('%H giờ %M phút')}",
                "Một giây để tôi xem giờ..."
            ],
            "unknown": [
                "Xin lỗi, tôi chưa hiểu ý bạn.",
                "Bạn có thể nói rõ hơn được không?",
                "Tôi chưa được học cách trả lời câu này."
            ]
        }

        import random
        if intent in responses:
            return random.choice(responses[intent])
        return responses["unknown"][0]

    def run(self):
        print("🤖 Vietnamese Chatbot (Type 'quit' to exit)")
        print("=" * 50)

        while self.running:
            try:
                # Nhập câu từ người dùng
                user_input = input("\n👤 You: ").strip()

                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("🤖 Chatbot: Tạm biệt! Hẹn gặp lại!")
                    self.running = False
                    continue

                if not user_input:
                    continue

                # Phát hiện intent
                result = self.engine.detect(user_input)

                # Tạo phản hồi
                response = self.get_response(
                    result.intent,
                    result.entities,
                    result.confidence
                )

                # Hiển thị kết quả
                print(f"🤖 Chatbot: {response}")
                print(f"   [Intent: {result.intent}, Confidence: {result.confidence:.2f}]")
                if result.entities:
                    print(f"   [Entities: {result.entities}]")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                self.running = False
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    bot = VietnameseChatbot()
    bot.run()
