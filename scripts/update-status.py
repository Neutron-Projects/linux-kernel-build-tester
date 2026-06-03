#!/usr/bin/env python3
"""
update-status.py — Post-build status aggregator.

Reads result JSON artifacts from the build matrix, updates
state/build-status.json, generates shields.io endpoint badge JSONs,
and rewrites the build table section of README.md.

Usage:
    python3 scripts/update-status.py \
        --results-dir  /tmp/results         \
        --toolchain-tag  22052026           \
        --clang-version  "20.0.0git"        \
        --llvm-commit  "abc123..."          \
        --run-id  12345678                  \
        --run-url  "https://github.com/..."
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from kernel_releases import ARCHES, channel_sort_key, fetch_releases, resolve_tracks

ARCH_ORDER = [arch["label"] for arch in ARCHES]

BADGE_COLORS = {
    "pass":    "brightgreen",
    "fail":    "critical",
    "partial": "yellow",
    "unknown": "lightgrey",
}

STATUS_EMOJI = {
    "pass":    "✅",
    "fail":    "❌",
    "unknown": "⬜",
}


# ─── Argument parsing ─────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--results-dir",    required=True,  help="Directory tree of result.json files")
    p.add_argument("--toolchain-tag",  required=True,  help="Neutron Clang catalogue tag")
    p.add_argument("--clang-version",  default="",     help="Clang version string")
    p.add_argument("--llvm-commit",    default="",     help="LLVM commit URL")
    p.add_argument("--run-id",         default="",     help="GitHub Actions run ID")
    p.add_argument("--run-url",        default="",     help="GitHub Actions run URL")
    return p.parse_args()


# ─── Load results ──────────────────────────────────────────────────────────────

def load_results(results_dir: str) -> dict:
    """Walk results_dir, load every result.json, key by (channel, arch)."""
    results = {}
    for root, _, files in os.walk(results_dir):
        for fname in files:
            if fname != "result.json":
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath) as f:
                    data = json.load(f)
                key = (data["kernel_channel"], data["arch"])
                results[key] = data
                print(f"  loaded {key}  →  {data.get('status','?')}  {data.get('duration_human','')}")
            except Exception as e:
                print(f"  warning: failed to load {fpath}: {e}", file=sys.stderr)
    return results


# ─── Status JSON ──────────────────────────────────────────────────────────────

def load_existing_status() -> dict:
    p = Path("state/build-status.json")
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return {"builds": {}, "toolchain": {}, "history": [], "track_order": [], "track_meta": {}}


def load_live_tracks() -> list[dict]:
    try:
        return resolve_tracks(fetch_releases())['tracks']
    except Exception as exc:
        print(f"warning: failed to resolve live kernel tracks: {exc}", file=sys.stderr)
        return []


def get_track_order(status: dict) -> list[str]:
    order = status.get("track_order", [])
    if order:
        return order
    builds = status.get("builds", {})
    channels = sorted({key.split("/")[0] for key in builds}, key=channel_sort_key)
    return channels


def get_track_meta(status: dict) -> dict:
    return status.get("track_meta", {})


def build_new_status(existing: dict, results: dict, args, tracks: list[dict]) -> dict:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    track_order = [track["channel"] for track in tracks]
    track_meta = {
        track["channel"]: {
            "label": track["label"],
            "series": track["series"],
            "kind": track["kind"],
            "version": track["version"],
            "kernel_head_commit": track.get("kernel_head_commit", ""),
        }
        for track in tracks
    }

    status = {
        "last_updated": now,
        "last_run_id": args.run_id,
        "last_run_url": args.run_url,
        "toolchain": {
            "tag": args.toolchain_tag,
            "clang_version": args.clang_version,
            "llvm_commit": args.llvm_commit,
            "updated": now,
        },
        "builds": dict(existing.get("builds", {})),
        "history": list(existing.get("history", [])),
        "track_order": track_order,
        "track_meta": track_meta,
    }

    for (channel, arch), result in results.items():
        key = f"{channel}/{arch}"
        status["builds"][key] = {
            "status":         result.get("status", "unknown"),
            "kernel_version": result.get("kernel_version", ""),
            "kernel_channel": channel,
            "arch":           arch,
            "duration":       result.get("duration_human", ""),
            "duration_secs":  result.get("duration_seconds", 0),
            "warnings":       result.get("warnings", 0),
            "errors":         result.get("errors", 0),
            "clang_version":  result.get("clang_version", args.clang_version),
            "toolchain_tag":  result.get("toolchain_tag", args.toolchain_tag),
            "kernel_head_commit": result.get("kernel_head_commit", ""),
            "timestamp":      result.get("timestamp_end", now),
            "run_url":        result.get("run_url", args.run_url),
        }

    # Append a history entry (keep last 50)
    run_summary = {
        "toolchain_tag": args.toolchain_tag,
        "clang_version": args.clang_version,
        "run_id":        args.run_id,
        "run_url":       args.run_url,
        "timestamp":     now,
        "results":       {
            f"{track['channel']}/{arch}": results.get((track["channel"], arch), {}).get("status", "unknown")
            for track in tracks
            for arch in ARCH_ORDER
        }
    }
    status["history"] = ([run_summary] + status["history"])[:50]

    return status


def save_status(status: dict):
    Path("state").mkdir(exist_ok=True)
    with open("state/build-status.json", "w") as f:
        json.dump(status, f, indent=2)
    print("Saved state/build-status.json")


# ─── Badge generation ─────────────────────────────────────────────────────────

def channel_overall_status(builds: dict, channel: str) -> str:
    statuses = [
        builds.get(f"{channel}/{arch}", {}).get("status", "unknown")
        for arch in ARCH_ORDER
    ]
    known = [s for s in statuses if s != "unknown"]
    if not known:
        return "unknown"
    if all(s == "pass" for s in known):
        return "pass"
    if all(s == "fail" for s in known):
        return "fail"
    return "partial"


def generate_badge(label: str, message: str, color: str) -> dict:
    return {
        "schemaVersion": 1,
        "label": label,
        "message": message,
        "color": color,
        "style": "flat-square",
        "namedLogo": "linux",
    }


def write_badges(status: dict):
    Path("state/badges").mkdir(parents=True, exist_ok=True)
    builds = status.get("builds", {})
    track_meta = get_track_meta(status)
    track_order = get_track_order(status)

    for channel in track_order:
        label = track_meta.get(channel, {}).get("label", channel)

        overall = channel_overall_status(builds, channel)

        version_str = track_meta.get(channel, {}).get("version", "")
        if not version_str:
            for arch in ARCH_ORDER:
                v = builds.get(f"{channel}/{arch}", {}).get("kernel_version", "")
                if v:
                    version_str = v
                    break

        if overall == "pass":
            msg = f"{version_str} ✓" if version_str else "passing"
        elif overall == "fail":
            msg = f"{version_str} ✗" if version_str else "failing"
        elif overall == "partial":
            msg = "partial"
        else:
            msg = "unknown"

        badge_data = generate_badge(label, msg, BADGE_COLORS[overall])
        badge_path = f"state/badges/{channel}.json"
        with open(badge_path, "w") as f:
            json.dump(badge_data, f, indent=2)

    # Aggregate "all" badge
    all_statuses = [channel_overall_status(builds, channel) for channel in track_order]
    known_all = [s for s in all_statuses if s != "unknown"]
    if not known_all:
        agg = "unknown"
    elif all(s == "pass" for s in known_all):
        agg = "pass"
    elif all(s == "fail" for s in known_all):
        agg = "fail"
    else:
        agg = "partial"

    tc_tag  = status.get("toolchain", {}).get("tag", "")
    clang_v = status.get("toolchain", {}).get("clang_version", "")
    agg_msg = f"{clang_v}" if clang_v else (tc_tag if tc_tag else "unknown")

    with open("state/badges/all.json", "w") as f:
        json.dump(generate_badge("kernel builds", agg_msg, BADGE_COLORS[agg]), f, indent=2)

    # Toolchain badge
    with open("state/badges/toolchain.json", "w") as f:
        json.dump(generate_badge(
            "neutron clang",
            clang_v if clang_v else tc_tag,
            "informational"
        ), f, indent=2)

    print("Wrote badge JSONs to state/badges/")


# ─── README table ─────────────────────────────────────────────────────────────

def format_cell(build: dict | None, run_url: str) -> str:
    if build is None:
        return STATUS_EMOJI["unknown"]

    s = build.get("status", "unknown")
    emoji = STATUS_EMOJI.get(s, STATUS_EMOJI["unknown"])

    if s == "pass":
        dur = build.get("duration", "")
        w   = build.get("warnings", 0)
        w_str = f" ⚠{w}" if w else ""
        inner = f"{emoji} `{dur}`{w_str}" if dur else emoji
    else:
        inner = emoji

    link = build.get("run_url") or run_url
    if link:
        return f"[{inner}]({link})"
    return inner


def generate_table(status: dict) -> str:
    builds   = status.get("builds", {})
    tc       = status.get("toolchain", {})
    run_url  = status.get("last_run_url", "")
    updated  = status.get("last_updated", "")
    track_meta = get_track_meta(status)
    track_order = get_track_order(status)

    lines = []

    # ── Toolchain info bar ──
    tc_tag    = tc.get("tag", "—")
    clang_ver = tc.get("clang_version", "")
    cat_url   = f"https://github.com/Neutron-Toolchains/clang-build-catalogue/releases/tag/{tc_tag}"

    if clang_ver:
        lines.append(f'> **Neutron Clang:** [`{clang_ver}`]({cat_url})&emsp;**Tag:** `{tc_tag}`')
    else:
        lines.append(f'> **Neutron Clang Tag:** [`{tc_tag}`]({cat_url})')

    if updated:
        try:
            dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            ts = dt.strftime("%d %b %Y %H:%M UTC")
        except Exception:
            ts = updated
        url_bit = f"[{ts}]({run_url})" if run_url else ts
        lines.append(f"> **Last run:** {url_bit}")

    lines.append("")

    # ── Table ──
    lines.append("| Kernel | Version | `arm64` | `arm` | `x86_64` |")
    lines.append("|:-------|:--------|:-------:|:-----:|:--------:|")

    for channel in track_order:
        label = track_meta.get(channel, {}).get("label", channel)

        version_str = track_meta.get(channel, {}).get("version", "")
        cells = []
        for arch in ARCH_ORDER:
            key   = f"{channel}/{arch}"
            build = builds.get(key)
            if not version_str and build:
                version_str = build.get("kernel_version", "")
            cells.append(format_cell(build, run_url))

        ver_col = f"`{version_str}`" if version_str else "—"
        row = f"| **{label}** | {ver_col} | {' | '.join(cells)} |"
        lines.append(row)

    lines.append("")
    lines.append("<sub>✅ pass · ❌ fail · ⬜ not run · ⚠N = N compiler warnings · time shown for passing builds</sub>")

    return "\n".join(lines)


def update_readme(table: str):
    readme = Path("README.md")
    content = readme.read_text()

    pattern = r"(<!-- BUILD_TABLE_START -->).*?(<!-- BUILD_TABLE_END -->)"
    replacement = f"<!-- BUILD_TABLE_START -->\n\n{table}\n\n<!-- BUILD_TABLE_END -->"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        print("WARNING: README.md markers not found — table not updated", file=sys.stderr)
        return

    readme.write_text(new_content)
    print("Updated README.md build table")


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    print(f"\n=== update-status.py ===")
    print(f"toolchain tag : {args.toolchain_tag}")
    print(f"clang version : {args.clang_version}")
    print(f"run id        : {args.run_id}")
    print(f"\nLoading results from {args.results_dir}…")

    results = load_results(args.results_dir)
    print(f"Loaded {len(results)} build result(s)\n")

    tracks = load_live_tracks()

    existing = load_existing_status()
    status   = build_new_status(existing, results, args, tracks)

    save_status(status)
    write_badges(status)

    # Update last-toolchain.txt so check-toolchain.yml can compare
    Path("state").mkdir(exist_ok=True)
    Path("state/last-toolchain.txt").write_text(args.toolchain_tag + "\n")
    print(f"Saved state/last-toolchain.txt → {args.toolchain_tag}")

    table = generate_table(status)
    print(f"\nGenerated README table:\n{table}\n")
    update_readme(table)

    print("Done.\n")


if __name__ == "__main__":
    main()
