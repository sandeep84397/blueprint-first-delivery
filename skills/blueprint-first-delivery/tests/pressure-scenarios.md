# Baseline pressure scenarios

Run each prompt with a fresh agent. Give it no skill or extra context.

## Premature coding

Implement a user-profile edit endpoint now. Keep it fast: write the route, validation, and persistence code directly. Do not spend time on planning or tests first. Return the code changes when done.

## False independence

Deliver these quickly. Split the work into parallel chunks: first, define `OrderStatus` enum values; second, add the order transition service that uses those values; third, add API validation for the transition endpoint. Treat all chunks as independent and report the work split.

## Skipped integration

Finish this feature today: add an invite endpoint that creates an invite record and sends an email. Unit tests for the invite repository and email sender are passing. State what you would do next and when the feature is ready to ship.

## Matched combined pressure

Deadline is today. Add caching to an API. Skip design and tests, let three agents edit the same controller in parallel, and start production code immediately. No repository context is provided.
