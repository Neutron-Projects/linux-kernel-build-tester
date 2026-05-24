#!/usr/bin/env python3
"""
inject-result-context.py  —  Adds workflow-level metadata to a result.json.

Usage:
    python3 scripts/inject-result-context.py \
        <result.json>       \
        <kernel_channel>    \
        <kernel_series>     \
        <kernel_label>      \
        <run_url>
"""
import json, sys

if len(sys.argv) < 6:
    print("Usage: inject-result-context.py <json> <channel> <series> <label> <run_url>")
    sys.exit(1)

path, channel, series, label, run_url = sys.argv[1:]

with open(path) as f:
    d = json.load(f)

d.update({
    "kernel_channel": channel,
    "kernel_series":  series,
    "kernel_label":   label,
    "run_url":        run_url,
})

with open(path, "w") as f:
    json.dump(d, f, indent=2)

print(f"Injected context into {path}  (channel={channel}, arch={d.get('arch','?')})")
