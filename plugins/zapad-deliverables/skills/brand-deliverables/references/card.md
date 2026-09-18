# Card de imagem

Comece de `assets/card.template.html`. É uma página de dimensão fixa renderizada para PNG por `scripts/render_png.sh`.

## Formatos

| Uso | Tamanho | Por quê |
|---|---|---|
| WhatsApp, feed | **1080 × 1350** (4:5) | Ocupa mais altura na conversa; é o padrão que aparece maior |
| Status, story | 1080 × 1920 (9:16) | Tela cheia no mobile |
| Quadrado | 1080 × 1080 | Quando o corte do 4:5 atrapalha |

```bash
scripts/render_png.sh card.html card.png 1080 1350
```

O script usa Chrome headless com `--force-device-scale-factor=1`, então o CSS é escrito em pixels reais: `width:1080px` no `html, body` corresponde 1:1 ao PNG.

## Legibilidade sob compressão

WhatsApp recomprime com agressividade. O que sobrevive:

- **Nada abaixo de ~21px** numa arte de 1080 de largura. É o piso testado; abaixo disso o rótulo cinza suja primeiro.
- Número principal entre 80 e 95px, título entre 96 e 110px.
- Peso 700/800 no que precisa ser lido. Peso 400 em cinza claro some.
- Contraste alto. Texto branco sobre o mesh escuro funciona; cinza médio sobre roxo médio não.

## Composição

Fundo é `mesh.jpg` com um véu em gradiente por cima, que escurece topo e base o suficiente para o texto branco firmar sem apagar o roxo do meio:

```css
background: linear-gradient(180deg, rgba(12,0,22,.46) 0%, rgba(12,0,22,.14) 40%, rgba(12,0,22,.66) 100%);
```

O corpo é flex column com `justify-content: space-between` e padding generoso, o que distribui os blocos pela altura toda em vez de amontoar tudo embaixo. Quatro blocos é o limite confortável em 4:5: título, números, gráfico, fecho.

Linhas de estatística usam o mesmo grid de 3×3 do deck — rótulo, número e legenda em linhas próprias — porque com flex um rótulo que quebra desalinha só aquela coluna.

## Marca no card

O template vem **sem os recortes de marca**, porque card sem logo circula melhor quando o conteúdo é o produto — foi o formato que ficou de pé na prática. Sem logo, a **legenda de cores no gráfico vira obrigatória**: nada mais dá contexto de que roxo é uma coisa e ouro é outra.

Para ligar a marca, descomente as duas linhas `.chip` no markup **e** troque o `padding-top` de `.corpo` de 92px para 210px. Sem esse ajuste os recortes cobrem o título — `.corpo` é `inset:0` e começa no topo do card, ao contrário da capa do deck, onde o conteúdo é centralizado e não colide.

Os `img` dos recortes têm `max-height` de propósito. Um asset faltando vira placeholder de proporção qualquer, e sem o limite ele estufa o recorte num bloco branco que engole metade da arte.

## Entrega

Renderize e salve num lugar que a pessoa ache: `~/Downloads/` é o natural para um arquivo que vai ser anexado em seguida. Confira o PNG antes de entregar — erro de alinhamento aparece na imagem, não no HTML.

Mande junto uma versão em texto com a formatação nativa do WhatsApp (`*negrito*`), porque muita gente encaminha só o texto:

```
*Título curto*

• *2.804* pedidos automáticos
• *−97,5%* de trabalho manual

Uma frase de contexto que não dependa da imagem.
```

O texto tem que se sustentar sozinho. A imagem é reforço.
