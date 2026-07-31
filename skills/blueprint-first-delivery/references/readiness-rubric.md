# Readiness rubric

Principal-engineer-style adversarial reviewer scores the blueprints before implementation. Author and reviewer must be different people/agents. Reviewer actively challenges contracts, hidden dependencies, ownership, failure paths, security, and claimed evidence.

| Area | Points | Pass condition |
| --- | ---: | --- |
| Scope and acceptance criteria | 15 | Explicit, testable, bounded |
| Module boundaries and ownership | 15 | Every change area has one clear purpose/owner; parallel work has frozen contracts and non-overlapping file/state ownership |
| Contracts and validation | 20 | Inputs, outputs, errors, and compatibility stated |
| Dependencies and ordering | 15 | Each dependency classified; no false independence |
| Data, security, and failure handling | 15 | State changes, authorization, and recovery covered |
| Verification and integration blueprint | 10 | Component evidence plus a separate integration blueprint and evidence defined |
| Risks and traceability | 10 | Assumptions, residual risks, and criterion mapping explicit |
| **Total** | **100** | |

Readiness passes only at **>= 95/100**. Any score below 95 blocks implementation. List deductions and required repairs; revise and re-review independently.
