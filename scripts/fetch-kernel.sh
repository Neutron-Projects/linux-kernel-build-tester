#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# Fetch the correct Linux kernel tarball for a given channel or version.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

CHANNEL="${1:-mainline}"
DEST_DIR="${2:-${HOME}}"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

log() { printf '[fetch-kernel] %s\n' "$*"; }
die() { printf '[fetch-kernel] ERROR: %s\n' "$*" >&2; exit 1; }

if [[ "${CHANNEL}" =~ ^[0-9]+\.[0-9]+ ]]; then
    # Explicit version string passed directly
    KERNEL_VERSION="${CHANNEL}"
    log "Explicit version: ${KERNEL_VERSION}"
else
    log "Resolving channel '${CHANNEL}'…"
    KERNEL_VERSION=$(python3 "${SCRIPT_DIR}/kernel_releases.py" resolve-version "${CHANNEL}") \
        || die "could not resolve version for channel '${CHANNEL}'"
    log "Resolved: ${KERNEL_VERSION}"
fi

[[ -n "${KERNEL_VERSION}" ]] || die "Empty kernel version for channel '${CHANNEL}'"

# ── Build tarball URL ─────────────────────────────────────────────────────────

MAJOR=$(echo "${KERNEL_VERSION}" | cut -d. -f1)
TARBALL="linux-${KERNEL_VERSION}.tar.xz"
TARBALL_SIG="${TARBALL}.sign"
URL="https://cdn.kernel.org/pub/linux/kernel/v${MAJOR}.x/${TARBALL}"

log "Kernel:  ${KERNEL_VERSION}"
log "URL:     ${URL}"
log "Dest:    ${DEST_DIR}"

# ── Download ──────────────────────────────────────────────────────────────────

cd "${DEST_DIR}"

if [[ -f "${TARBALL}" ]]; then
    log "Tarball already present, skipping download"
else
    log "Downloading…"
    curl -fL# --retry 3 --retry-delay 5 -o "${TARBALL}" "${URL}"
fi

# ── Extract ───────────────────────────────────────────────────────────────────

log "Extracting…"
tar -xf "${TARBALL}" --checkpoint=5000 --checkpoint-action=echo="%u records"
mv "linux-${KERNEL_VERSION}" linux

# ── Stamp metadata ────────────────────────────────────────────────────────────

echo "${KERNEL_VERSION}" > linux/.kernel-version
echo "${CHANNEL}"        > linux/.kernel-channel

log "Done. Source ready at ${DEST_DIR}/linux (${KERNEL_VERSION})"
