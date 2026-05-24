#!/usr/bin/env python3
"""
resolve-matrix.py — Resolves current kernel versions from kernel.org and
outputs a GitHub Actions matrix JSON + per-version env vars.

Usage:
    python3 scripts/resolve-matrix.py \
        [--kernel-filter <channel|all>] \
        [--arch-filter   <arch|all>]    \
        [--output-env    $GITHUB_OUTPUT] \
        [--output-matrix $GITHUB_OUTPUT]

Writes to stdout and/or $GITHUB_OUTPUT:
    matrix=<json>
    ver_mainline=<version>
    ver_6_18=<version>
    ...
"""

import argparse
import json
import os
import sys
import urllib.request

KERNELS = [
    {"channel": "mainline", "series": "mainline", "label": "Mainline", "lts": False},
    {"channel": "lts-6.18", "series": "6.18",     "label": "6.18 LTS", "lts": True},
    {"channel": "lts-6.12", "series": "6.12",     "label": "6.12 LTS", "lts": True},
    {"channel": "lts-6.6",  "series": "6.6",      "label": "6.6 LTS",  "lts": True},
    {"channel": "lts-6.1",  "series": "6.1",      "label": "6.1 LTS",  "lts": True},
    {"channel": "lts-5.15", "series": "5.15",     "label": "5.15 LTS", "lts": True},
]

ARCHES = [
    {"arch": "ARM64", "label": "arm64"},
    {"arch": "ARM",   "label": "arm"},
    {"arch": "X86",   "label": "x86_64"},
]


def fetch_releases():
    url = "https://www.kernel.org/releases.json"
    req = urllib.request.Request(url, headers={"User-Agent": "neutron-build-tester/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def resolve_version(releases, series):
    """Return latest non-rc, non-eol version for a series (or 'stable' for mainline)."""
    if series == "mainline":
        # prefer moniker == 'stable', no rc
        for r in releases["releases"]:
            if r.get("moniker") == "stable" and not r.get("iseol", False):
                v = r["version"]
                if "-rc" not in v:
                    return v
        # fallback: any non-eol, non-rc
        for r in releases["releases"]:
            if not r.get("iseol", False) and "-rc" not in r["version"]:
                return r["version"]
        return ""

    # LTS/stable series: find latest point release for that major.minor
    prefix = series + "."
    for r in releases["releases"]:
        v = r["version"]
        if (v.startswith(prefix) or v == series) and not r.get("iseol", False):
            if "-rc" not in v:
                return v
    # fallback: include eol too (we still want to test against it)
    for r in releases["releases"]:
        v = r["version"]
        if (v.startswith(prefix) or v == series) and "-rc" not in v:
            return v
    return ""


def build_matrix(versions, kernel_filter="all", arch_filter="all"):
    kernels = [k for k in KERNELS if versions.get(k["channel"])]

    if kernel_filter and kernel_filter not in ("all", ""):
        kernels = [k for k in kernels
                   if k["channel"] == kernel_filter or k["series"] == kernel_filter]

    arches = list(ARCHES)
    if arch_filter and arch_filter not in ("all", ""):
        arches = [a for a in arches
                  if a["label"] == arch_filter or a["arch"].lower() == arch_filter]

    matrix = {"include": []}
    for k in kernels:
        ver = versions[k["channel"]]
        for a in arches:
            matrix["include"].append({
                "kernel_channel": k["channel"],
                "kernel_series":  k["series"],
                "kernel_version": ver,
                "kernel_label":   k["label"],
                "arch":           a["arch"],
                "arch_label":     a["label"],
                "job_name":       f"{k['label']} / {a['label']}",
            })
    return matrix


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kernel-filter", default="all")
    p.add_argument("--arch-filter",   default="all")
    p.add_argument("--output-env",    default=os.environ.get("GITHUB_OUTPUT", ""))
    args = p.parse_args()

    print("Fetching kernel.org/releases.json …", flush=True)
    releases = fetch_releases()

    versions = {}
    for k in KERNELS:
        v = resolve_version(releases, k["series"])
        versions[k["channel"]] = v
        tag = "LTS" if k["lts"] else "   "
        print(f"  {tag}  {k['channel']:<12}  →  {v or '(not found)'}")

    matrix = build_matrix(versions, args.kernel_filter, args.arch_filter)
    print(f"\nMatrix: {len(matrix['include'])} job(s) after filtering "
          f"(kernel={args.kernel_filter}, arch={args.arch_filter})")

    if args.output_env:
        with open(args.output_env, "a") as f:
            f.write(f"matrix={json.dumps(matrix)}\n")
            f.write(f"matrix_count={len(matrix['include'])}\n")
            for k in KERNELS:
                env_key = "ver_" + k["channel"].replace("-", "_").replace(".", "_")
                f.write(f"{env_key}={versions.get(k['channel'], '')}\n")
        print(f"Wrote {len(matrix['include'])} matrix entries to GITHUB_OUTPUT")
    else:
        print(json.dumps(matrix, indent=2))


if __name__ == "__main__":
    main()
