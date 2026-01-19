#include "text_preprocessor.h"
#include <algorithm>
#include <cctype>
#include <sstream>
#include <iostream>
#include <cstring>
#include <unordered_map>

namespace VietIntent {

// Sử dụng string thay vì char để xử lý UTF-8
static const std::unordered_map<std::string, char> DIACRITIC_MAP = {
    // Chữ thường
    {"á", 'a'}, {"à", 'a'}, {"ả", 'a'}, {"ã", 'a'}, {"ạ", 'a'},
    {"ă", 'a'}, {"ắ", 'a'}, {"ằ", 'a'}, {"ẳ", 'a'}, {"ẵ", 'a'}, {"ặ", 'a'},
    {"â", 'a'}, {"ấ", 'a'}, {"ầ", 'a'}, {"ẩ", 'a'}, {"ẫ", 'a'}, {"ậ", 'a'},
    {"é", 'e'}, {"è", 'e'}, {"ẻ", 'e'}, {"ẽ", 'e'}, {"ẹ", 'e'},
    {"ê", 'e'}, {"ế", 'e'}, {"ề", 'e'}, {"ể", 'e'}, {"ễ", 'e'}, {"ệ", 'e'},
    {"í", 'i'}, {"ì", 'i'}, {"ỉ", 'i'}, {"ĩ", 'i'}, {"ị", 'i'},
    {"ó", 'o'}, {"ò", 'o'}, {"ỏ", 'o'}, {"õ", 'o'}, {"ọ", 'o'},
    {"ô", 'o'}, {"ố", 'o'}, {"ồ", 'o'}, {"ổ", 'o'}, {"ỗ", 'o'}, {"ộ", 'o'},
    {"ơ", 'o'}, {"ớ", 'o'}, {"ờ", 'o'}, {"ở", 'o'}, {"ỡ", 'o'}, {"ợ", 'o'},
    {"ú", 'u'}, {"ù", 'u'}, {"ủ", 'u'}, {"ũ", 'u'}, {"ụ", 'u'},
    {"ư", 'u'}, {"ứ", 'u'}, {"ừ", 'u'}, {"ử", 'u'}, {"ữ", 'u'}, {"ự", 'u'},
    {"ý", 'y'}, {"ỳ", 'y'}, {"ỷ", 'y'}, {"ỹ", 'y'}, {"ỵ", 'y'},
    {"đ", 'd'},

    // Chữ hoa
    {"Á", 'A'}, {"À", 'A'}, {"Ả", 'A'}, {"Ã", 'A'}, {"Ạ", 'A'},
    {"Ă", 'A'}, {"Ắ", 'A'}, {"Ằ", 'A'}, {"Ẳ", 'A'}, {"Ẵ", 'A'}, {"Ặ", 'A'},
    {"Â", 'A'}, {"Ấ", 'A'}, {"Ầ", 'A'}, {"Ẩ", 'A'}, {"Ẫ", 'A'}, {"Ậ", 'A'},
    {"É", 'E'}, {"È", 'E'}, {"Ẻ", 'E'}, {"Ẽ", 'E'}, {"Ẹ", 'E'},
    {"Ê", 'E'}, {"Ế", 'E'}, {"Ề", 'E'}, {"Ể", 'E'}, {"Ễ", 'E'}, {"Ệ", 'E'},
    {"Í", 'I'}, {"Ì", 'I'}, {"Ỉ", 'I'}, {"Ĩ", 'I'}, {"Ị", 'I'},
    {"Ó", 'O'}, {"Ò", 'O'}, {"Ỏ", 'O'}, {"Õ", 'O'}, {"Ọ", 'O'},
    {"Ô", 'O'}, {"Ố", 'O'}, {"Ồ", 'O'}, {"Ổ", 'O'}, {"Ỗ", 'O'}, {"Ộ", 'O'},
    {"Ơ", 'O'}, {"Ớ", 'O'}, {"Ờ", 'O'}, {"Ở", 'O'}, {"Ỡ", 'O'}, {"Ợ", 'O'},
    {"Ú", 'U'}, {"Ù", 'U'}, {"Ủ", 'U'}, {"Ũ", 'U'}, {"Ụ", 'U'},
    {"Ư", 'U'}, {"Ứ", 'U'}, {"Ừ", 'U'}, {"Ử", 'U'}, {"Ữ", 'U'}, {"Ự", 'U'},
    {"Ý", 'Y'}, {"Ỳ", 'Y'}, {"Ỷ", 'Y'}, {"Ỹ", 'Y'}, {"Ỵ", 'Y'},
    {"Đ", 'D'}
};

// Hàm kiểm tra UTF-8 character length
int utf8_char_length(unsigned char c) {
    if ((c & 0x80) == 0) return 1;        // ASCII
    else if ((c & 0xE0) == 0xC0) return 2; // 2-byte UTF-8
    else if ((c & 0xF0) == 0xE0) return 3; // 3-byte UTF-8
    else if ((c & 0xF8) == 0xF0) return 4; // 4-byte UTF-8
    return 1; // Invalid, treat as single byte
}

// Hàm trích xuất UTF-8 character
std::string get_utf8_char(const std::string& str, size_t pos) {
    if (pos >= str.length()) return "";

    int len = utf8_char_length(static_cast<unsigned char>(str[pos]));
    if (pos + len > str.length()) return str.substr(pos, 1);

    return str.substr(pos, len);
}

std::string TextPreprocessor::normalize(const std::string& text) {
    if (text.empty()) return "";

    std::string result;

    // Xử lý từng ký tự UTF-8
    for (size_t i = 0; i < text.length();) {
        std::string ch = get_utf8_char(text, i);
        i += ch.length();

        // Chuyển thành chữ thường (chỉ cho ASCII)
        if (ch.length() == 1 && static_cast<unsigned char>(ch[0]) < 128) {
            ch[0] = std::tolower(ch[0]);
        }

        result += ch;
    }

    // Xóa dấu
    result = remove_diacritics(result);

    // Xóa khoảng trắng thừa và ký tự đặc biệt
    std::stringstream ss(result);
    std::string token;
    result.clear();

    while (ss >> token) {
        // Xóa dấu câu ở đầu và cuối (chỉ ASCII)
        while (!token.empty()) {
            unsigned char last = static_cast<unsigned char>(token.back());
            unsigned char first = static_cast<unsigned char>(token.front());

            bool modified = false;

            if (std::ispunct(last) && last < 128) {
                token.pop_back();
                modified = true;
            }
            if (!token.empty() && std::ispunct(first) && first < 128) {
                token.erase(0, 1);
                modified = true;
            }

            if (!modified) break;
        }

        if (!token.empty()) {
            if (!result.empty()) result += " ";
            result += token;
        }
    }

    return result;
}

std::vector<std::string> TextPreprocessor::tokenize(const std::string& text) {
    std::vector<std::string> tokens;
    std::stringstream ss(normalize(text));
    std::string token;

    while (ss >> token) {
        if (!token.empty()) {
            tokens.push_back(token);
        }
    }

    return tokens;
}

std::string TextPreprocessor::remove_diacritics(const std::string& text) {
    if (text.empty()) return "";

    std::string result;

    // Xử lý từng ký tự UTF-8
    for (size_t i = 0; i < text.length();) {
        std::string ch = get_utf8_char(text, i);

        // Kiểm tra xem có trong map dấu không
        auto it = DIACRITIC_MAP.find(ch);
        if (it != DIACRITIC_MAP.end()) {
            // Thay thế bằng ký tự không dấu
            result += it->second;
        } else {
            // Giữ nguyên
            result += ch;
        }

        i += ch.length();
    }

    return result;
}

std::string TextPreprocessor::standardize_vietnamese(const std::string& text) {
    std::string result = normalize(text);
    // Đã được xử lý dấu trong normalize()
    return result;
}

std::vector<std::string> TextPreprocessor::word_segmentation(const std::string& text) {
    return tokenize(text);
}

char TextPreprocessor::remove_tone(char c) {
    // Đơn giản hóa: chỉ xử lý ASCII
    // Đối với ký tự tiếng Việt, cần xử lý trong remove_diacritics
    return std::tolower(static_cast<unsigned char>(c));
}

} // namespace VietIntent
