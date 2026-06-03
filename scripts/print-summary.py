#!/usr/bin/env python3
"""Print the build matrix table to stdout and GITHUB_STEP_SUMMARY."""

import json
import os
from pathlib import Path

from kernel_releases import channel_sort_key

sf = Path("state/build-status.json")
if not sf.exists():
    print("No state/build-status.json found"); raise SystemExit(0)

status = json.loads(sf.read_text())
builds = status.get("builds", {})
tc     = status.get("toolchain", {})
track_order = status.get("track_order", [])
track_meta  = status.get("track_meta", {})

ARCHES  = ["arm64","arm","x86_64"]
EMOJI = {"pass": "✅", "fail": "❌", "unknown": "⬜"}

if not track_order:
    track_order = sorted({key.split("/")[0] for key in builds}, key=channel_sort_key)

rows = []
total_p = total_f = 0
for k in track_order:
    cells = []
    ver = track_meta.get(k, {}).get("version", "")
    for a in ARCHES:
        b = builds.get(f"{k}/{a}", {})
        if not ver:
            ver = b.get("kernel_version", "")
        s = b.get("status", "unknown")
        if s == "pass":
            total_p += 1
        elif s == "fail":
            total_f += 1
        dur = f" `{b['duration']}`" if s == "pass" and b.get("duration") else ""
        cells.append(EMOJI.get(s, "⬜") + dur)
    rows.append(f"| **{track_meta.get(k, {}).get('label', k)}** | `{ver or '?'}` | {' | '.join(cells)} |")

header = f"Neutron Clang {tc.get('clang_version','?')} ({tc.get('tag','?')})"
print(f"\n{header}")
print(f"Passed: {total_p} / Failed: {total_f} / Total: {total_p+total_f}\n")
print("| Kernel | Version | arm64 | arm | x86_64 |")
print("|:-------|:--------|:-----:|:---:|:------:|")
for r in rows:
    print(r)

# Append to step summary if running in GitHub Actions
summary_path = os.environ.get("GITHUB_STEP_SUMMARY", "")
if summary_path:
    with open(summary_path, "a") as f:
        f.write(f"\n## Build Matrix Summary\n")
        f.write(f"**Neutron Clang** `{tc.get('clang_version','?')}` tag `{tc.get('tag','?')}`\n\n")
        f.write("| Kernel | Version | arm64 | arm | x86_64 |\n")
        f.write("|:-------|:--------|:-----:|:---:|:------:|\n")
        for r in rows:
            f.write(r + "\n")
        f.write(f"\n**{total_p} passed** · **{total_f} failed**\n")
    print(f"\nWrote summary to {summary_path}")
