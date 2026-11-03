#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Compose AGENTS.md from complete sections and exact partial patches."""

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import tomllib


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ADDRESS = "마스터"
NAME = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
SETTING = re.compile(r"\{settings\.([^{}]*)\}")


class BuildError(Exception):
    """An invalid source, profile, or patch prevents generation."""


@dataclass(frozen=True)
class Patch:
    start: int
    end: int
    after: str
    origin: str


def table(value: object, required: set[str], optional: set[str], origin: str) -> dict:
    if not isinstance(value, dict):
        raise BuildError(f"{origin}: expected a table")
    missing = required - value.keys()
    unknown = value.keys() - required - optional
    if missing:
        raise BuildError(f"{origin}: missing fields: {', '.join(sorted(missing))}")
    if unknown:
        raise BuildError(f"{origin}: unknown fields: {', '.join(sorted(unknown))}")
    return value


def read_toml(path: Path) -> dict:
    try:
        with path.open("rb") as source:
            return tomllib.load(source)
    except tomllib.TOMLDecodeError as error:
        raise BuildError(f"{path}: {error}") from error


def names(value: object, origin: str, *, empty: bool = True) -> list[str]:
    if not isinstance(value, list) or (not value and not empty):
        raise BuildError(f"{origin}: expected {'a nonempty' if not empty else 'an'} array of names")
    for name in value:
        if not isinstance(name, str) or not NAME.fullmatch(name):
            raise BuildError(f"{origin}: invalid name {name!r}; use letters, digits, '_' and '-', starting with a letter")
    if len(value) != len(set(value)):
        raise BuildError(f"{origin}: duplicate names")
    return value


def validate_section(name: str, text: str, origin: str) -> None:
    opening, closing = f"<{name}>", f"</{name}>"
    lines = text.splitlines()
    if len(lines) < 3 or lines[0] != opening or lines[-1] != closing:
        raise BuildError(f"{origin}: expected one complete {opening} section")
    if not any(line.strip() for line in lines[1:-1]):
        raise BuildError(f"{origin}: a section cannot be empty")
    if any(line in (opening, closing) for line in lines[1:-1]):
        raise BuildError(f"{origin}: duplicate section boundary")


def read_sections() -> dict[str, str]:
    path = ROOT / "base.toml"
    base = table(read_toml(path), {"sections"}, set(), str(path))
    sections = {}
    for name in names(base["sections"], f"{path}: sections", empty=False):
        path = ROOT / "sections" / f"{name}.md"
        text = path.read_text(encoding="utf-8").rstrip("\n") + "\n"
        validate_section(name, text, str(path))
        sections[name] = text
    return sections


def validate_address(value: object, origin: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value or value.splitlines() != [value]:
        raise BuildError(f"{origin}: address must be a nonempty single-line string")
    return value


def read_profile(name: str) -> tuple[list[str], str]:
    names([name], "--profile", empty=False)
    path = ROOT / "profiles" / f"{name}.toml"
    profile = table(read_toml(path), {"variants"}, {"settings"}, str(path))
    variants = names(profile["variants"], f"{path}: variants")
    settings = table(profile.get("settings", {}), set(), {"address"}, f"{path}: settings")
    address = validate_address(settings.get("address", DEFAULT_ADDRESS), f"{path}: settings.address")
    return variants, address


def apply_variants(sections: dict[str, str], variants: list[str]) -> dict[str, str]:
    plan: dict[str, list[Patch]] = {name: [] for name in sections}
    for variant in variants:
        path = ROOT / "variants" / f"{variant}.toml"
        data = table(read_toml(path), {"patches"}, set(), str(path))
        if not isinstance(data["patches"], list) or not data["patches"]:
            raise BuildError(f"{path}: patches must be a nonempty array of tables")
        for index, value in enumerate(data["patches"], start=1):
            origin = f"{path}: patch {index}"
            patch = table(value, {"section", "before", "after"}, set(), origin)
            name, before, after = patch["section"], patch["before"], patch["after"]
            if not isinstance(name, str) or name not in sections:
                raise BuildError(f"{origin}: unknown section {name!r}")
            if not isinstance(before, str) or not before or not isinstance(after, str):
                raise BuildError(f"{origin}: before must be a nonempty string and after must be a string")
            before = before.replace("\r\n", "\n").replace("\r", "\n")
            after = after.replace("\r\n", "\n").replace("\r", "\n")
            original = sections[name]
            start = original.find(before)
            if start == -1:
                raise BuildError(f"{origin}: before has no match in {name}")
            if original.find(before, start + 1) != -1:
                raise BuildError(f"{origin}: before matches more than once in {name}; include enough context to identify one location")
            end = start + len(before)
            body_start = len(f"<{name}>\n")
            body_end = original.rfind(f"</{name}>")
            if start < body_start or end > body_end:
                raise BuildError(f"{origin}: patches must stay inside {name}; section boundaries cannot be changed")
            plan[name].append(Patch(start, end, after, origin))

    result = {}
    for name, original in sections.items():
        patches = sorted(plan[name], key=lambda patch: patch.start)
        for left, right in zip(patches, patches[1:]):
            if right.start < left.end:
                raise BuildError(f"overlapping patches in {name}: {left.origin} and {right.origin}")
        text = original
        for patch in reversed(patches):
            text = text[:patch.start] + patch.after + text[patch.end:]
        validate_section(name, text, f"composed {name}")
        result[name] = text
    return result


def render(sections: dict[str, str], address: str) -> str:
    text = "\n\n".join(section.rstrip("\n") for section in sections.values()) + "\n"
    for match in SETTING.finditer(text):
        if match.group(1) != "address":
            raise BuildError(f"unknown setting placeholder {match.group(0)!r}")
    if "{settings." in SETTING.sub("", text):
        raise BuildError("malformed settings placeholder")
    return SETTING.sub(lambda match: address, text)


def write_output(path: Path, text: str) -> None:
    destination = path.expanduser()
    resolved = destination.resolve()
    source_directories = (ROOT / "sections", ROOT / "variants", ROOT / "profiles", ROOT / "scripts")
    if resolved == ROOT / "base.toml" or any(resolved.is_relative_to(directory) for directory in source_directories):
        raise BuildError("output cannot overwrite source files or configuration")
    mode = stat.S_IMODE(destination.stat().st_mode) if destination.exists() else None
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=destination.parent,
            prefix=f".{destination.name}.", suffix=".tmp", delete=False,
        ) as output:
            temporary = Path(output.name)
            output.write(text)
        if mode is not None:
            temporary.chmod(mode)
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, help="profile name from profiles/<name>.toml")
    parser.add_argument("--address", help=f"override the profile address; built-in default: {DEFAULT_ADDRESS}")
    parser.add_argument("--output", type=Path, help="destination file; omit to write to stdout")
    args = parser.parse_args()
    try:
        variants, address = read_profile(args.profile)
        if args.address is not None:
            address = validate_address(args.address, "--address")
        sections = apply_variants(read_sections(), variants)
        text = render(sections, address)
        if args.output is None:
            sys.stdout.buffer.write(text.encode("utf-8"))
        else:
            write_output(args.output, text)
    except (BuildError, OSError, UnicodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
