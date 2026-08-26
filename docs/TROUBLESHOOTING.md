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
