# Bob the Bot

Private application contract for Bob: the same direct, natural public assistant
identity used by Bot the Bot on Telegram, backed by the established Andrea
messaging engine and guarded OpenClaw delegation.

Status: bootstrap only. This repository does not deploy, start, restart, message,
or configure a live runtime.

## Why this repository is thin

The working messaging, approval, and OpenClaw integration code already exists in
Andrea NanoBot. Copying that engine here would create two drifting implementations.
Instead, this repository pins one reviewed Andrea commit and carries the smallest
reproducible Bob overlay plus independent acceptance checks.

    Bob-the-Bot contract and overlay
                 |
                 v
    Andrea NanoBot messaging and approval engine
                 |
                 +---- guarded OpenClaw helper lane
                 |
                 +---- Telegram and Messages adapters

Bob Ops Dashboard remains a separate portfolio control plane. It is not the Bob
application runtime.

## What is included

- contracts/bob-app.v1.json pins the engine, overlay digest, result tree, and file scope.
- patches/andrea-bob-overlay.patch preserves the six existing Bob identity and
  natural Telegram UX commits reconciled onto the current engine.
- config/bob.env.example contains non-secret, fail-closed product defaults only.
- scripts/verify-contract.mjs rejects base, patch, tree, scope, and safety drift.
- CI applies the overlay only to a disposable pinned engine checkout, then runs
  offline identity, routing, OpenClaw, and send-authorization tests.

## Local contract checks

Node 22 is required. These checks do not need an engine checkout and do not call
live services.

    npm ci --ignore-scripts
    npm run check

To verify the integration itself, use a disposable clone only:

    git clone https://github.com/rupret007/Andrea_NanoBot .engine/Andrea_NanoBot
    git -C .engine/Andrea_NanoBot checkout --detach f8655e2da59d1db8bd3777758ae8220ecb65d847
    npm run verify:engine

verify:engine intentionally applies the reviewed overlay to that disposable
checkout. Never point it at an active or user-owned Andrea worktree.

## Safety boundary

- No credentials, recipient details, endpoints, runtime databases, logs, or media belong here.
- Outbound messaging, control APIs, and the OpenAI backend are disabled in the
  example. CI has no credentials and loads Andrea's network guard.
- Tests use Andrea's network guard and mocked adapters.
- No merge authorizes a live send, gateway restart, settings change, deployment,
  provider call, or production action.
- Updating the engine pin or overlay invalidates the recorded proof and requires a
  new review.

See docs/ARCHITECTURE.md, docs/MIGRATION.md, SECURITY.md, and
docs/TROUBLESHOOTING.md before changing the contract.
