# Readiness rubric

Principal-engineer-style adversarial reviewer scores the blueprints before implementation. Author and reviewer must be different people/agents. Reviewer actively challenges contracts, hidden dependencies, ownership, failure paths, security, and claimed evidence.

Outcome-backward planning is a separate pre-score gate. It verifies observable outcome evidence, backward prerequisites, forward feasibility, reconciliation, and module freeze before this rubric is applied.

If it is not `PASS`, readiness is **unscorable**. Do not add, remove, or reweight rubric rows to represent an outcome-backward failure.

| Area | Maximum | Awarded | Deductions |
| --- | ---: | ---: | --- |
| Requirement clarity | 15 |  | Deduct 5 for missing problem/outcome; deduct 5 for ambiguous in/out scope or constraints; deduct 5 for missing affected modules. |
| Blueprint completeness | 15 |  | Deduct 3 each for missing architecture evidence, module responsibility/data flow, state ownership, failure/rollback path, or separate integration blueprint. |
| Interfaces and contracts | 15 |  | Deduct 3 each for missing input, output, error, compatibility, or security/privacy boundary. |
| Dependency isolation | 10 |  | Deduct 5 for any unclassified dependency; deduct 5 for any false-independence, shared-state, or overlapping-ownership parallel claim. |
| Acceptance criteria | 10 |  | Deduct 2 for each missing, non-testable, or unmapped criterion, up to 10. |
| Testability | 15 |  | Deduct 5 for missing focused test strategy; deduct 5 for missing contract/integration/e2e/regression plan; deduct 5 for missing deterministic command plus oracle. |
| Edge-case handling | 10 |  | Deduct 2 each when failure/retry, rollback/recovery, security/authorization, concurrency/state conflict, or backward-compatibility edge handling is absent. |
| Independent review | 10 |  | Award 0 if author and reviewer are not distinct; otherwise deduct 5 if findings lack dispositions and deduct 5 if score/evidence is not recorded. |
| **Total** | **100** |  | **Sum awarded points; record every deduction and repair.** |

Architecture evidence is a scoring prerequisite. An existing-codebase blueprint with no architecture-evidence block is **unscorable**; do not assign a readiness score. If missing evidence could change module boundaries or contracts, record an unresolved critical risk and veto implementation. The 3-point deduction above applies only when a present evidence block is incomplete. A greenfield blueprint must state the literal status `greenfield` and its supporting evidence.

Cap every row at zero. Readiness passes only at **>= 95/100**. Any score below 95 blocks implementation. **No unresolved critical risk** is a separate veto: it blocks implementation even at 95/100 or higher. List deductions and required repairs; revise and re-review independently. Apply this complete rubric and veto to each implementation chunk before its gate.

A readiness score measures process coverage. It does not replace executable proof, a deterministic oracle, immutable baseline evidence, or the separate task and integration gates. No row may compensate for a critical `ASSUMPTION`, `BLOCKED`, or `STALE` proof status.
