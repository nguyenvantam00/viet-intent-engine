#ifndef TEXT_PREPROCESSOR_H
#define TEXT_PREPROCESSOR_H

#include <string>
#include <vector>

namespace VietIntent {

class TextPreprocessor {
public:
    static std::string normalize(const std::string& text);
    static std::vector<std::string> tokenize(const std::string& text);
    static std::string remove_diacritics(const std::string& text);

    // Chuẩn hóa tiếng Việt
    static std::string standardize_vietnamese(const std::string& text);

    // Tách từ đơn giản
    static std::vector<std::string> word_segmentation(const std::string& text);

private:
    static char remove_tone(char c);
};

} // namespace VietIntent

#endif
