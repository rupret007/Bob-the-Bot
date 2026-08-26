import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, statSync } from 'node:fs';
import path from 'node:path';

const SHA_PATTERN = /^[0-9a-f]{40}$/;
const DIGEST_PATTERN = /^[0-9a-f]{64}$/;

function invariant(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function sortedUnique(values) {
  return [...new Set(values)].sort();
}

function sameStringList(left, right) {
  return (
    left.length === right.length &&
    left.every((value, index) => value === right[index])
  );
}

function safeRelativePath(root, value, label) {
  invariant(typeof value === 'string' && value.length > 0, label + ' is required');
  invariant(!path.isAbsolute(value), label + ' must be relative');
  invariant(!value.includes('\\'), label + ' must use POSIX separators');
  const normalized = path.posix.normalize(value);
  invariant(
    normalized === value && normalized !== '..' && !normalized.startsWith('../'),
    label + ' must remain inside the repository',
  );
  const resolved = path.resolve(root, value);
  invariant(
    resolved.startsWith(path.resolve(root) + path.sep),
    label + ' escaped the repository',
  );
  return resolved;
}

export function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

export function extractTouchedPaths(patchText) {
  const paths = [];
  for (const line of patchText.split(/\r?\n/u)) {
    if (!line.startsWith('diff --git a/')) {
      continue;
    }
    const match = /^diff --git a\/(\S+) b\/(\S+)$/u.exec(line);
    invariant(Boolean(match), 'overlay contains an unsupported diff header');
    invariant(match[1] === match[2], 'overlay may not rename files');
    paths.push(match[1]);
  }
  invariant(paths.length > 0, 'overlay does not contain any file patches');
  return sortedUnique(paths);
}

export function readContract(root) {
  const contractPath = path.join(root, 'contracts', 'bob-app.v1.json');
  return JSON.parse(readFileSync(contractPath, 'utf8'));
}

export function verifyStaticContract({
  root,
  contract = readContract(root),
  patchText,
} = {}) {
  invariant(root, 'repository root is required');
  invariant(contract.schemaVersion === 1, 'unsupported contract schema');
  invariant(contract.application?.id === 'bob-the-bot', 'unexpected application id');
  invariant(contract.application?.displayName === 'Bob', 'public identity must be Bob');
  invariant(
    contract.application?.telegramDisplayName === 'Bot the Bot',
    'Telegram display identity must be Bot the Bot',
  );
  invariant(
    contract.application?.repository ===
      'https://github.com/rupret007/Bob-the-Bot',
    'unexpected application repository',
  );
  invariant(
    contract.application?.visibility === 'private',
    'Bob application contract must remain private',
  );
  invariant(
    contract.engine?.repository ===
      'https://github.com/rupret007/Andrea_NanoBot',
    'unexpected engine repository',
  );
  invariant(SHA_PATTERN.test(contract.engine?.baseCommit || ''), 'invalid engine base');
  invariant(
    contract.delegation?.name === 'OpenClaw' &&
      contract.delegation?.mode === 'guarded' &&
      contract.delegation?.publicOnlyWhenExplicitlyAddressed === true,
    'OpenClaw delegation must remain explicitly addressed and guarded',
  );

  const overlay = contract.overlay || {};
  invariant(DIGEST_PATTERN.test(overlay.sha256 || ''), 'invalid overlay digest');
  invariant(
    SHA_PATTERN.test(overlay.expectedResultTree || ''),
    'invalid expected result tree',
  );
  invariant(
    Array.isArray(overlay.sourceCommits) &&
      overlay.sourceCommits.length === 6 &&
      overlay.sourceCommits.every((value) => SHA_PATTERN.test(value)),
    'overlay must preserve the six source commit ids',
  );
  invariant(
    Array.isArray(overlay.touchedPaths) && overlay.touchedPaths.length > 0,
    'overlay touched paths are required',
  );
  invariant(
    typeof overlay.refinement?.purpose === 'string' &&
      overlay.refinement.purpose.length > 0 &&
      Array.isArray(overlay.refinement.files) &&
      overlay.refinement.files.length === 3 &&
      overlay.refinement.files.every((value) =>
        overlay.touchedPaths.includes(value),
      ),
    'overlay refinement must document its three in-scope files',
  );

  const overlayPath = safeRelativePath(root, overlay.path, 'overlay path');
  invariant(statSync(overlayPath).isFile(), 'overlay path is not a file');
  const actualPatch = patchText ?? readFileSync(overlayPath, 'utf8');
  invariant(sha256(actualPatch) === overlay.sha256, 'overlay digest mismatch');
  invariant(
    !/(?:^|\n)(?:new file mode|deleted file mode|rename from|rename to|GIT binary patch)/u.test(
      actualPatch,
    ),
    'overlay may only modify existing text files',
  );
  invariant(
    !/\/Users\/|\/home\/runner|file:\/|gh[pousr]_[A-Za-z0-9_]+|sk-[A-Za-z0-9_-]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY/u.test(
      actualPatch,
    ),
    'overlay contains a forbidden local path or credential pattern',
  );

  const actualTouched = extractTouchedPaths(actualPatch);
  const declaredTouched = sortedUnique(overlay.touchedPaths);
  invariant(
    declaredTouched.length === overlay.touchedPaths.length,
    'overlay touched paths must be unique',
  );
  invariant(
    sameStringList(actualTouched, declaredTouched),
    'overlay touched paths do not match the patch',
  );
  for (const touched of actualTouched) {
    safeRelativePath(root, touched, 'overlay touched path');
    invariant(
      touched.startsWith('src/') || touched.startsWith('groups/'),
      'overlay may only modify Andrea source or group guidance',
    );
  }

  for (const key of [
    'liveNetworkRequired',
    'credentialsRequired',
    'outboundMessagingDefault',
    'gatewayRestartRequired',
    'productionDeploymentRequired',
  ]) {
    invariant(contract.safety?.[key] === false, 'unsafe contract flag: ' + key);
  }

  return {
    overlayPath,
    overlaySha256: overlay.sha256,
    touchedPaths: actualTouched,
  };
}

function runGit(engineRoot, args) {
  return execFileSync('git', args, {
    cwd: engineRoot,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim();
}

function requireMarker(engineRoot, relativePath, marker) {
  const text = readFileSync(path.join(engineRoot, relativePath), 'utf8');
  invariant(
    text.includes(marker),
    relativePath + ' is missing required contract marker: ' + marker,
  );
}

export function verifyPatchedEngineMarkers(engineRoot) {
  requireMarker(
    engineRoot,
    'groups/main/CLAUDE.md',
    'Bob is the only public assistant identity.',
  );
  requireMarker(
    engineRoot,
    'groups/main/CLAUDE.md',
    'must not finalize a purchase without the explicit approval code',
  );
  requireMarker(
    engineRoot,
    'src/assistant-routing.ts',
    'matched approval-gated external message intent',
  );
  requireMarker(
    engineRoot,
    'src/assistant-routing.ts',
    'unless the user explicitly addresses @openclaw',
  );
  requireMarker(
    engineRoot,
    'src/command-surface-registry.ts',
    'texts (sends need your yes)',
  );
  requireMarker(
    engineRoot,
    'src/command-surface-registry.ts',
    'Andrea runs messaging under the hood.',
  );
  requireMarker(
    engineRoot,
    'src/channels/bluebubbles.ts',
    'BlueBubbles outbound send is disabled.',
  );
  requireMarker(
    engineRoot,
    'src/channels/bluebubbles.ts',
    'require an exact approval-bound 1:1 message action',
  );
  requireMarker(engineRoot, 'src/channels/telegram.ts', 'deleteMyCommands');
  requireMarker(
    engineRoot,
    'src/channels/telegram.ts',
    'Texts stay unsent until you say send it.',
  );
  requireMarker(
    engineRoot,
    'src/channels/telegram.ts',
    'texts (sends need your yes)',
  );
  requireMarker(engineRoot, 'src/config.ts', 'TELEGRAM_NATURAL_UX');
}

export function verifyEngineContract({ root, engineRoot, apply = false }) {
  const contract = readContract(root);
  const staticReport = verifyStaticContract({ root, contract });
  const resolvedEngine = path.resolve(engineRoot);
  invariant(statSync(resolvedEngine).isDirectory(), 'engine path is not a directory');
  invariant(
    runGit(resolvedEngine, ['rev-parse', 'HEAD']) === contract.engine.baseCommit,
    'engine checkout is not at the pinned base commit',
  );
  invariant(
    runGit(resolvedEngine, ['status', '--porcelain=v1']) === '',
    'engine checkout must be clean before verification',
  );

  runGit(resolvedEngine, [
    'apply',
    '--check',
    '--whitespace=error-all',
    staticReport.overlayPath,
  ]);
  if (!apply) {
    return {
      ...staticReport,
      engineBase: contract.engine.baseCommit,
      applied: false,
    };
  }

  runGit(resolvedEngine, [
    'apply',
    '--index',
    '--whitespace=error-all',
    staticReport.overlayPath,
  ]);
  const resultTree = runGit(resolvedEngine, ['write-tree']);
  invariant(
    resultTree === contract.overlay.expectedResultTree,
    'patched engine tree does not match the reviewed result',
  );
  verifyPatchedEngineMarkers(resolvedEngine);

  return {
    ...staticReport,
    engineBase: contract.engine.baseCommit,
    resultTree,
    applied: true,
  };
}
