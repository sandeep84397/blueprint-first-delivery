# Adaptive evidence-first pressure scenarios

| ID | Pressure case | Expected result |
| --- | --- | --- |
| AE01 | Exact one-owner reversible change with deterministic oracle and no handoff | Direct |
| AE02 | Bounded implementation with one owner and no Full trigger | Lite |
| AE03 | Unknown external API behavior or unresolved external dependency | Full |
| AE04 | Persistence, migration, recovery, deletion, or integrity risk | Full |
| AE05 | Two modules or state owners on one causal path | Full |
| AE06 | Critical contract has prose but no named executable oracle | Approval blocked |
| AE07 | Baseline contract, owned file, or evidence digest changes | Evidence STALE; re-approval required |
| AE08 | Full work has Agent Brain summary without source references | Gate blocked |
| AE09 | Integration is deferred until the final milestone | Early vertical proof required |
| AE10 | Lite handoff lacks source-linked Agent Brain | Gate blocked |
