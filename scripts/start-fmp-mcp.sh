#!/bin/zsh

set -euo pipefail

readonly keychain_service="${CODEX_FMP_KEYCHAIN_SERVICE:-role-specific-plugins-fmp}"
readonly keychain_account="${CODEX_FMP_KEYCHAIN_ACCOUNT:-${USER}}"

if ! command -v security >/dev/null 2>&1; then
  print -u2 "FMP MCP setup requires macOS Keychain's 'security' command."
  exit 1
fi

if ! command -v npx >/dev/null 2>&1; then
  print -u2 "FMP MCP setup requires Node.js and npx."
  exit 1
fi

api_key="$(
  security find-generic-password \
    -w \
    -a "${keychain_account}" \
    -s "${keychain_service}"
)" || {
  print -u2 "No FMP API key found in macOS Keychain."
  print -u2 "See .codex/config.example.toml for the setup command."
  exit 1
}

if [[ -z "${api_key}" || "${api_key}" == *[^A-Za-z0-9._~-]* ]]; then
  print -u2 "The FMP API key stored in Keychain is empty or has an unexpected format."
  exit 1
fi

readonly endpoint="https://financialmodelingprep.com/mcp?apikey=${api_key}"
unset api_key

exec npx -y mcp-remote@0.1.38 "${endpoint}" --silent
