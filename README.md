<div align="center">

# Linux Kernel Build Tester

Automated Linux kernel builds for [Neutron Clang](https://github.com/Neutron-Toolchains/clang-build-catalogue).
The build matrix is resolved at runtime from kernel.org, so the repo always tracks the current mainline RC, the current stable release, and every active longterm series.

<p>
  <a href="https://github.com/Neutron-Toolchains/clang-build-catalogue"><img alt="Neutron Clang" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/toolchain.json&style=flat-square" /></a>
  <a href="https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml"><img alt="Kernel builds" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/all.json&style=flat-square" /></a>
  <a href="https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml"><img alt="Mainline" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/mainline.json&style=flat-square" /></a>
  <a href="https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml"><img alt="Stable" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/stable.json&style=flat-square" /></a>
  <a href="https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml"><img alt="6.18 LTS" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.18.json&style=flat-square" /></a>
  <a href="https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml"><img alt="6.12 LTS" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.12.json&style=flat-square" /></a>
  <a href="https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml"><img alt="6.6 LTS" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.6.json&style=flat-square" /></a>
  <a href="https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml"><img alt="6.1 LTS" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.1.json&style=flat-square" /></a>
  <a href="https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/workflows/build-matrix.yml"><img alt="5.15 LTS" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-5.15.json&style=flat-square" /></a>
</p>

---

## Overview

This repository runs a fan-out Linux kernel build matrix across `arm64`, `arm`, and `x86_64` using the current Neutron Clang toolchain.
Kernel versions are resolved from kernel.org at runtime, so the active mainline, stable, and longterm series do not need manual pinning.

<!-- BUILD_TABLE_START -->

> **Neutron Clang:** [`23.0.0git`](https://github.com/Neutron-Toolchains/clang-build-catalogue/releases/tag/09062026)&emsp;**Tag:** `09062026`
> **Last run:** [09 Jun 2026 15:02 UTC](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829)

| Kernel | Version | `arm64` | `arm` | `x86_64` |
|:-------|:--------|:-------:|:-----:|:--------:|
| **Mainline** | `7.1-rc7` | [✅ `31m38s`](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `19m36s`](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `8m45s`](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) |
| **Stable** | `7.0.12` | [✅ `34m15s`](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `19m24s`](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `8m53s`](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) |
| **6.18 LTS** | `6.18.35` | [✅ `31m24s` ⚠1](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `16m43s` ⚠1](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [❌](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) |
| **6.12 LTS** | `6.12.93` | [✅ `27m03s` ⚠2](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `15m35s` ⚠2](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `8m29s` ⚠2](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) |
| **6.6 LTS** | `6.6.142` | [✅ `23m21s` ⚠2](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `13m46s` ⚠356](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `7m50s` ⚠2](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) |
| **6.1 LTS** | `6.1.175` | [✅ `20m54s` ⚠2](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `13m55s` ⚠364](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `7m43s` ⚠2](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) |
| **5.15 LTS** | `5.15.209` | [✅ `16m44s` ⚠1](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `12m07s` ⚠362](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `6m11s` ⚠3](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) |
| **5.10 LTS** | `5.10.258` | [✅ `12m24s` ⚠2](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `11m21s` ⚠358](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) | [✅ `4m30s` ⚠38](https://github.com/Neutron-Projects/linux-kernel-build-tester/actions/runs/27213102829) |

<sub>✅ pass · ❌ fail · ⬜ not run · ⚠N = N compiler warnings · time shown for passing builds</sub>

<!-- BUILD_TABLE_END -->

---

## How It Works

```mermaid
flowchart TD
    A[Neutron Clang release] --> B[check-toolchain.yml]
    B --> C[build-matrix.yml setup]
    C --> D[Resolve kernel.org releases.json]
    D --> E[Build matrix includes mainline, stable, and active LTS tracks]
    E --> F[Parallel builds on arm64 / arm / x86_64]
    F --> G[update-status.py refreshes state, badges, and README]
```

Mainline rows also capture the current upstream HEAD commit so a failed snapshot can be reproduced more easily later.

### Track Resolution

| Track | Source | Notes |
|:------|:-------|:------|
| `mainline` | kernel.org `moniker: mainline` | Current rc snapshot; result.json stores the current HEAD commit |
| `stable` | kernel.org `moniker: stable` | Current stable release |
| `lts-*` | kernel.org `moniker: longterm` | Active longterm series are discovered dynamically |

---

## Triggering a Build

### Automatic

`check-toolchain.yml` polls the [clang-build-catalogue](https://github.com/Neutron-Toolchains/clang-build-catalogue) every 6 hours and dispatches `build-matrix.yml` when a new toolchain tag appears.

### Manual

Use **Actions → 🔨 Build Matrix → Run workflow** and fill in the inputs:

| Input | Description | Default |
|:------|:------------|:--------|
| `toolchain_tag` | Specific Neutron Clang tag, or empty for the latest catalogue entry | latest |
| `clang_version` | Clang version string for display only | — |
| `llvm_commit` | LLVM commit URL for display only | — |
| `kernel_filter` | Limit to one kernel channel, series, or label | `all` |
| `arch_filter` | Limit to one architecture | `all` |
| `triggered_by` | Label used in the commit message | `manual` |

### REST API

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
      "arch_filter": "all",
      "triggered_by": "api"
    }
  }'
```

To force a catalogue refresh:

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
  "status": "pass",
  "arch": "arm64",
  "kernel_version": "7.1-rc6",
  "kernel_channel": "mainline",
  "kernel_label": "Mainline",
  "kernel_head_commit": "ba3e43a9e601636f5edb54e259a74f96ca3b8fd8",
  "clang_version": "Neutron Clang 23.0.0git …",
  "toolchain_tag": "22052026",
  "duration_seconds": 342,
  "duration_human": "5m42s",
  "warnings": 4,
  "errors": 0,
  "timestamp_start": "2026-05-22T04:00:01Z",
  "timestamp_end": "2026-05-22T04:05:43Z",
  "run_url": "https://github.com/…/actions/runs/…",
  "exit_code": 0
}
```

Artifacts are retained for 90 days. Failure logs are kept for 14 days.

---

## Badge Integration

```markdown
![mainline](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/mainline.json&style=flat-square)
![stable](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/stable.json&style=flat-square)
![6.18 LTS](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.18.json&style=flat-square)
![6.12 LTS](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.12.json&style=flat-square)
![6.6 LTS](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.6.json&style=flat-square)
![6.1 LTS](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-6.1.json&style=flat-square)
![5.15 LTS](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Neutron-Projects/linux-kernel-build-tester/main/state/badges/lts-5.15.json&style=flat-square)
```

---
·
Kernel versions from
<a href="https://www.kernel.org/releases.json">kernel.org/releases.json</a>
</sub>
</div>
