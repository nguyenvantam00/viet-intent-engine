#ifndef INTENT_DETECTOR_H
#define INTENT_DETECTOR_H

#include <string>
#include <vector>
#include <map>
#include <memory>

namespace VietIntent {

// Forward declaration của IntentResult từ viet_intent.h
struct IntentResult;

struct IntentPattern {
    std::vector<std::string> patterns;
    std::vector<std::string> keywords;
    double threshold = 0.5;
};

class IntentDetector {
public:
    IntentDetector();
    ~IntentDetector();

    IntentResult detect(const std::string& text);

    void add_intent(const std::string& intent_name,
                   const IntentPattern& pattern,
                   const std::string& response_pattern = "");

    bool load_from_json(const std::string& filepath);

private:
    class Impl;
    std::unique_ptr<Impl> pimpl;
};

}

#endif
