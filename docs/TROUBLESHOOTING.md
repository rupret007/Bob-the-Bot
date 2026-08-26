# Troubleshooting

## Engine checkout is not at the pinned base

Use a fresh disposable Andrea clone and detach it at the exact engine commit in
contracts/bob-app.v1.json. Do not reset or modify an existing user worktree.

## Engine checkout must be clean

The verifier refuses to mix Bob with unrelated changes. Use a new disposable clone.
Preserve the existing checkout and any backups.

## Overlay digest mismatch

The patch changed without a reviewed contract update. Inspect the full patch. If the
change is intentional, regenerate the digest, touched-path allowlist, and expected
result tree from one reviewed reconciliation.

## Overlay patch ID mismatch

The content-normalized Git patch identity does not match the contract. Do not paste
in a plausible 40-character value. Regenerate it from the reviewed overlay and
confirm the SHA-256 digest, scope, and result tree in the same review.

## Patch does not apply

The Andrea engine moved or the patch was edited. Reconcile against the new engine in
an isolated branch. Do not relax the base check or apply with rejected hunks.

## Patched tree mismatch

The final content differs from the reviewed result even if the patch applied. Stop
and inspect whitespace, file modes, and all changed files. Never replace the
expected tree merely to silence the failure.

## A targeted engine test fails

Run that same test against the reconciled disposable engine and classify the
failure. Network, credentials, services, and communication are disabled by design.
Do not enable a live dependency to turn CI green.

## Hosted CI has not completed

Report the branch as locally verified or hosted pending. A queued integration with
no test job is not green or red, and it authorizes no merge or live action.

If GitHub creates a job with zero steps and no runner, inspect its annotation. A
payment or spending-limit annotation is billing-blocked, not a code failure. Do not
rerun it until billing is confirmed fixed; retain the complete local proof record.
