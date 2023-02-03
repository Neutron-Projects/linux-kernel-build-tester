#!/bin/bash
set -e

export TC_PATH="$HOME/neutron/bin"
export PATH="$HOME/neutron/bin:$PATH"

KMAKEFLAGS=("LLVM=1"
    "LLVM_IAS=1"
    "CC=${TC_PATH}/clang"
    "LD=${TC_PATH}/ld.lld"
    "AR=${TC_PATH}/llvm-ar"
    "NM=${TC_PATH}/llvm-nm"
    "STRIP=${TC_PATH}/llvm-strip"
    "OBJCOPY=${TC_PATH}/llvm-objcopy"
    "OBJDUMP=${TC_PATH}/llvm-objdump"
    "READELF=${TC_PATH}/llvm-readelf"
    "HOSTCC=${TC_PATH}/clang"
    "HOSTCXX=${TC_PATH}/clang++"
    "HOSTAR=${TC_PATH}/llvm-ar"
    "HOSTLD=${TC_PATH}/ld.lld")

if [[ $1 == "X86" ]]; then
    make distclean defconfig all -sj"$(getconf _NPROCESSORS_ONLN)" \
        "${KMAKEFLAGS[@]}"
elif [[ $1 == "ARM64" ]]; then
    make distclean defconfig all -sj"$(getconf _NPROCESSORS_ONLN)" \
        "${KMAKEFLAGS[@]}" \
        ARCH=arm64 \
        CROSS_COMPILE=aarch64-linux-gnu-
elif [[ $1 == "ARM" ]]; then
    make distclean defconfig all -sj"$(getconf _NPROCESSORS_ONLN)" \
        "${KMAKEFLAGS[@]}" \
        ARCH=arm \
        CROSS_COMPILE=arm-linux-gnueabi-
else
    echo "Invalid arch: $1"
    exit 1
fi
