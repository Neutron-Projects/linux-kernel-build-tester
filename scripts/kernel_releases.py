#!/usr/bin/env python3
"""Shared kernel.org release helpers for the build tester."""

from __future__ import annotations

import json
import re
import subprocess
import urllib.request
from dataclasses import dataclass, asdict

RELEASES_URL = "https://www.kernel.org/releases.json"
MAINLINE_GIT_URL = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git"

ARCHES = [
    {"arch": "ARM64", "label": "arm64"},
    {"arch": "ARM", "label": "arm"},
    {"arch": "X86", "label": "x86_64"},
]

CHANNEL_ALIASES = {
    "latest": "stable",
    "latest-release": "stable",
    "stable": "stable",
    "mainline": "mainline",
}


@dataclass(frozen=True)
class KernelTrack:
    channel: str
    series: str
    label: str
    kind: str
    version: str
    kernel_head_commit: str = ""

    def to_matrix_entry(self, arch: dict[str, str]) -> dict[str, str]:
        return {
            "kernel_channel": self.channel,
            "kernel_series": self.series,
            "kernel_version": self.version,
            "kernel_label": self.label,
            "kernel_head_commit": self.kernel_head_commit,
            "arch": arch["arch"],
            "arch_label": arch["label"],
            "job_name": f"{self.label} / {arch['label']}",
        }

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def fetch_releases(timeout: int = 30) -> dict:
    req = urllib.request.Request(RELEASES_URL, headers={"User-Agent": "linux-kernel-build-tester/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read())


def resolve_mainline_head_commit(timeout: int = 30) -> str:
    try:
        result = subprocess.run(
            ["git", "ls-remote", MAINLINE_GIT_URL, "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return ""

    first_line = result.stdout.strip().splitlines()
    if not first_line:
        return ""
    return first_line[0].split()[0]


def _version_key(version: str) -> tuple[int, ...]:
    parts = re.findall(r"\d+", version)
    return tuple(int(part) for part in parts)


def _version_matches_series(version: str, series: str) -> bool:
    return version == series or version.startswith(f"{series}.")


def _latest_track_version(releases: dict, moniker: str, allow_rc: bool = False) -> str:
    for item in releases.get("releases", []):
        if item.get("moniker") != moniker or item.get("iseol", False):
            continue
        version = item.get("version", "")
        if allow_rc or "-rc" not in version:
            return version
    for item in releases.get("releases", []):
        if item.get("moniker") != moniker:
            continue
        version = item.get("version", "")
        if allow_rc or "-rc" not in version:
            return version
    return ""


def _latest_longterm_series(releases: dict) -> list[str]:
    series_versions: dict[str, str] = {}
    for item in releases.get("releases", []):
        if item.get("moniker") != "longterm" or item.get("iseol", False):
            continue
        version = item.get("version", "")
        match = re.match(r"^(\d+\.\d+)", version)
        if not match:
            continue
        series = match.group(1)
        current = series_versions.get(series)
        if current is None or _version_key(version) > _version_key(current):
            series_versions[series] = version

    return sorted(series_versions, key=_version_key, reverse=True)


def resolve_tracks(releases: dict, include_mainline_head_commit: bool = True) -> dict:
    latest_stable = releases.get("latest_stable", {}).get("version", "")
    stable_version = _latest_track_version(releases, "stable") or latest_stable
    mainline_version = _latest_track_version(releases, "mainline", allow_rc=True)

    tracks = []
    if mainline_version:
        tracks.append(
            KernelTrack(
                channel="mainline",
                series="mainline",
                label="Mainline",
                kind="mainline",
                version=mainline_version,
                kernel_head_commit=resolve_mainline_head_commit() if include_mainline_head_commit else "",
            )
        )

    if stable_version:
        tracks.append(
            KernelTrack(
                channel="stable",
                series="stable",
                label="Stable",
                kind="stable",
                version=stable_version,
            )
        )

    for series in _latest_longterm_series(releases):
        version = next(
            (
                item.get("version", "")
                for item in releases.get("releases", [])
                if item.get("moniker") == "longterm" and _version_matches_series(item.get("version", ""), series)
            ),
            "",
        )
        if not version:
            continue
        tracks.append(
            KernelTrack(
                channel=f"lts-{series}",
                series=series,
                label=f"{series} LTS",
                kind="lts",
                version=version,
            )
        )

    return {
        "tracks": [track.to_dict() for track in tracks],
        "latest_stable": latest_stable or stable_version,
        "mainline_head_commit": tracks[0].kernel_head_commit if tracks and tracks[0].channel == "mainline" else "",
    }


def resolve_version_for_channel(channel_or_version: str, releases: dict | None = None) -> str:
    channel = normalize_channel(channel_or_version)
    if re.fullmatch(r"\d+\.\d+(?:\.\d+)?(?:-rc\d+)?", channel_or_version):
        return channel_or_version

    if releases is None:
        releases = fetch_releases()

    if channel == "mainline":
        return _latest_track_version(releases, "mainline", allow_rc=True)
    if channel == "stable":
        return _latest_track_version(releases, "stable") or releases.get("latest_stable", {}).get("version", "")
    if channel.startswith("lts-"):
        series = channel.removeprefix("lts-")
        for item in releases.get("releases", []):
            if item.get("moniker") != "longterm":
                continue
            version = item.get("version", "")
            if _version_matches_series(version, series) and not item.get("iseol", False):
                return version
        for item in releases.get("releases", []):
            if item.get("moniker") != "longterm":
                continue
            version = item.get("version", "")
            if _version_matches_series(version, series):
                return version
    raise ValueError(f"Could not resolve kernel channel '{channel_or_version}'")


def normalize_channel(channel: str) -> str:
    key = channel.strip().lower()
    return CHANNEL_ALIASES.get(key, key)


def build_matrix(kernel_filter: str = "all", arch_filter: str = "all", releases: dict | None = None) -> dict:
    if releases is None:
        releases = fetch_releases()

    track_info = resolve_tracks(releases)
    tracks = track_info["tracks"]

    if kernel_filter and kernel_filter not in {"", "all"}:
        normalized_filter = normalize_channel(kernel_filter)
        tracks = [
            track for track in tracks
            if track["channel"] == normalized_filter
            or track["series"] == normalized_filter
            or track["label"].lower() == kernel_filter.lower()
            or track["kind"] == normalized_filter
        ]

    arches = list(ARCHES)
    if arch_filter and arch_filter not in {"", "all"}:
        normalized_arch = arch_filter.strip().lower()
        arches = [
            arch for arch in arches
            if arch["label"] == normalized_arch or arch["arch"].lower() == normalized_arch
        ]

    matrix = {"include": []}
    for track in tracks:
        for arch in arches:
            matrix["include"].append({**track, **KernelTrack(**track).to_matrix_entry(arch)})

    return {
        "matrix": matrix,
        "tracks": tracks,
        "latest_stable": track_info["latest_stable"],
        "mainline_head_commit": track_info["mainline_head_commit"],
    }


def channel_sort_key(channel: str) -> tuple[int, ...]:
    normalized = normalize_channel(channel)
    if normalized == "mainline":
        return (10_000,)
    if normalized == "stable":
        return (9_000,)
    if normalized.startswith("lts-"):
        series = normalized.removeprefix("lts-")
        return (int(series.split(".")[0]), int(series.split(".")[1]))
    return tuple(-ord(ch) for ch in normalized)


if __name__ == "__main__":
    import argparse
    import os
    import sys

    parser = argparse.ArgumentParser(description="Resolve kernel.org releases.")
    parser.add_argument("command", choices=["matrix", "resolve-version", "tracks"])
    parser.add_argument("value", nargs="?")
    parser.add_argument("--kernel-filter", default="all")
    parser.add_argument("--arch-filter", default="all")
    args = parser.parse_args()

    if args.command == "resolve-version":
        if not args.value:
            raise SystemExit("resolve-version requires a channel or version value")
        print(resolve_version_for_channel(args.value))
    elif args.command == "tracks":
        data = resolve_tracks(fetch_releases())
        print(json.dumps(data, indent=2))
    else:
        data = build_matrix(args.kernel_filter, args.arch_filter)
        print(json.dumps(data["matrix"], indent=2))
