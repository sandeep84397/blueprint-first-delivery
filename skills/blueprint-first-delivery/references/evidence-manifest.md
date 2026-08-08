# Evidence manifest

An evidence manifest is machine-readable delivery evidence. The validator is `scripts/validate_evidence_manifest.py`; route examples live in `references/examples/`.

## Required envelope

Every manifest records `schema_version`, `work_id`, `route`, `state`, `route_facts`, and `baseline`. Direct adds a receipt; Lite adds a Lite card; Full adds a proof matrix, traceability, Agent Brain, and integration record.

## Proof matrix

Each Full claim records requirement ID, contract/invariant ID, criticality, owner, status, task ID, executable oracle, expected result, evidence reference, baseline reference, and integration counterpart.

Valid statuses: `FACT`, `ASSUMPTION`, `PROOF_REQUIRED`, `PROVEN`, `BLOCKED`, `STALE`.

At `ARCHITECTURE_APPROVED` and `PLAN_FROZEN`, every critical row must have an owner, oracle, expected result, baseline, and either observed fact or a named future task. `ASSUMPTION`, `BLOCKED`, or `STALE` cannot approve a critical row. `PROOF_REQUIRED` is allowed only when its executor path is named. At `TASK_PROVEN`, `INTEGRATION_PROVEN`, and `DELIVERY_READY`, every critical row is `PROVEN`.

## Traceability

Every Full proof row maps requirement → contract/invariant → task → oracle → evidence → integration result. The same identifiers must appear in the traceability record. Readiness scoring summarizes evidence; it never creates it.

## Immutable baseline and drift

The baseline records git reference, contract digests, owned paths, file SHA-256 values, and an evidence digest. The validator can compare recorded files with a workspace. If a baseline contract, owned file, or evidence digest changes, mark affected evidence `STALE`, stop the affected gate, and re-approve from the earliest invalid state.

## Agent Brain continuity

Full work always uses source-linked Agent Brain. Lite uses it for handoff or multi-turn work. Record source references such as decision IDs, paths, symbols, or reviewed artifact anchors. Agent Brain may preserve discovery and decisions; it never proves a contract or test result.

## Integration evidence

For Full cross-module work, record the required integration plan, early vertical proof, final gate, owner, and result. Missing early proof is a blocked plan, not a final-milestone task.

## Validation

```sh
python3 scripts/validate_evidence_manifest.py references/examples/direct-task-proven.json
python3 scripts/validate_evidence_manifest.py references/examples/lite-task-proven-handoff.json
python3 scripts/validate_evidence_manifest.py references/examples/full-plan-frozen.json
```
