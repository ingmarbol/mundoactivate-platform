#!/usr/bin/env python3
import argparse
from pathlib import Path
import yaml

def load(path):
    with Path(path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)

def has_cycle(graph):
    visiting, visited = set(), set()
    def visit(node):
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(dep) for dep in graph.get(node, [])):
            return True
        visiting.remove(node)
        visited.add(node)
        return False
    return any(visit(node) for node in graph)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", required=True)
    p.add_argument("--policy", required=True)
    a = p.parse_args()
    catalog, policy = load(a.catalog), load(a.policy)
    errors = []
    components = catalog.get("components", [])
    ids = {c.get("id") for c in components}
    graph = {c["id"]: c.get("dependencies", []) for c in components}
    database_owners = []
    for component in components:
        for field in ["id", "kind", "owner", "bounded_context", "database_owner", "public_api", "runtime_identity", "classification"]:
            if not component.get(field):
                errors.append(f"{component.get('id')}: missing {field}")
        unknown = set(component.get("dependencies", [])) - ids
        if unknown:
            errors.append(f"{component.get('id')}: unknown dependencies {sorted(unknown)}")
        database_owners.append(component.get("database_owner"))
    if has_cycle(graph):
        errors.append("component dependency graph contains a cycle")
    if len(database_owners) != len(set(database_owners)):
        errors.append("shared database ownership detected")
    true_fields = {
        "boundaries": ["owner_required", "bounded_context_required", "circular_dependencies_forbidden", "shared_database_forbidden", "public_contract_required"],
        "security": ["workload_identity_required", "secrets_in_code_forbidden", "encryption_in_transit_required", "least_privilege_required"],
        "resilience": ["timeout_required", "retry_only_for_transient_failures", "circuit_breaker_required", "bulkhead_required", "graceful_degradation_required", "idempotency_required"],
        "delivery": ["independent_deployability_target", "progressive_delivery_required", "rollback_required", "contract_tests_required", "security_scans_required"],
        "observability": ["opentelemetry_required", "service_name_required", "slo_required", "correlation_required"],
        "evolution": ["strangler_route_by_route", "anti_corruption_layer_required", "decommission_evidence_required", "fitness_functions_in_ci"],
        "cost": ["component_cost_owner_required", "cell_max_size_required", "cross_cell_traffic_minimized"],
    }
    for section, fields in true_fields.items():
        for field in fields:
            if policy.get(section, {}).get(field) is not True:
                errors.append(f"{section}.{field} must be true")
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        print("RESULT: SECURE ARCHITECTURE BASELINE INVALID")
        return 1
    print(f"PASS {len(components)} components have owners, bounded contexts and contracts")
    print("PASS dependency graph is acyclic and database ownership is isolated")
    print("PASS workload identity, encryption and least privilege controls")
    print("PASS timeout, circuit breaker, bulkhead, degradation and idempotency")
    print("PASS progressive delivery, observability and evolutionary fitness functions")
    print("RESULT: SECURE ARCHITECTURE BASELINE VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
