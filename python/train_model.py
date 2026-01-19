import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

training_data = {
    "greeting": [
        "xin chào", "chào bạn", "chào anh", "chào chị", "chào em",
        "chào ông", "chào bà", "chào cô", "chào chú", "chào mọi người",
        "chào quý khách", "hello", "hi", "chao", "chao ban", "chao anh",
        "chao chi", "chao em", "chao ong", "chao ba", "chao co", "chao chu",
        "chao moi nguoi", "chao quy khach", "helo", "hí", "chao buoi sang",
        "chao buoi chieu", "chao buoi toi", "chào buổi sáng", "chào buổi chiều",
        "chào buổi tối", "good morning", "good afternoon", "good evening",
        "chuc mung", "chúc mừng", "rat vui duoc gap ban", "rất vui được gặp bạn"
    ],

    "order_food": [
        "tôi muốn đặt món", "cho tôi đặt đồ ăn", "tôi muốn gọi món",
        "đặt đồ ăn giúp tôi", "cho tôi order món", "tôi muốn order đồ ăn",
        "đặt món ăn", "gọi món", "toi muon dat mon", "cho toi dat do an",
        "toi muon goi mon", "dat do an giup toi", "cho toi order mon",
        "toi muon order do an", "dat mon an", "goi mon", "muon an pho",
        "muốn ăn phở", "dat ban", "đặt bàn", "cho toi mot suat com",
        "cho tôi một suất cơm", "dat pizza", "đặt pizza", "order do uong",
        "order đồ uống", "toi can dat mon an", "tôi cần đặt món ăn"
    ],

    "ask_price": [
        "bao nhiêu tiền", "giá bao nhiêu", "có giá không", "chi phí thế nào",
        "bao nhieu tien", "gia bao nhieu", "co gia khong", "chi phi the nao",
        "giá cả thế nào", "giá như thế nào", "tính tiền thế nào", "gia ca the nao",
        "gia nhu the nao", "tinh tien the nao", "phi bao nhieu", "phí bao nhiêu",
        "cost bao nhieu", "cost bao nhiêu", "gia ca ra sao", "giá cả ra sao",
        "bao nhieu 1 mon", "bao nhiêu 1 món", "1 pho gia bao nhieu",
        "1 phở giá bao nhiêu", "com bao nhieu tien", "cơm bao nhiêu tiền"
    ],

    "ask_time": [
        "mấy giờ rồi", "thời gian hiện tại", "cho hỏi giờ", "bây giờ là mấy giờ",
        "may gio roi", "thoi gian hien tai", "cho hoi gio", "bay gio la may gio",
        "hiện tại mấy giờ", "bây giờ mấy giờ rồi", "hien tai may gio",
        "bay gio may gio roi", "gio may roi", "giờ mấy rồi", "bao gio",
        "bao giờ", "khi nao", "khi nào", "thoi gian", "thời gian",
        "bay gio may gio", "bây giờ mấy giờ", "may gio", "mấy giờ"
    ],

    "thank_you": [
        "cảm ơn", "cám ơn", "thanks", "thank you", "cam on", "cam on ban",
        "cảm ơn bạn", "cảm ơn nhiều", "cam on nhieu", "xin cảm ơn",
        "xin cam on", "rat cam on", "rất cảm ơn", "thank you very much"
    ],

    "goodbye": [
        "tạm biệt", "tam biet", "bye", "goodbye", "chao tam biet",
        "chào tạm biệt", "hen gap lai", "hẹn gặp lại", "see you",
        "see you later", "chuc mot ngay tot lanh", "chúc một ngày tốt lành"
    ]
}

# Keywords cho mỗi intent
keywords_data = {
    "greeting": ["chào", "xin", "hello", "hi", "chao", "helo", "good", "morning", "afternoon", "evening"],
    "order_food": ["đặt", "món", "đồ ăn", "gọi", "order", "thức ăn", "dat", "mon", "do an", "goi", "thuc an", "ăn", "an", "uống", "uong"],
    "ask_price": ["giá", "tiền", "bao nhiêu", "chi phí", "tính tiền", "gia", "tien", "bao nhieu", "chi phi", "tinh tien", "phí", "phi", "cost"],
    "ask_time": ["giờ", "thời gian", "mấy giờ", "bao giờ", "gio", "thoi gian", "may gio", "bao gio", "khi nào", "khi nao"],
    "thank_you": ["cảm ơn", "cám ơn", "thanks", "thank", "cam on", "xin cảm ơn", "xin cam on"],
    "goodbye": ["tạm biệt", "tam biet", "bye", "goodbye", "chào", "chao", "hen gap", "hẹn gặp"]
}

# Responses
responses = {
    "greeting": "Xin chào! Tôi có thể giúp gì cho bạn?",
    "order_food": "Bạn muốn đặt món gì ạ?",
    "ask_price": "Bạn muốn hỏi giá sản phẩm nào ạ?",
    "ask_time": "Hiện tại là {time}",
    "thank_you": "Không có gì! Rất vui được giúp bạn!",
    "goodbye": "Tạm biệt! Hẹn gặp lại bạn!"
}

# Tạo file JSON
model_data = {}
for intent in training_data:
    model_data[intent] = {
        "patterns": training_data[intent],
        "keywords": keywords_data.get(intent, []),
        "threshold": 0.4,
        "response": responses.get(intent, "")
    }

# Lưu file
with open("models/intents.json", "w", encoding="utf-8") as f:
    json.dump(model_data, f, ensure_ascii=False, indent=2)

print("Đã tạo file training models/intents.json")
print(f"Tổng số intents: {len(model_data)}")
for intent, data in model_data.items():
    print(f"  - {intent}: {len(data['patterns'])} patterns, {len(data['keywords'])} keywords")
