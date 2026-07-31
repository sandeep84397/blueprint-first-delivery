# Blueprint-First Delivery Skill — Design

## Goal

Ship a portable Codex skill that turns ambiguous feature work into small, evidence-backed implementation chunks. The skill must require a plain-English design before code, independent design review, readiness gates, safe parallelism, incremental integration, and final requirement traceability.

## Scope

The first release is a documentation-led Codex skill. It includes reusable templates, review checklists, a 100-point readiness rubric, and pressure scenarios that verify the skill resists premature coding and false parallelism.

The skill works without Agent Brain. When Agent Brain is available, the skill may log design, gate, and final-verification evidence; that integration remains optional.

## Repository layout

```text
skills/blueprint-first-delivery/
  SKILL.md
  agents/openai.yaml
  references/
    blueprint-templates.md
    readiness-rubric.md
    review-and-gate-checklists.md
  tests/
    pressure-scenarios.md
    validate-skill.sh
README.md
```

## Workflow contract

1. Explore existing architecture and clarify requirements.
2. Produce a module-level plain-English blueprint before implementation.
3. Obtain a principal-engineer-style adversarial design review.
4. Divide work until every implementation chunk has one responsibility, clear contracts, testable acceptance criteria, and a readiness score of at least 95/100.
5. Run chunks in parallel only when their approved contracts are frozen and their file/state ownership does not overlap.
6. Complete each chunk only after implementation, focused tests, blueprint-to-code review, contract verification, and no unresolved critical assumptions.
7. Treat integration as a separate designed chunk. Incrementally combine completed chunks and run contract, integration, end-to-end, and regression checks.
8. Finish with a requirement-to-evidence traceability report.

## Readiness scoring

| Evidence | Points |
| --- | ---: |
| Requirement clarity | 15 |
| Blueprint completeness | 15 |
| Interfaces and contracts | 15 |
| Dependency isolation | 10 |
| Acceptance criteria | 10 |
| Testability | 15 |
| Edge-case handling | 10 |
| Independent review | 10 |
| Total | 100 |

Implementation requires a score of at least 95 and no unresolved critical risk. This is process-readiness evidence, not a mathematical correctness guarantee.

## Non-goals

- Do not promise literal probability of correctness.
- Do not force parallel agents for dependent work.
- Do not require Agent Brain, a particular language, or a test framework.
- Do not replace project-specific architecture or test conventions.

## Validation

The repository will validate structure and frontmatter mechanically. Pressure scenarios will test three failure modes: coding before design approval, declaring false independence, and skipping the integration gate after passing unit tests. A successful run must produce the required artifacts and refuse each unsafe shortcut.

## Acceptance criteria

- The skill is discoverable from its name and description.
- Templates make each required design/gate artifact unambiguous.
- The rubric makes the 95-point threshold reproducible.
- Parallelism is conditional on explicit independence evidence.
- Integration has its own blueprint and completion gate.
- Tests validate both package shape and pressure-scenario expectations.
