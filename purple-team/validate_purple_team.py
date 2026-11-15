#!/usr/bin/env python3
"""Validate a safe, evidence-driven Purple Team exercise definition."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import yaml


def load(path: str) -> dict:
    with Path(path).open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate(plan: dict, scenario_doc: dict, observation_doc: dict) -> tuple[list[str], dict]:
    errors: list[str] = []
    authorization = plan["authorization"]
    safety = plan["safety"]
    require(authorization.get("approved") is True, "exercise requires explicit approval", errors)
    require(authorization.get("scope") == "non-production",
            "exercise scope must be non-production", errors)
    require(bool(authorization.get("ticket")), "authorization ticket is required", errors)
    require(bool(safety.get("kill_switch_owner")), "kill switch owner is required", errors)
    require(safety.get("synthetic_data_only") is True, "only synthetic data is allowed", errors)
    require(safety.get("sample_findings_only") is True, "only sample findings are allowed", errors)
    required_prohibited = {"destructive_actions", "persistence", "credential_dumping",
                           "denial_of_service", "data_exfiltration"}
    require(required_prohibited.issubset(set(safety.get("prohibited", []))),
            "all destructive/high-risk actions must be prohibited", errors)
    require(plan["cleanup"].get("verify_no_test_resources") is True,
            "cleanup must verify no test resources remain", errors)

    scenarios = scenario_doc.get("scenarios", [])
    require(len(scenarios) >= 5, "at least five scenarios are required", errors)
    scenario_ids = set()
    for scenario in scenarios:
        sid = scenario.get("id", "unknown")
        scenario_ids.add(sid)
        require(str(scenario.get("technique", "")).startswith("T"),
                f"{sid}: MITRE ATT&CK technique is required", errors)
        require(scenario.get("safe_mode") in {"sample", "synthetic"},
                f"{sid}: safe_mode must be sample or synthetic", errors)
        require(bool(scenario.get("data_sources")), f"{sid}: data sources are required", errors)
        require(bool(scenario.get("expected_detection")),
                f"{sid}: expected detection is required", errors)
        require(bool(scenario.get("owner")), f"{sid}: owner is required", errors)
        require(bool(scenario.get("success_criteria")),
                f"{sid}: success criteria are required", errors)
        require(bool(scenario.get("cleanup")), f"{sid}: cleanup is required", errors)

    observations = observation_doc.get("observations", [])
    observed_ids = {item.get("scenario_id") for item in observations}
    require(observed_ids == scenario_ids, "every scenario needs exactly one observation", errors)
    detected = [item for item in observations if item.get("detected") is True]
    coverage = round(100 * len(detected) / len(scenarios), 1) if scenarios else 0
    objective = observation_doc["objectives"]
    require(coverage >= objective["minimum_detection_coverage_percent"],
            f"detection coverage {coverage}% is below objective", errors)
    max_mttd = max((item.get("mttd_minutes", 0) for item in detected), default=0)
    max_mttr = max((item.get("mttr_minutes", 0) for item in detected), default=0)
    require(max_mttd <= objective["maximum_mttd_minutes"],
            f"MTTD {max_mttd} exceeds objective", errors)
    require(max_mttr <= objective["maximum_mttr_minutes"],
            f"MTTR {max_mttr} exceeds objective", errors)
    gaps = [item for item in observations if item.get("detected") is not True]
    for item in gaps:
        sid = item.get("scenario_id", "unknown")
        gap = item.get("gap", {})
        require(bool(gap.get("owner")), f"{sid}: detection gap requires owner", errors)
        require(gap.get("priority") in {"critical", "high", "medium", "low"},
                f"{sid}: detection gap requires priority", errors)
        require(bool(gap.get("remediation_due")), f"{sid}: gap requires due date", errors)
        require(bool(gap.get("action")), f"{sid}: gap requires remediation action", errors)
    return errors, {"scenarios": len(scenarios), "detected": len(detected),
                    "coverage": coverage, "max_mttd": max_mttd,
                    "max_mttr": max_mttr, "gaps": len(gaps)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    parser.add_argument("--scenarios", required=True)
    parser.add_argument("--observations", required=True)
    args = parser.parse_args()
    errors, metrics = validate(load(args.plan), load(args.scenarios), load(args.observations))
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        print("RESULT: PURPLE TEAM PLAN INVALID")
        return 1
    print("PASS authorization, safety controls and non-production scope")
    print(f"PASS {metrics['scenarios']} safe scenarios mapped to ATT&CK")
    print(f"PASS detection coverage {metrics['detected']}/{metrics['scenarios']} = {metrics['coverage']}%")
    print(f"PASS max MTTD {metrics['max_mttd']} min and max MTTR {metrics['max_mttr']} min")
    print(f"PASS {metrics['gaps']} detection gap has owner, priority, due date and action")
    print("RESULT: PURPLE TEAM PLAN VALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())
