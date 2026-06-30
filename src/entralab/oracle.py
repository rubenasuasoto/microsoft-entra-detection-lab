from __future__ import annotations

import json
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .paths import FIXTURES_PATH

Event = dict[str, Any]
Observation = tuple[bool, list[str], int]


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _event_time(event: Event) -> datetime:
    timestamp = event.get("createdDateTime") or event.get("activityDateTime")
    return _parse_time(str(timestamp))


def _events(case: dict[str, Any], source: str) -> list[Event]:
    return sorted(
        [event for event in case["events"] if event["source"] == source],
        key=_event_time,
    )


def _status_code(event: Event) -> int:
    return int(event.get("status", {}).get("errorCode", 0))


def _failure(event: Event) -> bool:
    return _status_code(event) != 0


def _success(event: Event) -> bool:
    return _status_code(event) == 0


def _grouped_window(
    events: list[Event],
    key: Callable[[Event], tuple[object, ...]],
    minutes: int,
    qualifies: Callable[[list[Event]], bool],
) -> list[Event]:
    for index, first in enumerate(events):
        end = _event_time(first) + timedelta(minutes=minutes)
        grouped = [
            event
            for event in events[index:]
            if _event_time(event) <= end and key(event) == key(first)
        ]
        if qualifies(grouped):
            return grouped
    return []


def _entra_001(case: dict[str, Any]) -> Observation:
    events = [event for event in _events(case, "signIn") if _failure(event)]
    matched = _grouped_window(
        events,
        lambda event: (event["ipAddress"], event["appDisplayName"]),
        5,
        lambda group: len(group) >= 5,
    )
    return bool(matched), ["status.errorCode", "ipAddress", "appDisplayName"], len(matched)


def _entra_002(case: dict[str, Any]) -> Observation:
    events = [event for event in _events(case, "signIn") if _failure(event)]
    matched = _grouped_window(
        events,
        lambda event: (event["ipAddress"], event["appDisplayName"]),
        10,
        lambda group: len({event["userPrincipalName"] for event in group}) >= 5,
    )
    return bool(matched), ["status.errorCode", "userPrincipalName", "ipAddress"], len(matched)


def _mfa_denied(event: Event) -> bool:
    reason = str(event.get("status", {}).get("failureReason", "")).lower()
    return _failure(event) and "mfa" in reason and "denied" in reason


def _entra_003(case: dict[str, Any]) -> Observation:
    events = _events(case, "signIn")
    denied = [event for event in events if _mfa_denied(event)]
    for success in [event for event in events if _success(event)]:
        start = _event_time(success) - timedelta(minutes=15)
        matched = [
            event
            for event in denied
            if start <= _event_time(event) <= _event_time(success)
            and event["userPrincipalName"] == success["userPrincipalName"]
            and event["ipAddress"] == success["ipAddress"]
        ]
        if len(matched) >= 2:
            return (
                True,
                ["status.failureReason", "userPrincipalName", "ipAddress"],
                len(matched) + 1,
            )
    return False, ["status.failureReason", "userPrincipalName", "ipAddress"], 0


def _entra_004(case: dict[str, Any]) -> Observation:
    matches = [
        event
        for event in _events(case, "signIn")
        if _success(event)
        and event.get("riskLevelDuringSignIn") in {"medium", "high"}
        and event.get("riskState") in {"atRisk", "confirmedCompromised"}
        and event.get("conditionalAccessStatus") != "failure"
    ]
    return (
        bool(matches),
        ["riskLevelDuringSignIn", "riskState", "conditionalAccessStatus"],
        len(matches),
    )


def _activity(event: Event) -> str:
    return str(event.get("activityDisplayName", "")).lower()


def _entra_005(case: dict[str, Any]) -> Observation:
    matches = [
        event
        for event in _events(case, "directoryAudit")
        if event.get("category") == "RoleManagement"
        and event.get("result") == "success"
        and "member to role" in _activity(event)
        and any(
            str(resource.get("displayName", "")).lower()
            in {"global administrator", "privileged role administrator"}
            for resource in event.get("targetResources", [])
        )
    ]
    return bool(matches), ["category", "activityDisplayName", "targetResources"], len(matches)


def _entra_006(case: dict[str, Any]) -> Observation:
    matches = [
        event
        for event in _events(case, "directoryAudit")
        if event.get("category") == "ApplicationManagement"
        and event.get("result") == "success"
        and (
            "credential" in _activity(event)
            or any(
                str(prop.get("displayName", "")).lower()
                in {"keycredentials", "passwordcredentials"}
                for resource in event.get("targetResources", [])
                for prop in resource.get("modifiedProperties", [])
            )
        )
    ]
    return bool(matches), ["category", "activityDisplayName", "modifiedProperties"], len(matches)


EVALUATORS: dict[str, Callable[[dict[str, Any]], Observation]] = {
    "ENTRA-001": _entra_001,
    "ENTRA-002": _entra_002,
    "ENTRA-003": _entra_003,
    "ENTRA-004": _entra_004,
    "ENTRA-005": _entra_005,
    "ENTRA-006": _entra_006,
}


def load_cases(path: Path = FIXTURES_PATH) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))["cases"]


def evaluate_cases(path: Path = FIXTURES_PATH) -> list[dict[str, Any]]:
    results = []
    for case in load_cases(path):
        observed, fields, event_count = EVALUATORS[case["rule_id"]](case)
        expected = bool(case["expected_alert"])
        results.append(
            {
                "case_id": case["case_id"],
                "rule_id": case["rule_id"],
                "category": case["category"],
                "expected": expected,
                "observed": observed,
                "status": "pass" if expected == observed else "fail",
                "disposition": case.get("disposition", "keep"),
                "matched_fields": fields,
                "matched_event_count": event_count,
                "note": case["note"],
            }
        )
    return results
