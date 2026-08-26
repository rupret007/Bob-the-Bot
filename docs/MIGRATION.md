# Migration record

## Starting point

Bob-the-Bot began as a private repository with a single README commit. The working
Bob behavior already existed as six commits on an Andrea development branch:

1. 70a898a2f0509032993debfe37ee0636aa9a89fd — natural Bob-style Telegram UX
2. f1f32e2a9112829b25507159078b0732fd281106 — Bob BotFather copy
3. 274a67cdbda12fca6cf566f7ccc2bedcb5ecebbe — quick-reply formatting
4. d04ef01249c2c4a446caf9f5c10811cd98a49d58 — Bob public identity
5. 0d5407e94c33037df974e9dd7064e3c828a2b58b — guidance regression alignment
6. 723a793b78513c979b866dd589f63d06add37897 — natural UX menu cleanup

## Reconciliation result

All six commits replayed cleanly, in order, onto authoritative Andrea main
f8655e2da59d1db8bd3777758ae8220ecb65d847. No older branch-only commit was
required. The combined result modifies 15 existing source, test, and group-guidance
files and produces Git tree 6c193efa849e16392c4ba179c261cdcb6bc7aa17.

The combined patch is preserved rather than copying the Andrea tree. Its digest,
scope, source commits, base, and result tree are locked in the versioned contract.
The first acceptance run also exposed stale inherited expectations for Bob's
natural command-free copy. The overlay includes the narrow test alignment and makes
the send-approval requirement visible in short Telegram help, welcome, and feature
copy.

## Safe update procedure

1. Start with a fresh disposable clone of the new Andrea main.
2. Reconcile the six source changes or the latest reviewed replacement.
3. Run the strongest offline Andrea tests before exporting an overlay.
4. Replace the patch, engine pin, digest, touched-path allowlist, and result tree together.
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
