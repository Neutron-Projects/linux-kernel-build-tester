#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# Fetch the correct Linux kernel tarball for a given channel or version.
#
# Usage:
#   ./fetch-kernel.sh <channel-or-version> [dest-dir]
#
# Channels:
#   mainline            → latest stable release (e.g. 7.0.9)
#   lts-6.18            → latest 6.18.x LTS point release
#   lts-6.12            → latest 6.12.x LTS point release
#   lts-6.6             → latest 6.6.x  LTS point release
#   lts-6.1             → latest 6.1.x  LTS point release
#   lts-5.15            → latest 5.15.x LTS point release
#   lts-5.10            → latest 5.10.x LTS point release
#   <version>           → explicit version string (e.g. 6.12.90)
#
# Outputs:
#   <dest-dir>/linux/   extracted kernel source tree
#   <dest-dir>/linux/.kernel-version   the resolved version string
#   <dest-dir>/linux/.kernel-channel   the channel used
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

CHANNEL="${1:-mainline}"
DEST_DIR="${2:-${HOME}}"

log() { printf '[fetch-kernel] %s\n' "$*"; }
die() { printf '[fetch-kernel] ERROR: %s\n' "$*" >&2; exit 1; }

# ── Fetch kernel.org releases JSON ────────────────────────────────────────────

log "Fetching kernel.org/releases.json…"
RELEASES_JSON=$(curl -sf "https://www.kernel.org/releases.json") \
    || die "Failed to fetch kernel.org/releases.json"

# ── Resolve version for channel ───────────────────────────────────────────────

resolve_version() {
    local channel="$1"
    python3 - "${channel}" <<'PYEOF'
import json, sys, re

channel = sys.argv[1]

with open('/dev/stdin') as f:
    raw = f.read()

data = json.loads(raw)

def get_stable():
    for r in data['releases']:
        if r['moniker'] in ('stable',) and not r.get('iseol', False):
            v = r['version']
            if '-rc' not in v:
                return v
    # fallback: first non-rc non-eol
    for r in data['releases']:
        if not r.get('iseol', False) and '-rc' not in r['version']:
            return r['version']
    return ''

def get_series(series):
    for r in data['releases']:
        v = r['version']
        if (v.startswith(series + '.') or v == series) and not r.get('iseol', False):
            if '-rc' not in v:
                return v
    # fallback: might be EOL but we still want it for testing
    for r in data['releases']:
        v = r['version']
        if v.startswith(series + '.') or v == series:
            if '-rc' not in v:
                return v
    return ''

series_map = {
    'mainline':  get_stable,
    'stable':    get_stable,
    'lts-6.18':  lambda: get_series('6.18'),
    'lts-6.12':  lambda: get_series('6.12'),
    'lts-6.6':   lambda: get_series('6.6'),
    'lts-6.1':   lambda: get_series('6.1'),
    'lts-5.15':  lambda: get_series('5.15'),
    'lts-5.10':  lambda: get_series('5.10'),
}

if channel in series_map:
    version = series_map[channel]()
elif re.match(r'^\d+\.\d+', channel):
    # Treat as explicit version
    version = channel
else:
    version = ''

if not version:
    print('ERROR: could not resolve version', file=sys.stderr)
    sys.exit(1)

print(version)
PYEOF
}

if [[ "${CHANNEL}" =~ ^[0-9]+\.[0-9]+ ]]; then
    # Explicit version string passed directly
    KERNEL_VERSION="${CHANNEL}"
    log "Explicit version: ${KERNEL_VERSION}"
else
    log "Resolving channel '${CHANNEL}'…"
    KERNEL_VERSION=$(echo "${RELEASES_JSON}" | resolve_version "${CHANNEL}")
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
