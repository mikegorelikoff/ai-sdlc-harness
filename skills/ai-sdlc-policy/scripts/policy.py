#!/usr/bin/env python3
"""Resolve layered policy and evaluate explainable waiver-aware decisions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SHARED = Path(__file__).resolve().parents[2] / "_shared"
if not _SHARED.is_dir():
    _SHARED = _SHARED.parent / "ai-sdlc-shared-runtime" / "scripts"
sys.path.insert(0, str(_SHARED))
from ai_sdlc_toon import encode_toon
from ai_sdlc_safe_io import atomic_write_text


LAYER_SCHEMA = "ai-sdlc-policy-layer/v1"
WAIVER_SCHEMA = "ai-sdlc-policy-waiver/v1"
RESOLUTION_SCHEMA = "ai-sdlc-policy-resolution/v1"
DECISION_SCHEMA = "ai-sdlc-policy-decision/v1"
SCOPES = ("base", "organization", "project", "user")
RULE_FIELDS = {"id", "actions", "effect", "when", "required_gates", "protected", "waivable", "description"}
PREDICATE_FIELDS = {"field", "operator", "value"}
WAIVER_FIELDS = {"schema", "id", "rule_id", "actions", "subject", "constraints", "owner", "approved_by", "decision_ref", "reason", "issued_at", "expires_at"}
EFFECT_STRENGTH = {"allow": 0, "require": 1, "deny": 2}


def canonical(value: Any) -> str:
    """Serialize deterministic JSON for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    """Return a deterministic SHA-256 digest."""
    if not isinstance(value, str):
        value = canonical(value)
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def atomic_write(root: Path, path: Path, content: str) -> None:
    """Atomically replace one generated policy output."""
    atomic_write_text(root, path, content)


def timestamp(value: Any, field: str) -> tuple[datetime | None, str | None]:
    """Parse a timezone-aware ISO timestamp."""
    if not isinstance(value, str):
        return None, f"{field} must be an ISO timestamp"
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None, f"{field} must be an ISO timestamp"
    if parsed.tzinfo is None:
        return None, f"{field} must include a timezone"
    return parsed.astimezone(timezone.utc), None


def action_pattern(value: Any) -> bool:
    """Validate exact and suffix-wildcard action patterns."""
    return isinstance(value, str) and bool(re.fullmatch(r"(?:\*|[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)*(?:\.\*)?)", value))


def validate_rule(rule: Any, source: str) -> list[str]:
    """Validate one bounded rule language record."""
    errors: list[str] = []
    if not isinstance(rule, dict) or set(rule) != RULE_FIELDS:
        return [f"{source}: rule fields must match {', '.join(sorted(RULE_FIELDS))}"]
    if not isinstance(rule["id"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9.-]*", rule["id"]):
        errors.append(f"{source}: rule id is invalid")
    actions = rule["actions"]
    if not isinstance(actions, list) or not actions or not all(action_pattern(item) for item in actions) or len(actions) != len(set(actions)):
        errors.append(f"{source}: rule actions must be unique valid patterns")
    if rule["effect"] not in EFFECT_STRENGTH:
        errors.append(f"{source}: rule effect must be allow, require, or deny")
    if not isinstance(rule["protected"], bool) or not isinstance(rule["waivable"], bool):
        errors.append(f"{source}: protected and waivable must be booleans")
    if not isinstance(rule["description"], str) or not rule["description"].strip():
        errors.append(f"{source}: rule description is required")
    gates = rule["required_gates"]
    if not isinstance(gates, list) or not all(isinstance(item, str) and item for item in gates) or len(gates) != len(set(gates)):
        errors.append(f"{source}: required_gates must be a unique string array")
    elif rule["effect"] != "require" and gates:
        errors.append(f"{source}: only require rules may declare gates")
    predicates = rule["when"]
    if not isinstance(predicates, list):
        errors.append(f"{source}: when must be an array")
    else:
        for index, predicate in enumerate(predicates):
            if not isinstance(predicate, dict) or set(predicate) != PREDICATE_FIELDS:
                errors.append(f"{source}: predicate {index} fields are invalid")
                continue
            if not isinstance(predicate["field"], str) or not re.fullmatch(r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*", predicate["field"]):
                errors.append(f"{source}: predicate {index} field is invalid")
            if predicate["operator"] not in {"eq", "in", "exists", "gte", "lte"}:
                errors.append(f"{source}: predicate {index} operator is invalid")
            if predicate["operator"] == "in" and not isinstance(predicate["value"], list):
                errors.append(f"{source}: predicate {index} in value must be an array")
            if predicate["operator"] == "exists" and not isinstance(predicate["value"], bool):
                errors.append(f"{source}: predicate {index} exists value must be boolean")
    return errors


def load_layer(path: Path, expected_scope: str, source_name: str | None = None) -> tuple[dict[str, Any], list[str]]:
    """Load and validate one strict policy layer."""
    try:
        raw = path.read_text(encoding="utf-8")
        value = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read policy layer {path}: {exc}"]
    errors: list[str] = []
    required = {"schema", "id", "version", "scope", "rules"}
    if not isinstance(value, dict) or set(value) != required:
        return {}, [f"{path}: layer fields must match {LAYER_SCHEMA}"]
    if value["schema"] != LAYER_SCHEMA:
        errors.append(f"{path}: schema must be {LAYER_SCHEMA}")
    if not isinstance(value["id"], str) or not value["id"].strip():
        errors.append(f"{path}: layer id is required")
    if not isinstance(value["version"], str) or not re.fullmatch(r"\d+\.\d+\.\d+", value["version"]):
        errors.append(f"{path}: version must use semantic x.y.z form")
    if value["scope"] != expected_scope:
        errors.append(f"{path}: expected {expected_scope} scope, got {value['scope']}")
    if not isinstance(value["rules"], list):
        errors.append(f"{path}: rules must be an array")
    else:
        ids: list[str] = []
        for index, rule in enumerate(value["rules"]):
            errors.extend(validate_rule(rule, f"{path}: rule {index}"))
            if isinstance(rule, dict) and isinstance(rule.get("id"), str):
                ids.append(rule["id"])
        if len(ids) != len(set(ids)):
            errors.append(f"{path}: duplicate rule ids")
    value["_source"] = source_name or path.as_posix()
    value["_source_sha256"] = digest(raw)
    return value, errors


def weakens(current: dict[str, Any], candidate: dict[str, Any]) -> list[str]:
    """Explain every protected-boundary weakening."""
    reasons: list[str] = []
    if current["actions"] != candidate["actions"]:
        reasons.append("protected action scope changed")
    if current["when"] != candidate["when"]:
        reasons.append("protected predicates changed")
    if EFFECT_STRENGTH[candidate["effect"]] < EFFECT_STRENGTH[current["effect"]]:
        reasons.append(f"effect {current['effect']} -> {candidate['effect']}")
    if not set(current["required_gates"]).issubset(candidate["required_gates"]):
        reasons.append("required gates removed")
    if current["protected"] and not candidate["protected"]:
        reasons.append("protected flag cleared")
    if not current["waivable"] and candidate["waivable"]:
        reasons.append("non-waivable rule made waivable")
    return reasons


def resolve_layers(layers: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    """Merge valid layers with protected-rule enforcement and provenance."""
    rules: dict[str, dict[str, Any]] = {}
    provenance: dict[str, str] = {}
    errors: list[str] = []
    layer_records: list[dict[str, str]] = []
    for layer in layers:
        source = f"{layer['scope']}:{layer['id']}@{layer['version']}"
        layer_records.append({"id": layer["id"], "version": layer["version"], "scope": layer["scope"], "source": layer["_source"], "sha256": layer["_source_sha256"]})
        for candidate in layer["rules"]:
            current = rules.get(candidate["id"])
            if current and current["protected"]:
                reasons = weakens(current, candidate)
                if reasons:
                    errors.append(f"{source} weakens protected rule {candidate['id']}: {', '.join(reasons)}")
                    continue
            normalized = {key: candidate[key] for key in sorted(RULE_FIELDS)}
            normalized["actions"] = sorted(normalized["actions"])
            normalized["required_gates"] = sorted(normalized["required_gates"])
            normalized["fingerprint"] = digest(normalized)
            rules[candidate["id"]] = normalized
            provenance[candidate["id"]] = source
    resolution: dict[str, Any] = {
        "schema": RESOLUTION_SCHEMA,
        "precedence": list(SCOPES),
        "layers": layer_records,
        "rules": [dict(rules[key], provenance=provenance[key]) for key in sorted(rules)],
        "protected_rules": sorted(key for key, rule in rules.items() if rule["protected"]),
    }
    resolution["fingerprint"] = digest(resolution)
    return resolution, errors


def get_field(context: dict[str, Any], field: str) -> tuple[Any, bool]:
    """Resolve one dot-addressed context field."""
    current: Any = context
    for part in field.split("."):
        if not isinstance(current, dict) or part not in current:
            return None, False
        current = current[part]
    return current, True


def predicate_matches(predicate: dict[str, Any], context: dict[str, Any]) -> bool:
    """Evaluate one bounded predicate without coercion."""
    actual, exists = get_field(context, predicate["field"])
    operator = predicate["operator"]
    expected = predicate["value"]
    if operator == "exists":
        return exists is expected
    if not exists:
        return False
    if operator == "eq":
        return actual == expected
    if operator == "in":
        return actual in expected
    if operator in {"gte", "lte"}:
        if isinstance(actual, bool) or isinstance(expected, bool) or not isinstance(actual, (int, float, str)) or not isinstance(expected, type(actual)):
            return False
        return actual >= expected if operator == "gte" else actual <= expected
    return False


def action_matches(patterns: list[str], action: str) -> bool:
    """Match an action against exact, global, or suffix wildcard patterns."""
    return any(pattern == "*" or pattern == action or (pattern.endswith(".*") and action.startswith(pattern[:-1])) for pattern in patterns)


def load_waiver(path: Path, source_name: str | None = None) -> tuple[dict[str, Any], list[str]]:
    """Load one strict waiver contract."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read waiver {path}: {exc}"]
    errors: list[str] = []
    if not isinstance(value, dict) or set(value) != WAIVER_FIELDS:
        return {}, [f"{path}: waiver fields must match {WAIVER_SCHEMA}"]
    if value["schema"] != WAIVER_SCHEMA:
        errors.append(f"{path}: schema must be {WAIVER_SCHEMA}")
    for field in ("id", "rule_id", "subject", "owner", "approved_by", "decision_ref", "reason"):
        if not isinstance(value[field], str) or not value[field].strip():
            errors.append(f"{path}: {field} is required")
    if not isinstance(value["actions"], list) or not value["actions"] or not all(action_pattern(item) for item in value["actions"]) or len(value["actions"]) != len(set(value["actions"])):
        errors.append(f"{path}: actions must be unique valid patterns")
    if not isinstance(value["constraints"], dict):
        errors.append(f"{path}: constraints must be an object")
    issued, issued_error = timestamp(value["issued_at"], "issued_at")
    expires, expires_error = timestamp(value["expires_at"], "expires_at")
    if issued_error:
        errors.append(f"{path}: {issued_error}")
    if expires_error:
        errors.append(f"{path}: {expires_error}")
    if issued and expires and expires <= issued:
        errors.append(f"{path}: expires_at must be after issued_at")
    value["_source"] = source_name or path.as_posix()
    return value, errors


def waiver_result(waiver: dict[str, Any], rule: dict[str, Any] | None, action: str, context: dict[str, Any], as_of: datetime, matched: bool) -> tuple[str, str]:
    """Return applied/rejected and an exact reason code."""
    if rule is None:
        return "rejected", "unknown-rule"
    if not matched:
        return "rejected", "rule-not-matched"
    if not rule["waivable"]:
        return "rejected", "rule-not-waivable"
    if not action_matches(waiver["actions"], action):
        return "rejected", "action-mismatch"
    if context.get("subject") != waiver["subject"]:
        return "rejected", "subject-mismatch"
    if any(get_field(context, field) != (expected, True) for field, expected in waiver["constraints"].items()):
        return "rejected", "constraint-mismatch"
    issued, _ = timestamp(waiver["issued_at"], "issued_at")
    expires, _ = timestamp(waiver["expires_at"], "expires_at")
    if issued and as_of < issued:
        return "rejected", "not-yet-valid"
    if expires and as_of > expires:
        return "rejected", "expired"
    return "applied", "accepted"


def evaluate(resolution: dict[str, Any], action: str, context: dict[str, Any], waiver_values: list[dict[str, Any]], as_of: datetime) -> dict[str, Any]:
    """Evaluate one action with deny-first combination and waiver evidence."""
    rules_by_id = {rule["id"]: rule for rule in resolution["rules"]}
    matched_ids = {rule["id"] for rule in resolution["rules"] if action_matches(rule["actions"], action) and all(predicate_matches(predicate, context) for predicate in rule["when"])}
    waiver_rows: list[dict[str, str]] = []
    waived: set[str] = set()
    for waiver in sorted(waiver_values, key=lambda item: item["id"]):
        rule = rules_by_id.get(waiver["rule_id"])
        status, reason = waiver_result(waiver, rule, action, context, as_of, waiver["rule_id"] in matched_ids)
        waiver_rows.append({"id": waiver["id"], "rule_id": waiver["rule_id"], "status": status, "reason": reason, "decision_ref": waiver["decision_ref"], "source": waiver["_source"]})
        if status == "applied":
            waived.add(waiver["rule_id"])
    effective = [rules_by_id[rule_id] for rule_id in sorted(matched_ids - waived)]
    gates = sorted({gate for rule in effective for gate in rule["required_gates"]})
    if any(rule["effect"] == "deny" for rule in effective):
        result = "deny"
    elif any(rule["effect"] == "require" for rule in effective):
        result = "require"
    elif any(rule["effect"] == "allow" for rule in effective):
        result = "allow"
    else:
        result = "allow" if matched_ids else "deny"
    matched_rows = [{"id": rule["id"], "effect": rule["effect"], "required_gates": rule["required_gates"], "provenance": rule["provenance"], "waived": rule["id"] in waived, "description": rule["description"]} for rule in (rules_by_id[item] for item in sorted(matched_ids))]
    reasons = [f"matched-{row['effect']}:{row['id']}" for row in matched_rows if not row["waived"]]
    reasons.extend(f"waived:{row['rule_id']}" for row in waiver_rows if row["status"] == "applied")
    if not effective:
        reasons.append("unknown-action" if not matched_ids else "all-matched-rules-waived")
    decision: dict[str, Any] = {"schema": DECISION_SCHEMA, "action": action, "as_of": as_of.isoformat().replace("+00:00", "Z"), "result": result, "required_gates": gates, "reason_codes": sorted(reasons), "matched_rules": matched_rows, "waivers": waiver_rows, "policy_fingerprint": resolution["fingerprint"], "context_fingerprint": digest(context)}
    decision["fingerprint"] = digest(decision)
    return decision


def markdown(value: dict[str, Any]) -> str:
    """Render an explainable human policy result."""
    if value["schema"] == RESOLUTION_SCHEMA:
        lines = ["# Policy Resolution", "", f"Fingerprint: `{value['fingerprint']}`", "", "| Rule | Effect | Protected | Provenance |", "| --- | --- | --- | --- |"]
        lines.extend(f"| `{rule['id']}` | {rule['effect']} | {str(rule['protected']).lower()} | `{rule['provenance']}` |" for rule in value["rules"])
        return "\n".join(lines) + "\n"
    lines = ["# Policy Decision", "", f"Action: `{value['action']}`", f"Result: **{value['result']}**", f"Policy: `{value['policy_fingerprint']}`", "", "## Required gates", ""]
    lines.extend(f"- `{gate}`" for gate in value["required_gates"])
    if not value["required_gates"]:
        lines.append("- None")
    lines.extend(["", "## Reasons", ""])
    lines.extend(f"- `{reason}`" for reason in value["reason_codes"])
    return "\n".join(lines) + "\n"


def main() -> int:
    """Resolve policy layers or evaluate one action."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--resolve", action="store_true")
    actions.add_argument("--evaluate")
    actions.add_argument("--explain")
    parser.add_argument("--profile", choices=("standard", "high-assurance", "regulated"), default="standard")
    parser.add_argument("--base", type=Path)
    parser.add_argument("--organization", type=Path)
    parser.add_argument("--project", type=Path)
    parser.add_argument("--user", type=Path)
    parser.add_argument("--context", type=Path)
    parser.add_argument("--waiver", type=Path, action="append", default=[])
    parser.add_argument("--as-of", default=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--format", choices=("markdown", "json", "toon"), default="toon")
    parser.add_argument("--quick-flow", action="store_true")
    parser.add_argument("--full-flow", action="store_true")
    parser.add_argument("--feature", default="<feature-name>")
    parser.add_argument("--state-check", action="store_true")
    parser.add_argument("--begin-state", action="store_true")
    parser.add_argument("--complete-state", action="store_true")
    parser.add_argument("--decision-ref")
    parser.add_argument("--assumption")
    parser.add_argument("--state-workspace", choices=("refinement", "implementation"))
    args = parser.parse_args()
    if args.begin_state or args.complete_state:
        print("ERROR: policy evaluation cannot mutate feature lifecycle state")
        return 1
    repository = args.repository.resolve()
    if not repository.is_dir():
        print(f"ERROR: repository does not exist: {repository}")
        return 1
    profile_root = Path(__file__).resolve().parents[1] / "references/profiles"
    paths: list[tuple[Path, str, str]] = [(args.base.resolve() if args.base else profile_root / "default.json", "base", args.base.as_posix() if args.base else "profile:default")]
    if args.profile != "standard":
        paths.append((profile_root / f"{args.profile}.json", "organization", f"profile:{args.profile}"))
    for path, scope in ((args.organization, "organization"), (args.project, "project"), (args.user, "user")):
        if path:
            resolved = path.resolve()
            try:
                source_name = resolved.relative_to(repository).as_posix()
            except ValueError:
                source_name = resolved.as_posix()
            paths.append((resolved, scope, source_name))
    layers: list[dict[str, Any]] = []
    errors: list[str] = []
    for path, scope, source_name in paths:
        layer, layer_errors = load_layer(path, scope, source_name)
        layers.append(layer)
        errors.extend(layer_errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    resolution, errors = resolve_layers(layers)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    action = args.evaluate or args.explain
    if action:
        if not action_pattern(action) or action.endswith(".*") or action == "*":
            print("ERROR: evaluation action must be one exact action")
            return 1
        if args.context is None:
            print("ERROR: --context is required for evaluation")
            return 1
        try:
            context = json.loads(args.context.resolve().read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR: cannot read context: {exc}")
            return 1
        if not isinstance(context, dict):
            print("ERROR: context must be a JSON object")
            return 1
        as_of, time_error = timestamp(args.as_of, "as_of")
        if time_error or as_of is None:
            print(f"ERROR: {time_error}")
            return 1
        waiver_values: list[dict[str, Any]] = []
        for path in args.waiver:
            resolved = path.resolve()
            try:
                source_name = resolved.relative_to(repository).as_posix()
            except ValueError:
                source_name = resolved.as_posix()
            waiver, waiver_errors = load_waiver(resolved, source_name)
            waiver_values.append(waiver)
            errors.extend(waiver_errors)
        waiver_ids = [waiver.get("id") for waiver in waiver_values if isinstance(waiver, dict)]
        if len(waiver_ids) != len(set(waiver_ids)):
            errors.append("duplicate waiver ids")
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        value = evaluate(resolution, action, context, waiver_values, as_of)
        if args.write:
            decision_path = repository / f"_ai_sdlc/policy-decisions/{value['fingerprint']}.json"
            atomic_write(repository, decision_path, json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
            atomic_write(repository, decision_path.with_suffix(".toon"), encode_toon(value))
    else:
        value = resolution
        if args.write:
            atomic_write(repository, repository / "_ai_sdlc/policy-resolution.json", json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
            atomic_write(repository, repository / "_ai_sdlc/policy-resolution.toon", encode_toon(value))
    if args.format == "json":
        print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False))
    elif args.format == "toon":
        print(encode_toon(value), end="")
    else:
        print(markdown(value), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
