# Claude Code runtime mapping

Mapping version: `1`

| Tier | Requested model | Effort | Same-tier fallback | Higher fallback |
| --- | --- | --- | --- | --- |
| Light | `haiku` | `low` | none | `sonnet` / `low` |
| Standard | `sonnet` | `medium` | none | `opus` / `medium` |
| Deep | `opus` | `high` | none | `opus` / `max` only after Maximum review |
| Maximum | `opus` | `max` | none | blocked; decompose or review a new mapping |

## Request mechanism

Use a Claude Code subagent whose frontmatter or invocation pins `model` and `effort`.

## Availability and supported effort

Inspect and record `CLAUDE_CODE_SUBAGENT_MODEL`, `CLAUDE_CODE_EFFORT_LEVEL`, organization `availableModels`, organization effort caps, and runtime-reported effective model/effort. Environment or organization overrides win over subagent frontmatter. Unsupported effort may fall downward; Deep/Maximum mismatches block.

## Verification and fallback

Record runtime version, requested alias, resolved/observed model, observed effort, metadata source, observation timestamp, and fallback chain. If the runtime cannot prove a Deep/Maximum floor, block. Unsupported effort fallback is not proof that the requested floor ran.

## Digest

Compute the mapping digest from the repository root:

```sh
shasum -a 256 skills/blueprint-first-delivery/references/runtime-mappings/claude-code.md
```
