#!/usr/bin/env bash
# Injeta as convencoes do zapad-design-flow no inicio de toda sessao.
# Mesmo padrao do zapad-house-rules: o stdout do hook entra no contexto.
set -euo pipefail

ARQUIVO="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}/convencoes.md"

[ -f "$ARQUIVO" ] || exit 0
cat "$ARQUIVO"
