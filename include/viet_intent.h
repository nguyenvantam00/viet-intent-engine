#ifndef VIET_INTENT_H
#define VIET_INTENT_H

#include <string>
#include <vector>
#include <map>
#include <memory>

namespace VietIntent {

struct IntentResult {
    std::string intent;
    double confidence;
    std::map<std::string, std::string> entities;
    std::string response_pattern;
};

class IntentEngine {
public:
    IntentEngine();
    ~IntentEngine();

    bool initialize(const std::string& model_path = "models/");
    IntentResult detect(const std::string& text);

    void add_intent(const std::string& intent_name,
                    const std::vector<std::string>& patterns,
                    const std::string& response_pattern = "");

    void load_patterns_from_file(const std::string& filepath);
    void save_patterns(const std::string& filepath);

private:
    class Impl;
    std::unique_ptr<Impl> pimpl;
};

} // namespace VietIntent

#endif
