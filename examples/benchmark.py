# benchmark.py
import viet_intent
import time

def benchmark():
    engine = viet_intent.IntentEngine()

    test_sentences = [
        "xin chào",
        "chào buổi sáng",
        "tôi muốn đặt phở",
        "cho tôi đặt bún chả",
        "giá bánh mì bao nhiêu",
        "cà phê giá thế nào",
        "mấy giờ rồi",
        "bây giờ là mấy giờ",
        "đặt phòng khách sạn",
        "tôi cần thuê xe"
    ] * 100  # Lặp lại 100 lần để test hiệu năng

    print("🚀 Running benchmark...")
    print(f"Total queries: {len(test_sentences)}")

    start_time = time.time()

    results = []
    for sentence in test_sentences:
        result = engine.detect(sentence)
        results.append(result.intent)

    end_time = time.time()

    # Tính toán thống kê
    total_time = end_time - start_time
    avg_time = total_time / len(test_sentences)
    qps = len(test_sentences) / total_time

    print("\n📊 Benchmark Results:")
    print(f"  Total time: {total_time:.2f} seconds")
    print(f"  Average time per query: {avg_time*1000:.2f} ms")
    print(f"  Queries per second: {qps:.0f}")
    print(f"  Memory usage: {len(test_sentences)} queries processed")

    # Phân bố intent
    from collections import Counter
    intent_counts = Counter(results)
    print("\n📈 Intent Distribution:")
    for intent, count in intent_counts.most_common():
        percentage = count / len(results) * 100
        print(f"  {intent}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    benchmark()
