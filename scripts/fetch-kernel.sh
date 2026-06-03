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

log "Resolving channel '${CHANNEL}'…"
DOWNLOAD_INFO=$(python3 "${SCRIPT_DIR}/kernel_releases.py" download-info "${CHANNEL}") \
    || die "could not resolve download info for channel '${CHANNEL}'"

KERNEL_VERSION=$(printf '%s' "${DOWNLOAD_INFO}" | python3 -c 'import json,sys; print(json.load(sys.stdin)["version"])')
DOWNLOAD_URL=$(printf '%s' "${DOWNLOAD_INFO}" | python3 -c 'import json,sys; print(json.load(sys.stdin)["source"])')

if [[ -z "${KERNEL_VERSION}" || -z "${DOWNLOAD_URL}" ]]; then
    die "could not resolve download metadata for channel '${CHANNEL}'"
fi

log "Resolved: ${KERNEL_VERSION}"

[[ -n "${KERNEL_VERSION}" ]] || die "Empty kernel version for channel '${CHANNEL}'"

log "Kernel:  ${KERNEL_VERSION}"
log "URL:     ${DOWNLOAD_URL}"
log "Dest:    ${DEST_DIR}"

# ── Download ──────────────────────────────────────────────────────────────────

cd "${DEST_DIR}"

TARBALL_NAME="$(basename -- "${DOWNLOAD_URL}")"

if [[ -f "${TARBALL_NAME}" ]]; then
    log "Tarball already present, skipping download"
else
    log "Downloading…"
    curl -fL# --retry 3 --retry-delay 5 -o "${TARBALL_NAME}" "${DOWNLOAD_URL}"
fi

# ── Extract ───────────────────────────────────────────────────────────────────

log "Extracting…"
tar -xf "${TARBALL_NAME}" --checkpoint=5000 --checkpoint-action=echo="%u records"
mv "linux-${KERNEL_VERSION}" linux

# ── Stamp metadata ────────────────────────────────────────────────────────────

echo "${KERNEL_VERSION}" > linux/.kernel-version
echo "${CHANNEL}"        > linux/.kernel-channel

log "Done. Source ready at ${DEST_DIR}/linux (${KERNEL_VERSION})"
