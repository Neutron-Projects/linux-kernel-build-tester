#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# Neutron Clang — Linux Kernel Build Tester
# ─────────────────────────────────────────────────────────────────────────────
#
# Usage:
#   ./build.sh <ARCH> [KERNEL_DIR]
#
# ARCH values:
#   X86 | X86_64       → native x86_64
#   ARM64 | AARCH64    → AArch64 cross-compile
#   ARM                → ARMv7 cross-compile
#
# Environment overrides:
#   TC_ROOT            toolchain root directory   (default: $HOME/neutron)
#   JOBS               parallel make jobs         (default: nproc)
#   BUILD_LOG          path for build log file    (default: /tmp/build-ARCH.log)
#   RESULT_JSON        path for result JSON file  (default: /tmp/result-ARCH.json)
#
# Output JSON schema (written to $RESULT_JSON):
#   status             "pass" | "fail"
#   arch               normalised arch string
#   kernel_version     from include/config/kernel.release
#   clang_version      from clang --version
#   toolchain_tag      from $TOOLCHAIN_TAG env (optional)
#   duration_seconds   integer
#   duration_human     "Xm Ys"
#   warnings           integer (lines matching ": warning:")
#   errors             integer (lines matching ": error:")
#   timestamp_start    ISO-8601 UTC
#   timestamp_end      ISO-8601 UTC
#   exit_code          integer
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

# ── Arguments ─────────────────────────────────────────────────────────────────

ARCH_RAW="${1:-}"
KERNEL_DIR="${2:-${HOME}/linux}"

if [[ -z "${ARCH_RAW}" ]]; then
    echo "Usage: $0 <ARCH> [KERNEL_DIR]"
    echo "  ARCH: X86 | ARM64 | ARM"
    exit 1
fi

# ── Normalise ARCH ────────────────────────────────────────────────────────────

case "${ARCH_RAW^^}" in
    X86|X86_64|X86-64)
        ARCH_NORM="x86_64"
        MAKE_ARCH="ARCH=x86_64"   # always explicit — prevents leaked ARCH env var
        CROSS_FLAGS=()
        ;;
    ARM64|AARCH64)
        ARCH_NORM="arm64"
        MAKE_ARCH="ARCH=arm64"
        CROSS_FLAGS=("CROSS_COMPILE=aarch64-linux-gnu-")
        ;;
    ARM|ARMV7|ARM32)
        ARCH_NORM="arm"
        MAKE_ARCH="ARCH=arm"
        CROSS_FLAGS=("CROSS_COMPILE=arm-linux-gnueabi-")
        ;;
    *)
        echo "ERROR: Unknown arch '${ARCH_RAW}'" >&2
        exit 1
        ;;
esac

# Unset ARCH from the environment — the workflow passes it as ARCH=X86 (uppercase)
# which make would inherit. We always pass ARCH= explicitly on the command line,
# so the env value is redundant and harmful.
unset ARCH

# ── Configuration ──────────────────────────────────────────────────────────────

TC_ROOT="${TC_ROOT:-${HOME}/neutron}"
TC_PATH="${TC_ROOT}/bin"
JOBS="${JOBS:-$(getconf _NPROCESSORS_ONLN)}"
BUILD_LOG="${BUILD_LOG:-/tmp/build-${ARCH_NORM}.log}"
RESULT_JSON="${RESULT_JSON:-/tmp/result-${ARCH_NORM}.json}"

# ── Helpers ───────────────────────────────────────────────────────────────────

log()  { printf '[%s] %s\n' "$(date -u +"%H:%M:%S")" "$*"; }
die()  { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
hr()   { printf '%0.s─' {1..72}; printf '\n'; }

emit_result() {
    local status="$1"
    local exit_code="${2:-0}"

    local time_end; time_end=$(date +%s)
    local duration=$(( time_end - _TIME_START ))
    local mins=$(( duration / 60 ))
    local secs=$(( duration % 60 ))
    local duration_fmt
    printf -v duration_fmt "%dm%02ds" "${mins}" "${secs}"

    local warnings=0 errors=0
    if [[ -f "${BUILD_LOG}" ]]; then
        warnings=$(grep -c ": warning:" "${BUILD_LOG}" || true)
        errors=$(grep -c ": error:" "${BUILD_LOG}" || true)
    fi

    local kernel_version=""
    if [[ -f "${KERNEL_DIR}/include/config/kernel.release" ]]; then
        kernel_version=$(cat "${KERNEL_DIR}/include/config/kernel.release")
    fi

    local clang_version=""
    if [[ -x "${TC_PATH}/clang" ]]; then
        clang_version=$("${TC_PATH}/clang" --version 2>/dev/null | head -1 || true)
    fi

    cat > "${RESULT_JSON}" <<JSON
{
  "status": "${status}",
  "arch": "${ARCH_NORM}",
  "kernel_version": "${kernel_version}",
  "clang_version": "${clang_version}",
  "toolchain_tag": "${TOOLCHAIN_TAG:-}",
  "duration_seconds": ${duration},
  "duration_human": "${duration_fmt}",
  "warnings": ${warnings},
  "errors": ${errors},
  "timestamp_start": "${_TIMESTAMP_START}",
  "timestamp_end": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "exit_code": ${exit_code}
}
JSON

    log "Result → ${RESULT_JSON}"
    hr
    if [[ "${status}" == "pass" ]]; then
        log "✓ BUILD PASSED  arch=${ARCH_NORM}  duration=${duration_fmt}  warnings=${warnings}"
    else
        log "✗ BUILD FAILED  arch=${ARCH_NORM}  duration=${duration_fmt}  errors=${errors}  warnings=${warnings}"
    fi
    hr
}

# ── Timing anchor ─────────────────────────────────────────────────────────────

_TIME_START=$(date +%s)
_TIMESTAMP_START=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# ── Sanity checks ──────────────────────────────────────────────────────────────

[[ -d "${KERNEL_DIR}" ]]    || die "Kernel directory not found: ${KERNEL_DIR}"
[[ -x "${TC_PATH}/clang" ]] || die "Clang not found at ${TC_PATH}/clang"

# ── Banner ─────────────────────────────────────────────────────────────────────

hr
log "Neutron Clang — Linux Kernel Build Tester"
log "  arch:       ${ARCH_NORM}"
log "  kernel dir: ${KERNEL_DIR}"
log "  toolchain:  ${TC_PATH}"
log "  jobs:       ${JOBS}"
log "  log:        ${BUILD_LOG}"
[[ -n "${TOOLCHAIN_TAG:-}" ]] && log "  tc tag:     ${TOOLCHAIN_TAG}"
hr

# ── Toolchain flags ────────────────────────────────────────────────────────────

export PATH="${TC_PATH}:${PATH}"

KMAKEFLAGS=(
    "LLVM=1"
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
    "HOSTLD=${TC_PATH}/ld.lld"
)

cd "${KERNEL_DIR}"

# ── distclean ──────────────────────────────────────────────────────────────────

log "Running: make distclean"
make -s distclean ${MAKE_ARCH} 2>&1 | tee -a "${BUILD_LOG}" || true

# ── defconfig ──────────────────────────────────────────────────────────────────

log "Running: make defconfig"
DEFCONFIG_ARGS=("defconfig" "${KMAKEFLAGS[@]}")
[[ -n "${MAKE_ARCH}" ]] && DEFCONFIG_ARGS+=("${MAKE_ARCH}")
[[ "${#CROSS_FLAGS[@]}" -gt 0 ]] && DEFCONFIG_ARGS+=("${CROSS_FLAGS[@]}")

make "${DEFCONFIG_ARGS[@]}" 2>&1 | tee -a "${BUILD_LOG}"

# ── build ──────────────────────────────────────────────────────────────────────

log "Running: make all -j${JOBS}"

BUILD_ARGS=(
    "all"
    "-j${JOBS}"
    "${KMAKEFLAGS[@]}"
)
[[ -n "${MAKE_ARCH}" ]] && BUILD_ARGS+=("${MAKE_ARCH}")
[[ "${#CROSS_FLAGS[@]}" -gt 0 ]] && BUILD_ARGS+=("${CROSS_FLAGS[@]}")

set +e
make "${BUILD_ARGS[@]}" 2>&1 | tee -a "${BUILD_LOG}"
BUILD_EXIT="${PIPESTATUS[0]}"
set -e

# ── result ─────────────────────────────────────────────────────────────────────

if [[ "${BUILD_EXIT}" -eq 0 ]]; then
    emit_result "pass" 0
else
    emit_result "fail" "${BUILD_EXIT}"
    exit "${BUILD_EXIT}"
fi
