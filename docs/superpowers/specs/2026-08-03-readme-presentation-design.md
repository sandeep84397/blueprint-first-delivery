# README Presentation Redesign

## Goal

Make the public README explain the project before presenting its implementation details. A first-time visitor should understand what Blueprint-First Delivery does, why it exists, how it reduces AI coding failures, and how to use it with Codex or Claude Code.

## Audience

- Developers using coding agents for features, refactors, or multi-part changes.
- Technical leads who want design review, bounded execution, and objective delivery evidence.
- Contributors evaluating the repository before installation.

## Core message

Blueprint-First Delivery reduces ambiguity-driven AI coding failures by designing work in plain English, reviewing the design independently, splitting delivery into small verifiable chunks, routing each chunk to the cheapest capable model, and treating integration as its own reviewed and tested unit.

The README must not promise 95% or 100% software correctness. Its readiness threshold represents collected process evidence, not a mathematical probability.

## Narrative structure

1. Project title and one-sentence value proposition.
2. “What this project does” summary.
3. “The problem”:
   - large ambiguous tasks overload working context;
   - missing decisions are filled by assumptions;
   - coding before holistic review creates late refactoring;
   - individually correct components can still fail during integration;
   - self-reported confidence is not reliable evidence.
4. “The solution”:
   - plain-English module blueprint;
   - independent Principal Engineer review;
   - smallest practical single-responsibility chunks;
   - evidence-based model routing;
   - per-chunk start and completion gates;
   - explicit integration blueprint and gate;
   - final requirement traceability.
5. A compact end-to-end workflow.
6. “What you get” outcomes and artifacts.
7. A practical example showing one large feature becoming ordered and independently verifiable chunks.
8. Model-routing table and essential safety semantics.
9. Codex and Claude Code installation.
10. Usage examples.
11. Repository layout and validation.
12. Honest limitations.

## Presentation rules

- English only.
- No generated images, icons, badges, or decorative visual assets in this change.
- Lead with user value; move routing mechanics below the problem and solution.
- Prefer short paragraphs, scannable headings, tables, and one compact text workflow.
- Preserve all valid installation commands, compatibility warnings, routing safety rules, validation requirements, and repository paths from the existing README.
- Do not duplicate the full policy or every test scenario; link readers to repository references where detail is needed.

## Example shape

Use a neutral feature such as offline profile editing:

- define source of truth and conflict behavior;
- freeze repository/UI contracts;
- implement local persistence and UI in bounded chunks;
- run only genuinely independent chunks in parallel;
- integrate incrementally;
- validate end to end against the original requirement.

The example demonstrates the method without claiming that SOLID decomposition alone guarantees correctness.

## Validation

- Existing package validation remains green.
- README wrapper assertions remain green.
- All installation paths and commands remain present.
- README includes explicit purpose, problem, solution, workflow, outcomes, example, model routing, installation, usage, validation, and limitations sections.
- Git diff check passes.

## Out of scope

- Changes to skill behavior, routing policy, tests, runtime mappings, or global Codex/Claude configuration.
- Removal of duplicated global guidance.
- New image or icon assets.
- Claims of external Claude Code execution.
