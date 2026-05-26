<div align="center">

# 🔨 linux-kernel-build-tester

**Automated Linux kernel build matrix for [Neutron Clang](https://github.com/Neutron-Toolchains/clang-build-catalogue)**

Builds every active LTS and mainline kernel against `arm64`, `arm`, and `x86_64`  
on every new toolchain release — automatically.

---

### Toolchain

[![Neutron Clang](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/toolchain.json&style=flat-square)](https://github.com/Neutron-Toolchains/clang-build-catalogue)

### Build Status

| | Kernel | `arm64` | `arm` | `x86_64` |
|:-:|:-------|:-------:|:-----:|:--------:|
| [![mainline](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/mainline.json&style=flat-square&label=)](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml) | **Mainline** | ![](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml/badge.svg) | | |
| [![lts-6.18](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.18.json&style=flat-square&label=)](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml) | **6.18 LTS** | | | |
| [![lts-6.12](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.12.json&style=flat-square&label=)](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml) | **6.12 LTS** | | | |
| [![lts-6.6](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.6.json&style=flat-square&label=)](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml) | **6.6 LTS** | | | |
| [![lts-6.1](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.1.json&style=flat-square&label=)](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml) | **6.1 LTS** | | | |
| [![lts-5.15](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-5.15.json&style=flat-square&label=)](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml) | **5.15 LTS** | | | |

</div>

---

<!-- BUILD_TABLE_START -->

> **Neutron Clang:** [`23.0.0git`](https://github.com/Neutron-Toolchains/clang-build-catalogue/releases/tag/26052026)&emsp;**Tag:** `26052026`
> **Last run:** [26 May 2026 15:24 UTC](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561)

| Kernel | Version | `arm64` | `arm` | `x86_64` |
|:-------|:--------|:-------:|:-----:|:--------:|
| **Mainline** | `7.0.10` | [✅ `37m51s`](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) | [✅ `18m24s` ⚠366](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) | [✅ `8m52s`](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) |
| **6.18 LTS** | `6.18.33` | [✅ `31m23s` ⚠1](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) | [✅ `17m09s` ⚠366](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) | [❌](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) |
| **6.12 LTS** | `6.12.91` | [✅ `25m36s` ⚠2](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) | [✅ `11m08s` ⚠361](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) | [✅ `8m05s` ⚠2](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) |
| **6.6 LTS** | `6.6.141` | [✅ `24m00s` ⚠2](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) | [✅ `13m42s` ⚠355](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) | [✅ `7m58s` ⚠2](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) |
| **6.1 LTS** | `6.1.174` | [✅ `23m16s` ⚠4](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) | [✅ `14m03s` ⚠366](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) | [✅ `7m19s` ⚠3](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) |
| **5.15 LTS** | `5.15.208` | [✅ `17m25s` ⚠2](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) | [✅ `13m27s` ⚠363](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) | [✅ `6m11s` ⚠3](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/26455468561) |

<sub>✅ pass · ❌ fail · ⬜ not run · ⚠N = N compiler warnings · time shown for passing builds</sub>

<!-- BUILD_TABLE_END -->

---

## How It Works

```
Neutron Toolchains/clang-build-catalogue
        │  new release pushed
        ▼
check-toolchain.yml  (polls every 6 h via cron)
        │  new tag detected
        ▼
build-matrix.yml  ──────────────────────────────────────────────────────────┐
        │                                                                    │
        ├─ setup: resolve kernel.org versions + build JSON matrix            │
        │                                                                    │
        ├─ build (×18 parallel jobs):                                        │
        │    ┌─────────────────────┬──────────────┬───────────────────┐     │
        │    │  kernel channel     │  arch        │  what             │     │
        │    ├─────────────────────┼──────────────┼───────────────────┤     │
        │    │  mainline           │  arm64       │  fetch tarball    │     │
        │    │  lts-6.18           │  arm         │  sync toolchain   │     │
        │    │  lts-6.12           │  x86_64      │  defconfig + all  │     │
        │    │  lts-6.6            │              │  emit result.json │     │
        │    │  lts-6.1            │              │                   │     │
        │    │  lts-5.15           │              │                   │     │
        │    └─────────────────────┴──────────────┴───────────────────┘     │
        │                                                                    │
        └─ update-status: aggregate → badges → README → git push ───────────┘
```

### Kernel version resolution

Kernel versions are resolved **at run time** from [`kernel.org/releases.json`](https://www.kernel.org/releases.json) — the matrix always builds against the latest point release for each tracked series, no manual pinning required.

| Channel   | Series | Type    | EOL       |
|:----------|:-------|:--------|:----------|
| `mainline` | —     | Stable  | ~4 months |
| `lts-6.18` | 6.18  | LTS     | Dec 2028  |
| `lts-6.12` | 6.12  | LTS     | Dec 2028  |
| `lts-6.6`  | 6.6   | LTS     | Dec 2027  |
| `lts-6.1`  | 6.1   | LTS     | Dec 2027  |
| `lts-5.15` | 5.15  | LTS     | Dec 2026  |

---

## Triggering a Build

### Automatic

`check-toolchain.yml` polls the [clang-build-catalogue](https://github.com/Neutron-Toolchains/clang-build-catalogue) every **6 hours**. When a new toolchain tag is detected (comparing against `state/last-toolchain.txt`), it dispatches `build-matrix.yml` automatically.

### Manual — GitHub UI

Go to **Actions → 🔨 Build Matrix → Run workflow** and fill in the inputs:

| Input | Description | Default |
|:------|:------------|:--------|
| `toolchain_tag` | Specific Neutron Clang tag (e.g. `22052026`) | latest |
| `clang_version` | Clang version string (informational) | — |
| `kernel_filter` | Build only one channel | `all` |
| `arch_filter`   | Build only one arch | `all` |
| `triggered_by`  | Label for the commit message | `manual` |

### Manual — REST API

```bash
curl -X POST \
  -H "Authorization: Bearer <GITHUB_TOKEN>" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "toolchain_tag": "22052026",
      "kernel_filter": "all",
      "arch_filter":   "all",
      "triggered_by":  "api"
    }
  }'
```

**Force a toolchain re-check via API:**

```bash
curl -X POST \
  -H "Authorization: Bearer <GITHUB_TOKEN>" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Neutron-Projects/linux-kernel-build-tester/actions/workflows/check-toolchain.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "force_build": "true"
    }
  }'
```

---

## Build Metrics

Each build job emits a `result.json` artifact with:

```jsonc
{
  "status":           "pass",          // "pass" | "fail"
  "arch":             "arm64",
  "kernel_version":   "7.0.9",
  "kernel_channel":   "mainline",
  "kernel_label":     "Mainline",
  "clang_version":    "Neutron Clang 20.0.0git …",
  "toolchain_tag":    "22052026",
  "duration_seconds": 342,
  "duration_human":   "5m42s",
  "warnings":         4,               // lines matching ": warning:"
  "errors":           0,               // lines matching ": error:"
  "timestamp_start":  "2026-05-22T04:00:01Z",
  "timestamp_end":    "2026-05-22T04:05:43Z",
  "run_url":          "https://github.com/…/actions/runs/…",
  "exit_code":        0
}
```

Artifacts are retained for **90 days** (build logs kept for **14 days** on failure).

---

## Repository Layout

```
.
├── build.sh                         # Build entrypoint — called per arch
├── scripts/
│   ├── fetch-kernel.sh              # Standalone kernel tarball fetcher
│   ├── resolve-matrix.py            # Resolves kernel.org versions → matrix JSON
│   ├── inject-result-context.py     # Adds channel/label metadata to result.json
│   ├── update-status.py             # Aggregates results → state + README
│   └── print-summary.py             # Prints build table to stdout + step summary
├── state/
│   ├── build-status.json            # Live build state (committed after each run)
│   ├── last-toolchain.txt           # Last tested toolchain tag (for change detection)
│   └── badges/
│       ├── all.json                 # shields.io endpoint — aggregate
│       ├── toolchain.json           # shields.io endpoint — toolchain version
│       ├── mainline.json            # shields.io endpoint — per-kernel
│       ├── lts-6.18.json
│       ├── lts-6.12.json
│       ├── lts-6.6.json
│       ├── lts-6.1.json
│       └── lts-5.15.json
└── .github/workflows/
    ├── check-toolchain.yml          # Cron poller + dispatch trigger
    └── build-matrix.yml             # Full build matrix + status updater
```

---

## Badge Integration

Per-kernel shields.io endpoint badges can be embedded anywhere:

```markdown
![mainline](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/mainline.json&style=flat-square)
![6.18 LTS](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.18.json&style=flat-square)
![6.12 LTS](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.12.json&style=flat-square)
![6.6 LTS](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.6.json&style=flat-square)
![6.1 LTS](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.1.json&style=flat-square)
![5.15 LTS](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-5.15.json&style=flat-square)
```

---

<div align="center">
<sub>
Builds run inside
<a href="https://github.com/Neutron-Projects/docker-image"><code>ghcr.io/neutron-projects/docker-image:arch-neutron</code></a>
·
Toolchain managed by
<a href="https://github.com/Neutron-Toolchains/antman">antman</a>
·
Kernel versions from
<a href="https://www.kernel.org/releases.json">kernel.org/releases.json</a>
</sub>
</div>
