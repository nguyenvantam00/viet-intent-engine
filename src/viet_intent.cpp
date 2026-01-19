#include "viet_intent.h"
#include "intent_detector.h"
#include "text_preprocessor.h"
#include <iostream>  // THÊM DÒNG NÀY
#include <string>    // THÊM DÒNG NÀY (nếu cần)

namespace VietIntent {

class IntentEngine::Impl {
public:
    IntentDetector detector;
    bool initialized = false;
};

IntentEngine::IntentEngine() : pimpl(std::make_unique<Impl>()) {
    pimpl->initialized = true;
}

IntentEngine::~IntentEngine() = default;

bool IntentEngine::initialize(const std::string& model_path) {
    std::cout << "[IntentEngine] Initializing with model path: " << model_path << std::endl;
    pimpl->initialized = true;
    return true;
}

IntentResult IntentEngine::detect(const std::string& text) {
    if (!pimpl->initialized) {
        initialize();
    }
    return pimpl->detector.detect(text);
}

void IntentEngine::add_intent(const std::string& intent_name,
                             const std::vector<std::string>& patterns,
                             const std::string& response_pattern) {
    IntentPattern pattern;
    pattern.patterns = patterns;
    pattern.threshold = 0.5;

    // Tự động tạo keywords từ patterns
    for (const auto& p : patterns) {
        auto tokens = TextPreprocessor::tokenize(p);
        pattern.keywords.insert(pattern.keywords.end(), tokens.begin(), tokens.end());
    }

    pimpl->detector.add_intent(intent_name, pattern, response_pattern);
}

void IntentEngine::load_patterns_from_file(const std::string& filepath) {
    pimpl->detector.load_from_json(filepath);
}

void IntentEngine::save_patterns(const std::string& filepath) {
    std::cout << "[IntentEngine] Save patterns to: " << filepath
              << " (not implemented in this version)" << std::endl;
}

} // namespace VietIntent
