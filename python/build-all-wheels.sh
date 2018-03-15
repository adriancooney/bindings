#!/bin/bash
set -x
set -v
set -e

# Install with extra pythons
if [[ -d /opt/python/ ]]; then
    # Set LD PATH
    export LD_LIBRARY_PATH=/opt/openssl/lib:/usr/local/lib:$LD_LIBARY_PATH:
    for PYBIN in /opt/python/*/bin; do
        rm -rf build
        "${PYBIN}/pip" wheel . --wheel-dir dist
        whl=$(ls dist -htal | grep ".whl" | awk '{print $NF}' | head -n 1)
        
        (cd dist && auditwheel -vv show "$whl")
        if ! (cd dist && auditwheel repair "$whl" --wheel-dir .); then
            exit 1
        fi
    done
fi

# Install with default python if it exists
if (which pip2); then rm -rf build; pip2 wheel . --wheel-dir dist; fi
if (which pip3); then rm -rf build; pip3 wheel . --wheel-dir dist; fi

