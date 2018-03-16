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

if platform.system().lower() == "linux":
    platform_defines = [("UWS_THREADSAFE", 1)] # FIXME: Does not work on Windoze
else:
    platform_defines = []

platform_libraries = [] #["ws2_32","mswsock","advapi32","iphlpapi","psapi","userenv"] if platform.system().lower() == "windows" else []
extra_objects = []
if os.environ.get("MANYLINUX",None) is not None:
    # To satisfy manylinux1 tag, we need to jump through a lot of hoops; see docker/manylinux
    platform_link_args = [
        # Don't link with standard library, the script in docker/manylinux/ld-patch.sh will add the correct flags for that.
        "-nostdlib",
        "-Wl,--add-needed",
        "-Wl,--demangle",
        "-Wl,-Bstatic",
        "-lz",
        "-luv",
        "-L/opt/openssl/lib/",
        "-lssl",
        "-lcrypto",
        
        
        "/glibc-glibc-2.10/build/elf/soinit.os",
        "-Wl,-z,muldefs",
        "-Wl,--gc-sections",
        "-Wl,-fini=__wrap_fini",
        "-Wl,--wrap=atexit",
        "-Wl,-z,initfirst",
        "/glibc-glibc-2.10/build/libc_pic.a",
        "-Wl,--no-gc-sections",
        
        "-Wl,--default-symver",
        "-Wl,--version-script=/vagrant/manylinux.map",
        "-Wl,-Map=/vagrant/uWebSockets.map",
        "-Wl,--cref",
        
        "-Wl,-Bdynamic",

        "/opt/rh/devtoolset-2/root/usr/lib/gcc/x86_64-CentOS-linux/4.8.2/libgcc_eh.a",
        "/opt/rh/devtoolset-2/root/usr/lib/gcc/x86_64-CentOS-linux/4.8.2/libstdc++.a",        

    ]
    platform_include_dirs = ["/opt/glibc2.10/include", "/opt/openssl/include/"]
    platform_cflags = ["-fPIC", "-g", "-Og"]
    platform_defines += [("MANYLINUX",1)] # ("DEBUG_PYTHON_BINDINGS", 1)]

    

else:
    platform_link_args = []
    platform_include_dirs = []
    platform_cflags = []
    platform_libraries = ["ssl", "crypto", "z", "uv"]

uWebSockets = Extension("uWebSockets", 
    sources=["Bindings.cpp"] + upstream_src,
    include_dirs=[upstream_dir] + platform_include_dirs,
    libraries=platform_libraries,
    #define_macros=[("UWS_THREADSAFE", 1), ("PYTHON_FLAVOUR",sys.version_info[0])], ## FIXME: UWS_THREADSAFE unsupported on Windows and OSX
    define_macros=[("PYTHON_FLAVOUR", sys.version_info[0]), ("__STDC_LIMIT_MACROS",1)] + platform_defines,
    extra_compile_args=["-std=c++11"]+platform_cflags, # FIXME: Won't work on older compilers
    extra_link_args=platform_link_args,
    extra_objects = extra_objects
)

setup(name="uWebSockets",
    version="0.14.6a2",
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
    test_suite='nose.collector',
    tests_require=['nose']
)
