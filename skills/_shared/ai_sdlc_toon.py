#!/usr/bin/env python3
"""Deterministic TOON 3.3 encoding for the JSON data model.

The harness keeps JSON where JSON Schema or append-only JSONL interoperability
is required. Agent-facing projections use this encoder so they retain the full
record instead of emitting capability-specific summaries.
"""

from __future__ import annotations

import json
import math
import re
from typing import Any


_BARE_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]*$")
_NUMBER = re.compile(r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?$")
_RESERVED = {"true", "false", "null"}


def _primitive(value: Any) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def _key(value: Any) -> str:
    text = str(value)
    return text if _BARE_KEY.fullmatch(text) else json.dumps(text, ensure_ascii=False)


def _string(value: str) -> str:
    needs_quotes = (
        not value
        or value != value.strip()
        or value.lower() in _RESERVED
        or bool(_NUMBER.fullmatch(value))
        or value.startswith("-")
        or any(character in value for character in ':,"[]{}\n\r\t\\')
    )
    return json.dumps(value, ensure_ascii=False) if needs_quotes else value


def _scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("TOON cannot encode non-finite numbers")
        if value == 0:
            return "0"
        return repr(value)
    if isinstance(value, str):
        return _string(value)
    raise TypeError(f"unsupported TOON scalar: {type(value).__name__}")


def _table(value: list[Any]) -> list[str] | None:
    if not value or not all(isinstance(item, dict) and item for item in value):
        return None
    fields = sorted(value[0], key=str)
    if any(set(item) != set(fields) for item in value):
        return None
    if any(not _primitive(item[field]) for item in value for field in fields):
        return None
    return fields


def _emit_mapping(value: dict[Any, Any], depth: int) -> list[str]:
    lines: list[str] = []
    prefix = "  " * depth
    for raw_key in sorted(value, key=str):
        item = value[raw_key]
        key = _key(raw_key)
        if _primitive(item):
            lines.append(f"{prefix}{key}: {_scalar(item)}")
        elif isinstance(item, dict):
            if item:
                lines.append(f"{prefix}{key}:")
                lines.extend(_emit_mapping(item, depth + 1))
            else:
                lines.append(f"{prefix}{key}: {{}}")
        elif isinstance(item, list):
            lines.extend(_emit_named_list(key, item, depth))
        else:
            raise TypeError(f"unsupported TOON value: {type(item).__name__}")
    return lines


def _emit_named_list(key: str, value: list[Any], depth: int) -> list[str]:
    prefix = "  " * depth
    if not value:
        return [f"{prefix}{key}[0]:"]
    if all(_primitive(item) for item in value):
        return [f"{prefix}{key}[{len(value)}]: " + ",".join(_scalar(item) for item in value)]
    fields = _table(value)
    if fields is not None:
        header = ",".join(_key(field) for field in fields)
        rows = [f"{prefix}{key}[{len(value)}]{{{header}}}:"]
        rows.extend(
            f"{'  ' * (depth + 1)}" + ",".join(_scalar(item[field]) for field in fields)
            for item in value
        )
        return rows
    lines = [f"{prefix}{key}[{len(value)}]:"]
    lines.extend(_emit_list_items(value, depth + 1))
    return lines


def _emit_list_items(value: list[Any], depth: int) -> list[str]:
    lines: list[str] = []
    prefix = "  " * depth
    for item in value:
        if _primitive(item):
            lines.append(f"{prefix}- {_scalar(item)}")
        elif isinstance(item, dict):
            if not item:
                lines.append(f"{prefix}- {{}}")
                continue
            first, *rest = sorted(item, key=str)
            first_value = item[first]
            first_key = _key(first)
            if _primitive(first_value):
                lines.append(f"{prefix}- {first_key}: {_scalar(first_value)}")
            elif isinstance(first_value, dict):
                if first_value:
                    lines.append(f"{prefix}- {first_key}:")
                    lines.extend(_emit_mapping(first_value, depth + 2))
                else:
                    lines.append(f"{prefix}- {first_key}: {{}}")
            elif isinstance(first_value, list):
                nested = _emit_named_list(first_key, first_value, depth + 1)
                lines.append(f"{prefix}- {nested[0].lstrip()}")
                lines.extend(nested[1:])
            else:
                raise TypeError(f"unsupported TOON value: {type(first_value).__name__}")
            if rest:
                lines.extend(_emit_mapping({key: item[key] for key in rest}, depth + 1))
        elif isinstance(item, list):
            if not item:
                lines.append(f"{prefix}- [0]:")
            elif all(_primitive(child) for child in item):
                lines.append(f"{prefix}- [{len(item)}]: " + ",".join(_scalar(child) for child in item))
            else:
                lines.append(f"{prefix}- [{len(item)}]:")
                lines.extend(_emit_list_items(item, depth + 1))
        else:
            raise TypeError(f"unsupported TOON value: {type(item).__name__}")
    return lines


def encode_toon(value: Any) -> str:
    """Encode a JSON-compatible value as canonical, newline-terminated TOON."""
    if isinstance(value, dict):
        lines = _emit_mapping(value, 0)
    elif isinstance(value, list):
        if all(_primitive(item) for item in value):
            lines = [f"[{len(value)}]: " + ",".join(_scalar(item) for item in value)]
        else:
            lines = [f"[{len(value)}]:", *_emit_list_items(value, 1)]
    elif _primitive(value):
        lines = [_scalar(value)]
    else:
        raise TypeError(f"unsupported TOON root: {type(value).__name__}")
    return "\n".join(lines) + "\n"
