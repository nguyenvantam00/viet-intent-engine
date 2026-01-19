from setuptools import setup, Extension
import os
import sys

# Đường dẫn
base_dir = os.path.dirname(os.path.abspath(__file__))
include_dir = os.path.join(base_dir, '..', 'include')
src_dir = os.path.join(base_dir, '..', 'src')

# Thêm pybind11 include
pybind11_include = None
try:
    import pybind11
    pybind11_include = pybind11.get_include()
except ImportError:
    print("pybind11 not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pybind11"])
    import pybind11
    pybind11_include = pybind11.get_include()

# Tất cả include directories
include_dirs = [
    include_dir,
    pybind11_include,
    pybind11.get_include(True)
]

# Extension module
ext = Extension(
    'viet_intent',
    sources=[
        os.path.join(src_dir, 'text_preprocessor.cpp'),
        os.path.join(src_dir, 'intent_detector.cpp'),
        os.path.join(src_dir, 'viet_intent.cpp'),
        os.path.join(base_dir, 'viet_intent_py.cpp')
    ],
    include_dirs=include_dirs,
    language='c++',
    extra_compile_args=['-std=c++17', '-O3', '-Wall', '-Wno-sign-compare']
)

setup(
    name='viet-intent-engine',
    version='0.1.0',
    author='Vietnamese NLP',
    description='Vietnamese Intent Detection Engine',
    ext_modules=[ext],
)
