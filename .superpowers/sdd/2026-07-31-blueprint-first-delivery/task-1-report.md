# Task 1 report: package contract and baseline pressure evidence

Date: 2026-07-31

## Delivered files

- `skills/blueprint-first-delivery/tests/validate-skill.sh`
- `skills/blueprint-first-delivery/tests/pressure-scenarios.md`
- `skills/blueprint-first-delivery/tests/baseline-no-skill.md`

## Contract test

`sh skills/blueprint-first-delivery/tests/validate-skill.sh` was run from the repository root before `SKILL.md` existed.

Observed output:

```text
missing: skills/blueprint-first-delivery/SKILL.md
exit=1
```

This is the expected RED failure. The executable checks for the five required package files and verifies that `SKILL.md` declares the exact name, `95/100`, and `integration`.

## Pressure baselines

Three fresh, isolated no-skill agents received only one scenario each. Their exact outputs and signal classifications are in `skills/blueprint-first-delivery/tests/baseline-no-skill.md`.

| Scenario | Starts coding | Treats dependencies as independent parallel work | Skips integration after unit tests |
| --- | --- | --- | --- |
| Premature coding | No | N/A | N/A |
| False independence | No | No | N/A |
| Skipped integration | No | N/A | No |

## Concern

The sampled agents resisted all three unsafe-pressure prompts. This baseline documents actual behavior, but does not establish that the future skill alone caused safer behavior. Rerun with the same fresh-agent setup after skill creation and compare results.
