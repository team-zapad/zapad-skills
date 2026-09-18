#!/usr/bin/env bash
# Renderiza um HTML de dimensão fixa para PNG via Chrome headless.
#
#   render_png.sh card.html card.png [largura] [altura]
#
# Padrão 1080x1350 (4:5), o formato que o WhatsApp exibe maior na conversa.
# O CSS do card deve declarar a mesma dimensão em html, body — com
# --force-device-scale-factor=1 o pixel do CSS é o pixel do PNG.

set -euo pipefail

ENTRADA="${1:?uso: render_png.sh entrada.html saida.png [largura] [altura]}"
SAIDA="${2:?uso: render_png.sh entrada.html saida.png [largura] [altura]}"
LARGURA="${3:-1080}"
ALTURA="${4:-1350}"

CHROME="${CHROME_BIN:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
if [ ! -x "$CHROME" ]; then
  CHROME="$(command -v google-chrome || command -v chromium || command -v chromium-browser || true)"
fi
if [ -z "$CHROME" ] || [ ! -x "$CHROME" ]; then
  echo "Chrome não encontrado. Defina CHROME_BIN com o caminho do executável." >&2
  exit 1
fi

# Caminho absoluto: file:// relativo não resolve as imagens vizinhas.
case "$ENTRADA" in
  /*) URL="file://$ENTRADA" ;;
  *)  URL="file://$(cd "$(dirname "$ENTRADA")" && pwd)/$(basename "$ENTRADA")" ;;
esac

# virtual-time-budget dá tempo da fonte do Google Fonts chegar antes do print;
# sem isso o PNG sai com a fonte de fallback.
"$CHROME" \
  --headless=new \
  --disable-gpu \
  --hide-scrollbars \
  --force-device-scale-factor=1 \
  --window-size="${LARGURA},${ALTURA}" \
  --virtual-time-budget=6000 \
  --screenshot="$SAIDA" \
  "$URL" 2>/dev/null

if [ ! -f "$SAIDA" ]; then
  echo "falhou: $SAIDA não foi gerado" >&2
  exit 1
fi

python3 - "$SAIDA" <<'PY'
import struct, sys, pathlib
p = pathlib.Path(sys.argv[1])
d = p.read_bytes()
w, h = struct.unpack('>II', d[16:24])
print(f"{p} · {w}x{h} · {len(d)/1024:.1f} KB")
PY
