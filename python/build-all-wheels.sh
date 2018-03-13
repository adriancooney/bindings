#!/bin/bash
set -x
set -v
set -e
# Install with extra pythons
if [[ -d /opt/python/ ]]; then
    for PYBIN in /opt/python/*/bin; do
        rm -rf build
        "${PYBIN}/pip" wheel . --wheel-dir dist
    done
fi

# Install with default python if it exists
if (which pip2); then rm -rf build; pip2 wheel . --wheel-dir dist; fi
if (which pip3); then rm -rf build; pip3 wheel . --wheel-dir dist; fi

if [[ -d dist ]]; then
    for whl in dist/*.whl; do
        auditwheel repair "$whl" --wheel-dir dist || (echo "Can't repair $whl")
    done
fi
