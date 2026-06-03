#!/usr/bin/env python3
"""Resolve the current kernel build matrix from kernel.org."""

from __future__ import annotations

import argparse
import json
import os

from kernel_releases import build_matrix, fetch_releases


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kernel-filter", default="all")
    parser.add_argument("--arch-filter", default="all")
    parser.add_argument("--output-env", default=os.environ.get("GITHUB_OUTPUT", ""))
    args = parser.parse_args()

    print("Fetching kernel.org/releases.json …", flush=True)
    data = build_matrix(args.kernel_filter, args.arch_filter, fetch_releases())

    for track in data["tracks"]:
        head = f"  HEAD={track['kernel_head_commit']}" if track.get("kernel_head_commit") else ""
        print(f"  {track['kind']:<8} {track['channel']:<12} → {track['version']}{head}")

    print(
        f"\nMatrix: {len(data['matrix']['include'])} job(s) after filtering "
        f"(kernel={args.kernel_filter}, arch={args.arch_filter})"
    )

    if args.output_env:
        with open(args.output_env, "a", encoding="utf-8") as handle:
            handle.write(f"matrix={json.dumps(data['matrix'])}\n")
            handle.write(f"matrix_count={len(data['matrix']['include'])}\n")
            handle.write(f"mainline_head_commit={data['mainline_head_commit']}\n")
            handle.write(f"latest_stable={data['latest_stable']}\n")
        print(f"Wrote {len(data['matrix']['include'])} matrix entries to GITHUB_OUTPUT")
    else:
        print(json.dumps(data["matrix"], indent=2))


if __name__ == "__main__":
    main()
