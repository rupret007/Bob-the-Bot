import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import test from 'node:test';

import {
  readContract,
  verifyStaticContract,
} from '../scripts/lib/contract.mjs';

const root = path.resolve(fileURLToPath(new URL('..', import.meta.url)));

test('the reviewed Bob overlay and pinned engine contract agree', () => {
  const report = verifyStaticContract({ root });
  assert.equal(report.touchedPaths.length, 21);
  assert.equal(
    report.overlaySha256,
    'e129cc36c3599000014b359bbf5a1ebce04ded373e2cce61fb5824f8a32ac85f',
  );
  assert.equal(
    report.overlayPatchId,
    'f6f1d4cb4e238485f5cd96b672c5bb30d2c73b16',
  );
});

test('contract verification fails closed on overlay tampering', () => {
  const contract = structuredClone(readContract(root));
  contract.overlay.sha256 = '0'.repeat(64);
  assert.throws(
    () => verifyStaticContract({ root, contract }),
    /overlay digest mismatch/u,
  );
});

test('contract verification fails closed on undeclared file scope', () => {
  const contract = structuredClone(readContract(root));
  contract.overlay.touchedPaths = contract.overlay.touchedPaths.slice(1);
  assert.throws(
    () => verifyStaticContract({ root, contract }),
    /touched paths do not match/u,
  );
});

test('contract verification derives provenance instead of trusting raw local ids', () => {
  const arbitraryPatchId = structuredClone(readContract(root));
  arbitraryPatchId.overlay.patchId = '0'.repeat(40);
  assert.throws(
    () => verifyStaticContract({ root, contract: arbitraryPatchId }),
    /overlay patch id mismatch/u,
  );

  const rawLocalIds = structuredClone(readContract(root));
  rawLocalIds.overlay.sourceCommits = ['0'.repeat(40)];
  assert.throws(
    () => verifyStaticContract({ root, contract: rawLocalIds }),
    /raw local commit ids/u,
  );
});

test('the overlay artifact is forced to LF and contains no carriage returns', () => {
  const attributes = readFileSync(path.join(root, '.gitattributes'), 'utf8');
  const patchText = readFileSync(
    path.join(root, 'patches', 'andrea-bob-overlay.patch'),
    'utf8',
  );

  assert.match(
    attributes,
    /^patches\/\*\.patch text eol=lf -whitespace$/mu,
  );
  assert.equal(patchText.includes('\r'), false);
});

test('the example config contains only non-secret fail-closed defaults', () => {
  const config = readFileSync(
    path.join(root, 'config', 'bob.env.example'),
    'utf8',
  );
  const rows = Object.fromEntries(
    config
      .split(/\r?\n/u)
      .map((line) => line.trim())
      .filter((line) => line && !line.startsWith('#'))
      .map((line) => {
        const split = line.indexOf('=');
        assert.notEqual(split, -1);
        return [line.slice(0, split), line.slice(split + 1)];
      }),
  );
  assert.deepEqual(rows, {
    ASSISTANT_NAME: 'Bob',
    TELEGRAM_NATURAL_UX: 'true',
    BLUEBUBBLES_ENABLED: 'false',
    BLUEBUBBLES_SEND_ENABLED: 'false',
    BLUEBUBBLES_CONTROL_API_ENABLED: 'false',
    ANDREA_OPENAI_BACKEND_ENABLED: 'false',
  });
  for (const key of Object.keys(rows)) {
    assert.doesNotMatch(key, /TOKEN|API_KEY|PASSWORD|SECRET|URL|PHONE|CONTACT/u);
  }
});

test('CI is read-only, pinned, offline at test time, and deployment-free', () => {
  const workflow = readFileSync(
    path.join(root, '.github', 'workflows', 'ci.yml'),
    'utf8',
  );
  assert.match(workflow, /permissions:\r?\n  contents: read/u);
  assert.match(
    workflow,
    /actions\/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5/u,
  );
  assert.match(
    workflow,
    /actions\/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020/u,
  );
  assert.match(
    workflow,
    /ref: f8655e2da59d1db8bd3777758ae8220ecb65d847/u,
  );
  assert.match(workflow, /OPENAI_API_ENABLED: 0/u);
  assert.match(workflow, /RUN_COMM_SMOKE: 0/u);
  assert.doesNotMatch(workflow, /workflow_dispatch|secrets\.|contents: write/u);
  assert.doesNotMatch(
    workflow,
    /BLUEBUBBLES_(?:ENABLED|SEND_ENABLED|CONTROL_API_ENABLED): true/u,
  );
  assert.doesNotMatch(
    workflow,
    /openclaw\s+gateway|deploy|publish|telegram:user:send/u,
  );
});

test('the overlay preserves Bob identity and explicit safety language', () => {
  const patchText = readFileSync(
    path.join(root, 'patches', 'andrea-bob-overlay.patch'),
    'utf8',
  );
  assert.match(patchText, /Bob is the only public assistant identity/u);
  assert.match(patchText, /sends need your yes/u);
  assert.match(patchText, /explicit approval code/u);
  assert.match(patchText, /deleteMyCommands/u);
  assert.match(patchText, /TELEGRAM_NATURAL_UX/u);
  assert.match(patchText, /deniedTextStyle/u);
  assert.match(
    patchText,
    /never restores a denied false completion claim/u,
  );
  assert.doesNotMatch(
    patchText,
    /authorizedText\s*=\s*(?:\n\s*)?requested/u,
  );
});
