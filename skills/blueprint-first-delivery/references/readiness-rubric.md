# Readiness rubric

Principal-engineer-style adversarial reviewer scores the blueprints before implementation. Author and reviewer must be different people/agents. Reviewer actively challenges contracts, hidden dependencies, ownership, failure paths, security, and claimed evidence.

| Area | Maximum | Awarded | Deductions |
| --- | ---: | ---: | --- |
| Scope and acceptance criteria | 15 |  | Deduct 5 per missing or non-testable criterion; deduct remaining points if scope is unbounded |
| Module boundaries and ownership | 15 |  | Deduct 5 per unclear owner/purpose; deduct 5 for each unsafe parallel claim |
| Contracts and validation | 20 |  | Deduct 5 per missing input/output/error/compatibility boundary |
| Dependencies and ordering | 15 |  | Deduct 5 per unclassified dependency or false-independence claim |
| Data, security, and failure handling | 15 |  | Deduct 5 per missing state, authorization, or recovery treatment |
| Verification and integration blueprint | 10 |  | Deduct 5 when focused verification or the separate integration blueprint is absent |
| Risks and traceability | 10 |  | Deduct 5 per missing assumption/residual-risk record or missing criterion mapping |
| **Total** | **100** |  | **Sum awarded points; record every deduction and repair.** |

Readiness passes only at **>= 95/100**. Any score below 95 blocks implementation. **No unresolved critical risk** is a separate veto: it blocks implementation even at 95/100 or higher. List deductions and required repairs; revise and re-review independently. Apply the same scoring and veto to each implementation chunk before its gate.
