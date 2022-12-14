#!/bin/bash
set -e

export LINUX_VER=$(curl -sL "https://www.kernel.org" | grep -A 1 "latest_link" | tail -n +2 | sed 's|.*">||' | sed 's|</a>||')
export BUILDDIR=$(pwd)
export KERNEL_DIR="$BUILDDIR/linux-$LINUX_VER"

if [ -d "$KERNEL_DIR"/ ]; then
	echo "Kernel dir found"
else
	wget "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-$LINUX_VER.tar.xz"
	tar xvf linux-$LINUX_VER.tar.xz
fi

if [ -d "$KERNEL_DIR/clang"/ ]; then
	echo "clang dir found"
else
	cd "$KERNEL_DIR"
	git clone https://github.com/Neutron-Toolchains/neutron-clang.git clang
fi

cd "$KERNEL_DIR/clang"
bash antman -S

cd "$BUILDDIR"
if [[ $1 == "X86" ]]; then
	bash x86.sh
elif [[ $1 == "ARM64" ]]; then
	bash arm64.sh
elif [[ $1 == "ARM" ]]; then
	bash arm.sh
fi
