#!/usr/bin/env node
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const skippedDirectories = new Set([
  '.git',
  '.engine',
  'node_modules',
  'coverage',
]);
const forbiddenDirectoryNames = new Set(['backups', 'data', 'dist', 'logs']);
const forbiddenPatterns = [
  ['/Users path', /\/Users\//u],
  ['/home/runner path', /\/home\/runner/u],
  ['file URL', /file:\//u],
  ['private key', /BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY/u],
  ['GitHub token', /gh[pousr]_[A-Za-z0-9_]+/u],
  ['OpenAI-style token', /sk-[A-Za-z0-9_-]{20,}/u],
  ['Slack token', /xox[baprs]-[A-Za-z0-9-]+/u],
  [
    'credential assignment',
    /(?:TOKEN|API_KEY|PASSWORD|SECRET)\s*=\s*(?!\s*(?:$|#|<))\S+/u,
  ],
];

const files = [];
function walk(directory) {
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    if (entry.isDirectory() && skippedDirectories.has(entry.name)) {
      continue;
    }
    const absolute = path.join(directory, entry.name);
    const relative = path.relative(root, absolute).split(path.sep).join('/');
    if (entry.isDirectory()) {
      if (forbiddenDirectoryNames.has(entry.name)) {
        throw new Error('forbidden generated/private directory: ' + relative);
      }
      walk(absolute);
    } else if (entry.isFile() && statSync(absolute).size <= 1_000_000) {
      files.push({ absolute, relative });
    }
  }
}

walk(root);
let scannedFiles = 0;
for (const file of files) {
  if (file.relative === 'scripts/privacy-check.mjs') {
    continue;
  }
  scannedFiles += 1;
  const text = readFileSync(file.absolute, 'utf8');
  for (const [label, pattern] of forbiddenPatterns) {
    if (pattern.test(text)) {
      throw new Error(label + ' found in ' + file.relative);
    }
  }
}

console.log(
  JSON.stringify({
    ok: true,
    filesScanned: scannedFiles,
    scannerSelfExcluded: 1,
    localPaths: 0,
    credentialValues: 0,
    generatedOrPrivateDirectories: 0,
  }),
);
