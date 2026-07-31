# Readiness rubric

Independent reviewer scores the blueprint before implementation. Author and reviewer must be different people/agents.

| Area | Points | Pass condition |
| --- | ---: | --- |
| Scope and acceptance criteria | 15 | Explicit, testable, bounded |
| Module boundaries and ownership | 15 | Every change area has one clear purpose and owner |
| Contracts and validation | 20 | Inputs, outputs, errors, and compatibility stated |
| Dependencies and ordering | 15 | Each dependency classified; no false independence |
| Data, security, and failure handling | 15 | State changes, authorization, and recovery covered |
| Verification plan | 10 | Component plus integration evidence defined |
| Risks and traceability | 10 | Assumptions, residual risks, and criterion mapping explicit |
| **Total** | **100** | |

Readiness passes only at **>= 95/100**. Any score below 95 blocks implementation. List deductions and required repairs; revise and re-review independently.
