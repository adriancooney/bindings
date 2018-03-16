#!/bin/bash

args=$(echo $@ | sed -e 's/--build-id//g')
for f in crtbeginS.o crtendS.o; do
	HACK_PATH="/opt/rh/devtoolset-2/root/usr/lib/gcc/x86_64-CentOS-linux/4.8.2/$f"
	ORIG_PATH="/usr/lib/gcc/x86_64-redhat-linux/4.1.1/$f"
	args=$(echo $args | sed -e "s%${HACK_PATH}%${ORIG_PATH}%g")
done

#args=$(echo $args | sed -e "s%crtendS.o%crtend.o%g")

echo -e "\n\nRun linker:\t$args\n\n" 1>&2 | tee /vagrant/debug.ld
ld $args
