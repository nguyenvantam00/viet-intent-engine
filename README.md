
# Vietnamese Intent Engine

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![C++17](https://img.shields.io/badge/C++-17-blue.svg)](https://isocpp.org/)
[![GitHub Stars](https://img.shields.io/github/stars/nguyenvantam00/viet-intent-engine)](https://github.com/nguyenvantam00/viet-intent-engine/stargazers)
[![Code Size](https://img.shields.io/github/languages/code-size/nguyenvantam00/viet-intent-engine)](https://github.com/nguyenvantam00/viet-intent-engine)

Vietnamese Intent Engine is a lightweight, high-performance C++ library with Python bindings for detecting user intents in Vietnamese sentences. It works entirely offline with clear, rule-based logic, making it perfect for chatbots, voice assistants, and automated customer service systems.

## Features

- Accurate Vietnamese Intent Detection - Understands both formal and casual Vietnamese, with or without diacritics.
- Blazing Fast & Offline - No network required. Pure C++ core ensures low latency.
- Fully Customizable - Easily define new intents with your own patterns and responses.
- Seamless Python Integration - Simple API, works like any Python package.
- Easy Deployment - Single shared library, minimal dependencies.
- Entity Extraction - Identifies key items like food names, prices, and more from sentences.

## Table of Contents
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [API Reference](#api-reference)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Quick Start

Get started in under a minute:

```python
import viet_intent

# 1. Create an engine instance
engine = viet_intent.IntentEngine()

# 2. Detect intent from text
result = engine.detect("xin chào bạn")

# 3. Use the result
print(f"Intent: {result.intent}")          # Output: greeting
print(f"Confidence: {result.confidence:.2f}")  # Output: 0.95
print(f"Suggested Response: {result.response_pattern}")
# Output: Xin chào! Tôi có thể giúp gì cho bạn?
```

## Installation

### Prerequisites
- Python 3.6 or higher
- C++ Compiler with C++17 support (g++ ≥ 7, clang ≥ 5, or MSVC ≥ 2017)
- Git

### Method 1: Install from GitHub (Recommended for Development)
```bash
# Clone the repository
git clone https://github.com/nguyenvantam00/viet-intent-engine.git
cd viet-intent-engine

# Install in development mode
pip install -e .

# Verify installation
python -c "import viet_intent; print('Import successful!')"
```

### Method 2: Install via pip (Once Published to PyPI)
```bash
# Will be available after publishing
pip install viet-intent-engine
```

### Method 3: Build from Source (Advanced)
```bash
# Navigate to python directory
cd viet-intent-engine/python

# Build the extension
python setup.py build_ext --inplace

# Test the build
python -c "import viet_intent; print('Build successful!')"
```

### Verifying Your Installation
Run this quick test to ensure everything works:
```bash
cd viet-intent-engine/examples
python basic_usage.py
```

## Usage Guide

### 1. Basic Intent Detection
The engine comes with several built-in intents:

```python
import viet_intent

engine = viet_intent.IntentEngine()

test_phrases = [
    "xin chào",
    "tôi muốn đặt món phở",
    "giá bánh mì bao nhiêu",
    "mấy giờ rồi",
    "cảm ơn bạn",
    "tạm biệt"
]

for phrase in test_phrases:
    result = engine.detect(phrase)
    print(f"'{phrase}'")
    print(f"  Intent: {result.intent}")
    print(f"  Confidence: {result.confidence:.2f}")
    if result.entities:
        print(f"  Entities: {result.entities}")
    print()
```

### 2. Adding Custom Intents
Extend the engine with your own domain-specific intents:

```python
# Define a new intent for weather inquiries
engine.add_intent(
    "weather_inquiry",
    patterns=[
        "thời tiết hôm nay thế nào",
        "hôm nay có mưa không",
        "nhiệt độ bao nhiêu",
        "dự báo thời tiết ngày mai"
    ],
    response="Hôm nay trời nắng, nhiệt độ khoảng 28-32°C."
)

# Define an intent for hotel booking
engine.add_intent(
    "book_hotel",
    patterns=[
        "đặt phòng khách sạn",
        "tôi muốn book phòng",
        "còn phòng trống không",
        "đặt phòng cho 2 người"
    ],
    response="Bạn muốn đặt phòng loại nào và cho bao nhiêu người ạ?"
)

# Test the new intents
result = engine.detect("thời tiết hôm nay thế nào")
print(f"Weather inquiry detected: {result.intent}")  # weather_inquiry
```

### 3. Working with Extracted Entities
The engine can extract useful information from sentences:

```python
# Sentences with entities
test_cases = [
    "tôi muốn đặt 2 phần phở bò",
    "cho tôi một bánh mì thịt và một cà phê",
    "giá áo sơ mi bao nhiêu"
]

for text in test_cases:
    result = engine.detect(text)
    print(f"\nInput: '{text}'")
    print(f"Intent: {result.intent}")
    if result.entities:
        print("Extracted Entities:")
        for key, value in result.entities.items():
            print(f"  - {key}: {value}")
    
    # Use entities in your application logic
    if result.intent == "order_food" and "food_item" in result.entities:
        food = result.entities["food_item"]
        print(f"Preparing order for: {food}")
```

### 4. Building a Simple Chatbot
Here's a complete example of a Vietnamese chatbot:

```python
# examples/chatbot_demo.py
import viet_intent
import random
import time

class VietnameseChatbot:
    def __init__(self):
        self.engine = viet_intent.IntentEngine()
        self.setup_responses()
    
    def setup_responses(self):
        """Configure response templates for each intent"""
        self.responses = {
            "greeting": [
                "Xin chào! Tôi có thể giúp gì cho bạn?",
                "Chào bạn! Rất vui được gặp bạn!",
                "Hi! Bạn cần tôi giúp gì không?"
            ],
            "order_food": lambda entities: 
                f"Đã nhận đơn đặt {entities.get('food_item', 'món ăn')} của bạn!",
            "ask_price": lambda entities: 
                f"Giá {entities.get('item', 'sản phẩm')} là 50,000 VNĐ",
            "ask_time": lambda entities: 
                f"Hiện tại là {time.strftime('%H:%M')}",
            "thank_you": ["Không có gì! Rất vui được giúp bạn!"],
            "goodbye": ["Tạm biệt! Hẹn gặp lại bạn!"],
            "default": [
                "Xin lỗi, tôi chưa hiểu ý bạn.",
                "Bạn có thể nói rõ hơn được không?"
            ]
        }
    
    def get_response(self, intent_result):
        """Generate appropriate response based on intent"""
        intent = intent_result.intent
        
        if intent in self.responses:
            response = self.responses[intent]
            if callable(response):
                return response(intent_result.entities)
            return random.choice(response)
        
        return random.choice(self.responses["default"])
    
    def chat(self):
        """Main chat loop"""
        print("=" * 50)
        print("Vietnamese Chatbot (Type 'quit' to exit)")
        print("=" * 50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Chatbot: Tạm biệt! Hẹn gặp lại!")
                break
            
            # Detect intent
            result = self.engine.detect(user_input)
            
            # Get and print response
            response = self.get_response(result)
            print(f"Chatbot: {response}")
            
            # Show debug info (optional)
            print(f"   [Intent: {result.intent}, Confidence: {result.confidence:.2f}]")

if __name__ == "__main__":
    bot = VietnameseChatbot()
    bot.chat()
```

### 5. Performance Benchmarking
Measure how fast the engine processes requests:

```python
# examples/benchmark.py
import viet_intent
import time

def run_benchmark():
    engine = viet_intent.IntentEngine()
    
    # Test sentences
    test_sentences = [
        "xin chào",
        "tôi muốn đặt phở",
        "giá bao nhiêu",
        "mấy giờ rồi",
        "cảm ơn",
        "tạm biệt"
    ] * 1000  # Repeat 1000 times for meaningful results
    
    print("Starting performance benchmark...")
    print(f"Total queries: {len(test_sentences):,}")
    
    # Time the processing
    start_time = time.time()
    
    for sentence in test_sentences:
        _ = engine.detect(sentence)  # We ignore results for benchmark
    
    end_time = time.time()
    
    # Calculate metrics
    total_time = end_time - start_time
    queries_per_second = len(test_sentences) / total_time
    avg_latency = (total_time / len(test_sentences)) * 1000  # in milliseconds
    
    print("\nBenchmark Results:")
    print(f"  Total time: {total_time:.2f} seconds")
    print(f"  Average latency: {avg_latency:.2f} ms")
    print(f"  Queries per second: {queries_per_second:.0f}")
    print(f"  Total queries processed: {len(test_sentences):,}")

if __name__ == "__main__":
    run_benchmark()
```

## API Reference

### IntentEngine Class
Main class for intent detection.

#### Constructor
```python
engine = IntentEngine()
```

#### Methods

**detect(text: str) -> IntentResult**
Detects intent from Vietnamese text.

```python
result = engine.detect("xin chào bạn")
```

**Parameters:**
- `text` (str): Vietnamese sentence to analyze

**Returns:**
- `IntentResult`: Object containing detection results

**add_intent(name: str, patterns: List[str], response: str = "")**
Adds a custom intent to the engine.

```python
engine.add_intent(
    name="weather_inquiry",
    patterns=["thời tiết thế nào", "có mưa không"],
    response="Hôm nay trời đẹp."
)
```

**Parameters:**
- `name` (str): Unique identifier for the intent
- `patterns` (List[str]): List of example sentences for this intent
- `response` (str, optional): Default response template

**load_patterns_from_file(filepath: str)**
Loads intents from a JSON configuration file.

```python
engine.load_patterns_from_file("models/custom_intents.json")
```

**save_patterns(filepath: str)**
Saves current intents to a JSON file.

```python
engine.save_patterns("models/my_intents.json")
```

### IntentResult Class
Contains results from intent detection.

**Attributes:**
- `intent` (str): Detected intent name
- `confidence` (float): Confidence score (0.0 to 1.0)
- `entities` (Dict[str, str]): Extracted entities from the text
- `response_pattern` (str): Suggested response template

## Architecture

```
viet-intent-engine/
├── src/                 # C++ Core Engine
│   ├── intent_detector.cpp    # Main detection logic
│   ├── text_preprocessor.cpp  # Vietnamese text normalization
│   └── viet_intent.cpp        # Engine implementation
├── include/             # C++ Headers
├── python/              # Python Bindings
│   ├── viet_intent_py.cpp     # pybind11 wrapper
│   └── setup.py               # Build configuration
├── examples/            # Usage Examples
├── models/              # Intent Configuration
├── tests/               # Test Suite
└── docs/                # Documentation
```

**Data Flow:**
1. Input → Vietnamese text sentence
2. Preprocessing → Normalization, tokenization, diacritic handling
3. Pattern Matching → Compare with intent patterns using similarity algorithms
4. Intent Selection → Choose intent with highest confidence score
5. Entity Extraction → Identify key information in the sentence
6. Output → IntentResult with intent, confidence, and entities

## Contributing

We welcome contributions! Here's how you can help:

### Setting Up Development Environment
```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/viet-intent-engine.git
cd viet-intent-engine

# 2. Install development dependencies
pip install -e .[dev]

# 3. Build the extension
python setup.py build_ext --inplace

# 4. Run tests
python -m pytest tests/ -v
```

### Development Guidelines
- Follow existing code style (PEP 8 for Python, Google Style for C++)
- Add tests for new features
- Update documentation accordingly
- Use descriptive commit messages

### Reporting Issues
When reporting bugs, please include:
1. The exact command or code that caused the issue
2. Expected vs actual behavior
3. Your environment (OS, Python version, etc.)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact & Support

- **Repository**: https://github.com/nguyenvantam00/viet-intent-engine
- **Issues**: https://github.com/nguyenvantam00/viet-intent-engine/issues
- **Author**: Nguyen Van Tam

## Acknowledgments

- [pybind11](https://github.com/pybind/pybind11) for seamless C++/Python interoperability
- The Vietnamese NLP community for inspiration and resources
- All contributors and users of this project

---

If you find this project useful, please give it a star on GitHub!

---

*Last updated: January 2026 | Version: 1.0.0*
```
