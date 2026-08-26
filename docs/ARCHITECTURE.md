# Architecture

## Product boundary

Bob the Bot is the public product identity. Andrea NanoBot remains the established
messaging, persistence, routing, approval, and channel engine. OpenClaw remains a
guarded helper lane and is public only when the user explicitly addresses it.

This repository owns:

- Bob identity and natural interaction policy
- the exact engine compatibility pin
- the reviewed overlay that expresses the Bob product behavior
- safe example defaults
- integration and privacy acceptance
- migration and operator documentation

This repository does not own:

- Andrea engine internals outside the declared overlay
- live runtime state or service configuration
- Bob Ops Dashboard
- credentials, recipients, messages, or provider data
- production deployment or service lifecycle

## Reproducible integration contract

contracts/bob-app.v1.json binds six reproducible facts:

1. The exact public Andrea engine base commit.
2. The exact SHA-256 digest of the Bob overlay.
3. The stable Git patch ID derived from that overlay.
4. The complete allowlist of modified engine paths.
5. The exact Git tree expected after the overlay is applied.
6. Safety flags that must all remain false for live requirements and default sends.

Verification fails before tests when any of those facts drift. The overlay may
modify only existing text files under src or groups. New files, deleted files,
renames, binary patches, local paths, and credential-shaped content are rejected.

Six Bob change sets were observed only as local unpublished history during the
reconciliation. They are recorded as sanitized, non-authoritative provenance: the
contract asserts no remote reachability and includes no raw object IDs or local
author metadata. The public base plus overlay digest, derived patch ID, and result
tree are the authoritative replay evidence.

## Runtime relationship

Andrea already exposes ASSISTANT_NAME and carries the guarded messaging and
delegation behavior. The Bob overlay supplies the existing Bob-specific copy,
plain-language Telegram behavior, and identity guidance without bringing runtime
state into this repository.

The non-secret example selects Bob and natural Telegram UX while leaving
BlueBubbles send, its control API, and the Andrea OpenAI backend disabled. Real
runtime values remain owner-controlled and outside source control.

## Authority

The overlay does not widen authority. Existing engine tests remain the source of
truth for routing and exact send authorization. CI adds a Bob-specific acceptance
slice over those tests, with live communication disabled and the network guard
loaded.

Natural Telegram wording is selected inside the denied-delivery payload resolver.
It never substitutes the original requested completion after authorization has
failed, and denied controls remain discarded before the send boundary.

Only an explicit owner decision can authorize a merge. A merge still does not
authorize deployment, messaging, provider use, credentials, settings, gateway
restart, or any production action.

## Long-term direction

The preferred future endpoint is an upstream, tested public-identity configuration
boundary in Andrea that can express Bob without a patch. Until that interface
exists and passes the same acceptance suite, the pinned overlay is the smaller and
more honest reuse mechanism. It prevents a silent engine fork and makes drift
visible.
