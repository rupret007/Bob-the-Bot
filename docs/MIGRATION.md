# Migration record

## Starting point

Bob-the-Bot began as a private repository with a single README commit. Six Bob
change sets were observed in isolated, user-owned local Andrea history: natural
Telegram UX, BotFather copy, quick-reply formatting, public identity, guidance
regression alignment, and natural-UX menu cleanup.

Those local commit objects are not reachable from an Andrea origin ref and are not
an authoritative or portable dependency. Their raw IDs and machine-local author
metadata are intentionally omitted. The reviewed overlay below is the sanitized,
self-contained preservation boundary.

## Reconciliation result

All six local change sets reconciled cleanly, in order, onto authoritative Andrea main
f8655e2da59d1db8bd3777758ae8220ecb65d847. No older branch-only commit was
required. The reviewed result modifies 21 existing source, test, and group-guidance
files and produces Git tree 58f3e0a88ddd0d60a613331f0bc266aea5d51d04.

The combined patch is preserved rather than copying the Andrea tree. Its SHA-256
digest, derived stable patch ID, scope, public base, and result tree are locked in
the versioned contract and are the authoritative replay evidence.
The first acceptance run also exposed stale inherited expectations for Bob's
natural command-free copy. The overlay includes the narrow test alignment and makes
the send-approval requirement visible in short Telegram help, welcome, and feature
copy.

Independent review then found that natural-UX cleanup could restore a short
requested completion after delivery authorization had denied it. The repair moves
plain denied wording into the payload resolver, never reuses the requested claim or
controls, and adds a focused false-completion regression test. Draft head
42440481d832991db323a919031cf075a23c2d8f is superseded and must not be approved.
The complete offline suite also exposed four stale identity assertions and a real
default-trigger regression: with Bob configured, explicit @openclaw addressing no
longer matched. The reconciliation now preserves that guarded alias and makes the
affected expectations identity-aware.

## Safe update procedure

1. Start with a fresh disposable clone of the new Andrea main.
2. Start from the current reviewed overlay or a separately reviewed supported replacement.
3. Run the strongest offline Andrea tests before exporting an overlay.
4. Replace the patch, engine pin, digest, derived patch ID, touched-path allowlist,
   and result tree together.
5. Run npm run check and the disposable-engine acceptance suite.
6. Review the full diff for secrets, local paths, generated files, authority drift,
   unsafe links, and misleading readiness claims.
7. Publish a new draft and request approval for its exact head.

Never update only the engine pin to make a failing check pass. A mismatch is a
compatibility signal, not an invitation to bypass verification.

## Remaining migration work

- Decide whether to upstream a first-class Bob identity configuration into Andrea.
- If upstreamed, replace the patch with the smaller supported interface only after
  equivalent acceptance passes.
- Keep Andrea and Bob responsibilities explicit so neither becomes a silent fork.
- Connect or deploy a live Bob runtime only through a separately approved owner runbook.

## Rollback

This bootstrap has no production side effect. Discard the disposable engine clone
or revert the Bob draft branch to remove it. No service restart, credential change,
message, or remote runtime operation is required.
