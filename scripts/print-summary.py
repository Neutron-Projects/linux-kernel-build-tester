#!/usr/bin/env python3
"""
print-summary.py  —  Prints the build matrix table to stdout and GITHUB_STEP_SUMMARY.
"""
import json, os
from pathlib import Path

sf = Path("state/build-status.json")
if not sf.exists():
    print("No state/build-status.json found"); raise SystemExit(0)

status = json.loads(sf.read_text())
builds = status.get("builds", {})
tc     = status.get("toolchain", {})

KERNELS = ["mainline","lts-6.18","lts-6.12","lts-6.6","lts-6.1","lts-5.15"]
ARCHES  = ["arm64","arm","x86_64"]
LABELS  = {
    "mainline":  "Mainline",
    "lts-6.18":  "6.18 LTS",
    "lts-6.12":  "6.12 LTS",
    "lts-6.6":   "6.6 LTS",
    "lts-6.1":   "6.1 LTS",
    "lts-5.15":  "5.15 LTS",
}
EMOJI = {"pass": "✅", "fail": "❌", "unknown": "⬜"}

rows = []
total_p = total_f = 0
for k in KERNELS:
    cells = []
    ver = ""
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
    rows.append(f"| **{LABELS[k]}** | `{ver or '?'}` | {' | '.join(cells)} |")

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
