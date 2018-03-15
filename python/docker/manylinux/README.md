Dockerfile based on PyPi manylinux https://github.com/pypa/manylinux

manylinux1 is the PEP for portable linux python wheels.

*Unfortunately* it is currently based on a Centos/5 build environment.
It is likely that sooner or later, manylinux2 will come out, but until then, a number of hacks are required.

This took a while to work out.

Here's a brief description of issues with work arounds:

1. `openssl-devel` provides openssl which results in undefined symbols
 * We download a newer openssl source, BUT: this requires Perl 5.10.0 to configure...
 * We download Perl 5.12 source and compile it first, then we can use that perl to...
 * Compile openssl from source, so we can link dynamically. This gives us the symbols and `auditwheel` will work out the rest.
   * (Apparently PyPi does this too on various `manylinux` wheels but they keep it a secret)
 
2. `libuv-devel` does not exist
 * We download and compile from source (1.1.0) , this surprisingly Just Works

3. `g++` does not support `--std=c++11` 
 * Save some time and fix 4. first (using the existing Centos/5 toolchain), then come back to this.
 * Install `devtools-2` which gives us a newer g++ and gcc in `/opt`
 * Fool the devtools compilers by replacing their `ld` executable (!)
   * The devtools compilers pass an option (`--build-info`) which the system default doesn't understand, so
     we actually replace their ld with a wrapper script (!) which seds out (!!) the invalid argument (!!!)
     then calls the system default ld (!!!!)

4. Centos/5 glibc doesn't contain `eventfd` but nothing newer is supported by `auditwheel`
 * We are restricted to GLIB 2.5 or earlier
 * But nobody says we can't link with a recompiled glibc...
  * After reviewing commit history (and trying some versions), glibc 2.10 seems the safest
  * Compile glibc 2.10 with the original (system default) gcc but the ABI restricted to GLIB 2.5
 * Fiddle with the linker options in `setup.py` so that the compiled glibc 2.10 is used as a *fall back*
    Rename it libc210.so.1
5. BONUS
 * If you try to compile glibc 2.10 statically instead of restricting the ABI, it won't work; you need to patch the Makeconfig
   Basically from [this commit](https://sourceware.org/git/?p=glibc.git;a=blobdiff;f=Makeconfig;h=e96ebc7e96f17c6ee3965cb4aff16cd07afdacbc;hp=42b836ee1815d78eb8ff0d230b140f7da6da611c;hb=94b32c39127967ea58adac3d737a1e5d6116fb77;hpb=15055a1cd7e2c249093a5f6d57eca817767d8b85)
    7 versions later...
   
6. Audit
