# Deck

Comece de `assets/deck.template.html`. Ele já traz os tokens, a capa, um slide de conteúdo, o encerramento, a navegação e o tooltip.

## Anatomia

Slide 16:9, card branco sobre `--chao`, radius 14px, sombra discreta. `aspect-ratio: 16/9` só acima de 920px — abaixo disso a altura volta a ser o conteúdo, senão texto estoura em celular.

```
capa (painel escuro, recortes brancos nos cantos)
conteúdo × N
encerramento (painel escuro, "Vamos construir o futuro juntos?")
```

### Slide de conteúdo

```
eyebrow            11px / 700 / uppercase / 0.13em / --tinta-3
h2                 clamp(24px, 3.3vw, 40px) / 700 / -0.022em
aside              coluna à direita, 13.5–15.5px, --tinta-2   (opcional)
régua              1px --regua
conteúdo
rodapé             11.5px --tinta-3                            (opcional)
```

Cabeçalho é grid `1.55fr / 1fr` — título à esquerda, aside à direita. Sem aside, use `.s-head.solo` e o título ocupa a largura toda. Abaixo de 700px as colunas empilham.

O aside é o lugar de uma frase de contexto, não de um parágrafo. Se não couber em duas linhas, provavelmente é conteúdo do slide, não apoio.

### Capa e encerramento

Painel escuro ocupando o slide inteiro, com `mesh.jpg` em `background-size: cover` sobre `--mesh-base`. Os recortes são caixas brancas ancoradas nos cantos com radius no canto interno — logo da Zapad em cima à esquerda, logo do cliente embaixo à direita. No encerramento, a Zapad vai para o canto de baixo.

O padding dos recortes precisa ser folgado nos quatro lados. Com padding só em dois lados o conteúdo encosta na borda do slide e o `overflow:hidden` corta — é o erro mais fácil de cometer aqui.

### Caixas

```html
<div class="caixa destaque">   <!-- borda --roxo-borda, para o que importa -->
<div class="caixa">            <!-- borda --caixa-borda, secundária -->
<div class="destaque-largo">   <!-- faixa de largura total, título roxo + corpo -->
```

`destaque-largo` no fim do slide é o padrão para "a conclusão deste slide". Uma por slide, no máximo.

## Gráficos

Barras são div com largura percentual dentro de um trilho `--roxo-pale`. Sem biblioteca — o volume de dados de um deck não justifica uma.

```html
<div class="linha">
  <span class="chave">ago</span>
  <div class="trilho">
    <div class="seg auto" style="width:89.18%" data-tip="Agosto · 1.706 automáticos (97,8%)">
      <span class="seg-lab">1.706</span>
    </div>
    <div class="seg manual" style="width:2.04%" data-tip="Agosto · 39 à mão (2,2%)"></div>
  </div>
  <span class="valor">1.745<span class="q">97,8% auto</span></span>
</div>
```

Regras que evitam gráfico errado:

- **Uma escala por gráfico.** Todos os segmentos são percentual do mesmo máximo, e o rodapé diz qual é: "barra cheia = 1.913 pedidos". Duas medidas de grandeza diferente exigem dois gráficos com escalas declaradas como independentes, nunca dois eixos.
- **Gap de 2px entre segmentos** — separa visualmente sem inventar espaço na escala.
- **Rótulo só onde cabe.** Segmento estreito fica sem número; o valor aparece na coluna da direita. Abaixo de 620px, esconda todos com `.seg-lab { display:none }`.
- **Legenda sempre que houver duas séries**, com o mesmo par de cores usado no resto do deck.
- **Categorias de uma distribuição precisam ser mutuamente exclusivas.** "Mais de 1h" e "mais de 4h" se sobrepõem e somam mais que o total; o certo é 5min–1h, 1h–4h, 4h–12h.

Para uma proporção simples (um número grande tipo "98,4% chegam"), use uma faixa única em `--roxo` com o resto em `--roxo-pale`. Três cores para três estados só se validar antes.

### Linhas de estatística

Use grid de 3 colunas × 3 linhas, com rótulo, número e legenda em linhas separadas do mesmo grid. Com flex, um rótulo que quebra em duas linhas empurra o número só daquela coluna e desalinha a fileira inteira:

```css
.stats { display: grid; grid-template-columns: repeat(3, 1fr); column-gap: 34px; row-gap: 12px; align-items: end; }
```

## Navegação

`scroll-snap-type: y proximity` no `html` — dá sensação de apresentação sem prender o scroll em slide mais alto que a tela. Trilha de pontos fixa à direita, sincronizada por `IntersectionObserver` em 0.5, escondida abaixo de 860px. Setas e PageUp/PageDown movem slide a slide.

O `IntersectionObserver` só destaca o ponto ativo. Nada de conteúdo pode depender dele para aparecer: o que está no documento tem que estar visível de saída, senão a primeira impressão e a miniatura do link mostram página vazia.

## Antes de publicar

- Contagem de slides bate com a de pontos na navegação.
- Nenhuma cor da marca significa duas coisas diferentes no mesmo deck.
- Todo gráfico tem escala declarada no rodapé.
- Mês parcial ou recorte incompleto está marcado.
