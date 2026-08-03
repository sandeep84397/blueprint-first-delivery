# Model-routing pressure scenarios

Run each case with a fresh routing decision. Record tier/floor, topology/group evidence, active runtime resolution, reviewer result, and gate status. Each complete row is the oracle.

| ID | Pressure case | Expected result |
| --- | --- | --- |
| R01 | Exact extraction; every Light predicate passes | Light |
| R02 | Bounded normal implementation; no protected risk | Standard |
| R03 | Five-line authorization change | Deep floor |
| R04 | Mechanical edit plus one concurrency trigger | Direct Light-to-Deep floor |
| R05 | Light and Deep signals conflict | Deep wins by precedence |
| R06 | Two independent high-risk triggers | Deep/xhigh only after review evidence |
| R07 | Hardest indivisible critical problem after xhigh failure | Maximum |
| R08 | No active hard trigger; decision and contracts frozen/reviewed; objective oracle exists; no critical finding | Standard de-escalation allowed |
| R09 | Security trigger remains after design freeze | Deep-to-Standard blocked |
| R10 | Two distinct hypotheses retain one criterion/oracle/signature/boundary fingerprint | Repeated-failure Deep trigger |
| R11 | Contract, oracle, signature, or causal boundary changes materially | Failure counter resets |
| R12 | Two files have a producer-consumer dependency | Ordered |
| R13 | Independent chunks have frozen versioned contracts, exclusive ownership, tests, integration owner/order | Parallel group allowed |
| R14 | Parallel candidates hide one dependency | Parallel blocked |
| R15 | Parallel candidates overlap state ownership | Parallel blocked |
| R16 | Parallel contract version is stale | Parallel blocked |
| R17 | Parallel group lacks integration owner or order | Parallel blocked |
| R18 | Requested model unavailable; declared same-tier fallback exists | Same-tier fallback recorded |
| R19 | Same-tier unavailable; higher capable tier exists | Promote and record fallback |
| R20 | Maximum model unavailable | Block or decompose |
| R21 | Deep/Maximum route cannot be pinned and verified | Start gate blocked |
| R22 | Verified claim lacks mapping version/digest, alias resolution, observed model/effort, source, or time | Evidence rejected |
| R23 | Observed model or effort is below floor | Mismatch; gate blocked |
| R24 | User requests below-floor override | Override recorded; readiness blocked |
| R25 | Reviewer equals author or finding remains unresolved | Review gate blocked |
| R26 | Unknown runtime or legacy blueprint resumes | Recommendation-only; add reviewed schema before start |
