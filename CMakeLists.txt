cmake_minimum_required(VERSION 3.12)
project(viet_intent_python)

# Tìm Python và pybind11
find_package(Python REQUIRED COMPONENTS Development)
find_package(pybind11 REQUIRED)

# Thêm thư viện C++
add_library(viet_intent_cpp STATIC
    ../src/intent_detector.cpp
    ../src/text_preprocessor.cpp
    ../src/viet_intent.cpp
)

target_include_directories(viet_intent_cpp PRIVATE ../include)

# Module Python
pybind11_add_module(viet_intent
    viet_intent_py.cpp
)

target_link_libraries(viet_intent PRIVATE viet_intent_cpp)
target_include_directories(viet_intent PRIVATE ../include)

# Copy file mẫu khi build
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/__init__.py
               ${CMAKE_CURRENT_BINARY_DIR}/viet_intent/__init__.py COPYONLY)
