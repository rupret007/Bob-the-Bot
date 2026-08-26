#!/usr/bin/env node
import { fileURLToPath } from 'node:url';
import path from 'node:path';

import {
  verifyEngineContract,
  verifyStaticContract,
} from './lib/contract.mjs';

const root = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const args = process.argv.slice(2);
let engineRoot = null;
let apply = false;

for (let index = 0; index < args.length; index += 1) {
  const value = args[index];
  if (value === '--engine') {
    engineRoot = args[index + 1] || null;
    index += 1;
  } else if (value === '--apply') {
    apply = true;
  } else {
    throw new Error('unknown argument: ' + value);
  }
}
if (apply && !engineRoot) {
  throw new Error('--apply requires --engine <disposable-checkout>');
}

try {
  const report = engineRoot
    ? verifyEngineContract({ root, engineRoot, apply })
    : verifyStaticContract({ root });
  console.log(
    JSON.stringify(
      {
        ok: true,
        mode: engineRoot ? (apply ? 'applied' : 'apply-check') : 'static',
        engineBase: report.engineBase || null,
        resultTree: report.resultTree || null,
        overlaySha256: report.overlaySha256,
        touchedPaths: report.touchedPaths.length,
        liveActions: 0,
      },
      null,
      2,
    ),
  );
} catch (error) {
  console.error(
    'Bob contract verification failed: ' +
      (error instanceof Error ? error.message : String(error)),
  );
  process.exitCode = 1;
}
