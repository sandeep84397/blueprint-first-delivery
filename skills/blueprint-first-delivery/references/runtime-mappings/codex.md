# Codex runtime mapping

Mapping version: `1`

| Tier | Requested model | Effort | Same-tier fallback | Higher fallback |
| --- | --- | --- | --- | --- |
| Light | `gpt-5.6-luna` | `low` | none | `gpt-5.6-terra` / `low` |
| Standard | `gpt-5.6-terra` | `medium` | none | `gpt-5.6-sol` / `medium` |
| Deep | `gpt-5.6-sol` | `high` | none | `gpt-5.6-sol` / `max` only after Maximum review |
| Maximum | `gpt-5.6-sol` | `max` | none | blocked; decompose or review a new mapping |

## Request mechanism

Use a model-pinned custom subagent or a runtime call that explicitly accepts model and reasoning effort. A generic task label does not prove selection. Record the request metadata returned by the runtime.

## Availability and supported effort

Before dispatch, inspect the callable custom-agent/runtime metadata for the requested model and effort. If availability or effective effort cannot be observed, mark execution unverified. Deep and Maximum remain blocked. Deep may request xhigh only with policy evidence; Maximum uses max.

## Verification and fallback

Record runtime version, observed model, observed effort, metadata source, observation timestamp, alias resolution, and fallback chain. If the runtime cannot prove a Deep/Maximum floor, block. If Luna is unavailable, Light may promote to Terra/low and must record the promotion.

Codex Ultra is orchestrator-level parallel execution for at least two independently proven workstreams. It is not a chunk tier or a substitute for Maximum.

## Digest

Compute the mapping digest from the repository root:

```sh
shasum -a 256 skills/blueprint-first-delivery/references/runtime-mappings/codex.md
```
