#!/bin/bash

args=$(echo $@ | sed -e 's/--build-id//g')
if ( echo $args | grep "@" ); then
	f=$(echo $args | sed -e 's/^@//g')
	sed -e 's/--build-id//g' -i $f
fi
echo -e "\n\nRun linker:\t$args\n\n" 1>&2
ld $args
