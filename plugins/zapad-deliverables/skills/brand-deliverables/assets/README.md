# Assets

## Arquivos de marca da Zapad

Dois arquivos precisam estar aqui. Enquanto faltarem, `scripts/inline_assets.py`
cai para um fallback e avisa no stderr — o material funciona, mas não fica
idêntico ao padrão.

| Arquivo | O que é | Fallback |
|---|---|---|
| `zapad-logo.png` | Wordmark roxo sobre branco, 600×279 | pixel transparente (o recorte fica vazio) |
| `mesh.jpg` | Fundo roxo da capa e do card, 2884×2000 | gradiente SVG aproximado |

## Origem, e como reextrair

Os dois vieram de um deck Zapad exportado em PDF, recuperados com `poppler`
(`pdfimages`, `pdftoppm`). Se um dia se perderem, dá para refazer a partir de
qualquer apresentação da Zapad em PDF — mas com um cuidado que custa tempo se
for descoberto do jeito errado:

**`pdfimages` devolve o slide achatado, não o fundo.** A imagem embutida inclui
as margens brancas, os recortes de canto e os logos já compostos. Usar isso como
`mesh.jpg` coloca faixas brancas no material, que sob o véu escuro do card viram
manchas cinza difíceis de diagnosticar.

O caminho certo é renderizar a página e recortar só o interior do painel:

```bash
# 1. renderize a página em baixa resolução e ache o maior retângulo sem
#    pixel claro (luminância < 150), expandindo a partir do centro
pdftoppm -r 150 -f 1 -l 1 -png deck.pdf p150

# 2. recorte essa região a 600 DPI e confirme que não sobrou branco
pdftoppm -r 600 -f 1 -l 1 -x <X> -y <Y> -W <W> -H <H> -png deck.pdf mesh
```

Sempre **verifique** o recorte varrendo o pixel mais claro antes de aceitar.
Estimar as coordenadas olhando a imagem erra, e o erro só aparece depois, no
material renderizado.

O logo é vetorial no PDF, então não sai em `pdfimages` — ele é recortado do
render em alta resolução. Vem com fundo branco, o que é irrelevante: capa e card
colocam o logo dentro de um recorte branco de qualquer forma.

**Qualidade mínima do logo:** pelo menos 400px de largura, ou SVG. Abaixo de
~200px ele borra em tela retina, e o borrão aparece justo na capa. Se só houver
uma versão pequena, peça a original antes de finalizar.

**O mesh** é um JPEG de gradiente borrado. JPEG comprime gradiente muito melhor
que PNG — em torno de 40 KB contra 280 KB para a mesma imagem. Como ele vira
data URI dentro do HTML, esse tamanho entra direto no peso do arquivo final.

## Logo do cliente

Não mora aqui. É pedido a cada projeto e tratado como arquivo de sessão, porque
é material de terceiro e muda em toda entrega.

Logo de cliente quase sempre chega sem transparência, com fundo branco sólido.
Por isso capa e card colocam o logo dentro de um recorte branco — resolve o
problema e é o padrão da marca de qualquer forma.

## Templates

`deck.template.html`, `email.template.html` e `card.template.html` usam
marcadores `__NOME__` para conteúdo e para as imagens. Copie o template, preencha
o conteúdo, e rode `inline_assets.py` para trocar `__MESH__`, `__ZAPAD__` e
`__CLIENTE__` pelos data URIs.

Os marcadores de conteúdo (`__TITULO__`, `__NUMERO__`, …) são substituídos à mão
na edição — o script só cuida das imagens.
