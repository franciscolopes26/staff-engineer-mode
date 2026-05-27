#!/usr/bin/env bash
# find-callers.sh — Phase 1 helper.
#
# Usage:  scripts/find-callers.sh <symbol> [path]
#
# Finds callers of <symbol> using ripgrep (preferred) or grep.
# Excludes definition sites (best-effort) and common noise dirs.
# Prints: file:line:context — one row per call site.
#
# Why this script exists:
# Phase 1 (UNDERSTAND) demands reading callers before changing code.
# Doing this consistently — across all languages, excluding the
# definition, ignoring node_modules / dist / .git — is fiddly enough
# that a paste-able command is worth more than re-typing the regex
# every time.

set -euo pipefail

SYMBOL="${1:-}"
ROOT="${2:-.}"

if [ -z "$SYMBOL" ]; then
  echo "usage: $0 <symbol> [path]" >&2
  echo "example: $0 getActiveUsers src/" >&2
  exit 64
fi

# Excludes that almost always reduce noise.
EXCLUDES=(
  --glob '!node_modules/**'
  --glob '!dist/**'
  --glob '!build/**'
  --glob '!.next/**'
  --glob '!target/**'
  --glob '!vendor/**'
  --glob '!.git/**'
  --glob '!coverage/**'
  --glob '!.nyc_output/**'
  --glob '!.pytest_cache/**'
  --glob '!__pycache__/**'
  --glob '!.tox/**'
  --glob '!venv/**'
  --glob '!.venv/**'
  --glob '!*.lock'
  --glob '!*.lockb'
  --glob '!pnpm-lock.yaml'
  --glob '!package-lock.json'
  --glob '!yarn.lock'
  --glob '!Cargo.lock'
  --glob '!Pipfile.lock'
  --glob '!poetry.lock'
  --glob '!go.sum'
  --glob '!*.min.js'
  --glob '!*.bundle.js'
  --glob '!*.html'
  --glob '!*.htm'
)

if command -v rg >/dev/null 2>&1; then
  # Word boundary + line context. -n = line numbers, -H = filename, --no-heading for grep-style output.
  rg --no-heading -n -H "${EXCLUDES[@]}" -w -- "$SYMBOL" "$ROOT" \
    | grep -Ev '(function|class|def|const|let|var|fn|impl|type|interface|public|private|protected|export[[:space:]]+default|export[[:space:]]+(function|class|const|let|var))[[:space:]]+'"$SYMBOL"'\b' \
    || { echo "no callers found for '$SYMBOL' under '$ROOT'"; exit 1; }
else
  echo "(ripgrep not found; falling back to grep — install rg for speed and better filtering)" >&2
  grep -RIn \
    --exclude-dir={node_modules,dist,build,.next,target,vendor,.git,coverage,.nyc_output,.pytest_cache,__pycache__,.tox,venv,.venv} \
    --exclude='*.html' --exclude='*.htm' --exclude='*.min.js' --exclude='*.bundle.js' \
    --exclude='*.lock' --exclude='*.lockb' --exclude='*-lock.json' \
    --exclude='package-lock.json' --exclude='pnpm-lock.yaml' --exclude='yarn.lock' \
    --exclude='Cargo.lock' --exclude='Pipfile.lock' --exclude='poetry.lock' --exclude='go.sum' \
    -w -- "$SYMBOL" "$ROOT" \
    | grep -Ev '(function|class|def|const|let|var|fn|impl|type|interface|public|private|protected|export[[:space:]]+default|export[[:space:]]+(function|class|const|let|var))[[:space:]]+'"$SYMBOL"'\b' \
    || { echo "no callers found for '$SYMBOL' under '$ROOT'"; exit 1; }
fi
