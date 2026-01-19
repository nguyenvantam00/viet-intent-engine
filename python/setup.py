from setuptools import setup, Extension
import os
import sys
import subprocess

# Get pybind11 include path
try:
    import pybind11
    pybind11_include = pybind11.get_include()
except ImportError:
    print("Installing pybind11...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pybind11>=2.6.0"])
    import pybind11
    pybind11_include = pybind11.get_include()

# Get paths
base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(base_dir)
include_dir = os.path.join(project_dir, 'include')
src_dir = os.path.join(project_dir, 'src')

# Compilation arguments
extra_compile_args = ['-std=c++17', '-O3', '-Wall', '-fPIC']
if sys.platform == 'win32':
    extra_compile_args = ['/std:c++17', '/O2', '/D_CRT_SECURE_NO_WARNINGS']

# Extension module
ext_modules = [
    Extension(
        'viet_intent',
        sources=[
            os.path.join(src_dir, 'text_preprocessor.cpp'),
            os.path.join(src_dir, 'intent_detector.cpp'),
            os.path.join(src_dir, 'viet_intent.cpp'),
            os.path.join(base_dir, 'viet_intent_py.cpp')
        ],
        include_dirs=[include_dir, pybind11_include],
        language='c++',
        extra_compile_args=extra_compile_args,
        define_macros=[('VERSION_INFO', '"1.0.0"')],
    ),
]

# Read README
with open(os.path.join(project_dir, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='viet-intent-engine',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='Vietnamese Intent Detection Engine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/viet-intent-engine',
    ext_modules=ext_modules,
    packages=['viet_intent'],
    package_dir={'': 'python'},
    python_requires='>=3.6',
    install_requires=['pybind11>=2.6.0'],
    extras_require={
        'dev': ['pytest>=6.0', 'numpy>=1.19.0'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: C++',
    ],
    keywords='vietnamese nlp intent-detection chatbot offline',
    zip_safe=False,
)
