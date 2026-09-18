#!/usr/bin/env python3
"""Troca marcadores __ASSET_NOME__ por data URIs, deixando o HTML autocontido.

Uso:
    inline_assets.py entrada.src.html saida.html \
        --asset MESH=caminho/mesh.jpg \
        --asset ZAPAD=caminho/zapad-logo.png \
        --asset CLIENTE=caminho/logo-cliente.png

Mantenha o .src.html com os marcadores e edite sempre ele. O arquivo de saída
tem base64 no meio do markup — revisar ou editar isso à mão não é viável.

Se o arquivo de um asset não existir, o marcador correspondente recebe um
fallback (gradiente CSS para MESH, transparente para o resto) e o script avisa
no stderr. O deck fica utilizável, mas fora do padrão visual.
"""

import argparse
import base64
import mimetypes
import sys
from pathlib import Path

# Aproximação em CSS do fundo roxo oficial, para quando mesh.jpg não estiver disponível.
MESH_FALLBACK = (
    "data:image/svg+xml;base64,"
    + base64.b64encode(
        b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1152 766">'
        b'<defs>'
        b'<radialGradient id="a" cx="78%" cy="22%" r="62%">'
        b'<stop offset="0" stop-color="#B026C9" stop-opacity=".62"/>'
        b'<stop offset="1" stop-color="#B026C9" stop-opacity="0"/></radialGradient>'
        b'<radialGradient id="b" cx="26%" cy="78%" r="64%">'
        b'<stop offset="0" stop-color="#7C3AED" stop-opacity=".68"/>'
        b'<stop offset="1" stop-color="#7C3AED" stop-opacity="0"/></radialGradient>'
        b'<radialGradient id="c" cx="12%" cy="12%" r="70%">'
        b'<stop offset="0" stop-color="#431478" stop-opacity=".85"/>'
        b'<stop offset="1" stop-color="#431478" stop-opacity="0"/></radialGradient>'
        b'</defs>'
        b'<rect width="1152" height="766" fill="#1b0230"/>'
        b'<rect width="1152" height="766" fill="url(#c)"/>'
        b'<rect width="1152" height="766" fill="url(#b)"/>'
        b'<rect width="1152" height="766" fill="url(#a)"/>'
        b'</svg>'
    ).decode()
)

PIXEL_FALLBACK = (
    "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
)


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument(
        "--asset",
        action="append",
        default=[],
        metavar="NOME=CAMINHO",
        help="troca __NOME__ pelo data URI do arquivo; repita para cada asset",
    )
    args = ap.parse_args()

    html = Path(args.entrada).read_text(encoding="utf-8")
    faltando = []

    for par in args.asset:
        if "=" not in par:
            print(f"aviso: --asset '{par}' ignorado, formato esperado NOME=CAMINHO", file=sys.stderr)
            continue
        nome, caminho = par.split("=", 1)
        marcador = f"__{nome.strip().upper()}__"
        arquivo = Path(caminho).expanduser()

        if arquivo.is_file():
            html = html.replace(marcador, data_uri(arquivo))
        else:
            fallback = MESH_FALLBACK if "MESH" in marcador else PIXEL_FALLBACK
            html = html.replace(marcador, fallback)
            faltando.append((marcador, str(arquivo)))

    Path(args.saida).write_text(html, encoding="utf-8")

    restantes = sorted({m for m in ("__MESH__", "__ZAPAD__", "__CLIENTE__") if m in html})
    if restantes:
        print(f"aviso: marcador sem --asset correspondente: {', '.join(restantes)}", file=sys.stderr)

    for marcador, caminho in faltando:
        print(f"aviso: {marcador} usou fallback, arquivo não encontrado em {caminho}", file=sys.stderr)

    kb = Path(args.saida).stat().st_size / 1024
    print(f"{args.saida} · {kb:.1f} KB")
    return 1 if (faltando or restantes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
