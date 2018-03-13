import os
import shutil
import sys
import platform

#from distutils.core import setup, Extension
from setuptools import setup, Extension

upstream_dir = os.path.join(os.path.dirname(__file__),"uWebSockets", "src")
if not os.path.exists(upstream_dir):
    shutil.copytree(os.path.join(os.path.dirname(__file__), "..", "uWebSockets"), os.path.join(os.path.dirname(__file__), "uWebSockets"))

upstream_src = [os.path.join(upstream_dir, f) for f in os.listdir(upstream_dir) if f.split(".")[-1] in ("cpp", "cxx", "c")]
upstream_headers = [os.path.join(upstream_dir, f) for f in os.listdir(upstream_dir) if f.split(".")[-1] in ("hpp", "hxx", "h")]

platform_libraries = ["ws2_32","mswsock","advapi32","iphlpapi","psapi","userenv"] if platform.system().lower() == "windows" else []
platform_link_args = ["-Wl,-Bstatic", "-lc", "-lstdc++", "-Wl,-Bdynamic"]

uWebSockets = Extension("uWebSockets", 
    sources=["Bindings.cpp"] + upstream_src,
    include_dirs=[upstream_dir],
    libraries=["ssl","crypto","z","uv"] + platform_libraries,
    #define_macros=[("UWS_THREADSAFE", 1), ("PYTHON_FLAVOUR",sys.version_info[0])], ## FIXME: UWS_THREADSAFE unsupported on Windows and OSX
    define_macros=[("PYTHON_FLAVOUR", sys.version_info[0]), ("__STDC_LIMIT_MACROS",1)],
    extra_compile_args=["-std=c++11"], # FIXME: Won't work on older compilers
    extra_link_args=platform_link_args
)

setup(name="uWebSockets",
    version="0.14.6a1",
    description="Python Bindings for the uWebSockets library",
    url="https://github.com/uNetworking/uWebSockets-bindings/",
    author="Sam Moore",
    author_email="smoore@elementengineering.com.au",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ], 
    keywords="websockets development",
    ext_modules =[uWebSockets],
)
