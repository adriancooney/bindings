# Get python builds from manylinux project
FROM quay.io/pypa/manylinux1_x86_64:latest

# manylinux is Centos/5 which does not work out of the box

# Install development libraries
RUN yum -y install \
        which \
        openssl-devel \
        glibc-devel \
        libstdc++-devel \
        mlocate \
        unzip \
        zip \
        gcc \
        gcc-c++
        
RUN curl http://people.centos.org/tru/devtools-2/devtools-2.repo -o /etc/yum.repos.d/devtools-2.repo && \
    yum install devtoolset-2-gcc devtoolset-2-binutils devtoolset-2-gcc-c++
    

# Compile static glibc    
RUN curl https://codeload.github.com/bminor/glibc/tar.gz/glibc-2.9 -o glibc.tar.gz && \
    tar -xvf glibc.tar.gz && \
    cd glibc-glibc-2.9/ && mkdir -p build && cd build && ../configure --disable-shared --prefix=/opt/glibc2.9
    
    

RUN curl https://codeload.github.com/libuv/libuv/tar.gz/v1.10.2 -o libuv.tar.gz

# Setup vagrant with ssh
ADD docker-common.sh /docker-common.sh
RUN bash docker-common.sh && rm -f docker-common.sh
        
EXPOSE 22
ENTRYPOINT ["/usr/sbin/sshd", "-D"]
