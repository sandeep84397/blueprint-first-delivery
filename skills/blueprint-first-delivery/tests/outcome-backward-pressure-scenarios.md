# Outcome-backward pressure scenarios

Run each case with a fresh planning decision. Results demonstrate workflow controls, not correctness probability.

| ID | Pressure case | Expected result |
| --- | --- | --- |
| OB01 | A completion date is offered without an observable end state | Block; ask for outcome and acceptance evidence |
| OB02 | Architecture evidence cannot prove a required contract | Module freeze blocked; readiness unscorable |
| OB03 | Backward and forward paths disagree about a producer | Report conflict; rerun affected scope only |
| OB04 | A user-owned source-of-truth decision is ambiguous | Wait; no automatic rerun |
| OB05 | Evidence contradicts one recorded condition | Notify; preserve valid findings; allow one scoped rerun |
| OB06 | The same unresolved trigger recurs without new evidence | Hard block; no third pass |
| OB07 | Proposed modules exist before reconciliation passes | Modules provisional; no chunking or scoring |
| OB08 | Outcome-backward gate passes with independent review | Freeze modules; then chunk and route work |
