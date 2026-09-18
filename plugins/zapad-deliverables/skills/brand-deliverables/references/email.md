# E-mail

Comece de `assets/email.template.html`. A página tem duas camadas: o **bloco copiável** (`#bloco`) e a moldura ao redor com o botão de copiar. Só o bloco vai para o e-mail.

## A restrição que define tudo

Cliente de e-mail descarta `<style>`, não carrega fonte externa, bloqueia imagem por padrão e quebra flex/grid. O que sobrevive a um ctrl+C numa página renderizada e um ctrl+V no Gmail é **tabela com estilo inline**.

Por isso o bloco não usa nenhuma classe. Cada regra fica no atributo `style` do próprio elemento, e o `<style>` da página estiliza apenas a moldura e o botão — coisas que ficam de fora da cópia.

## Regras do bloco

- `max-width: 600px`. É o padrão de e-mail e evita linha longa demais no desktop.
- Layout só com `<table role="presentation" cellpadding="0" cellspacing="0" border="0">`.
- Fundo colorido em **dois lugares**: o atributo `bgcolor="#7C3AED"` e o `style="background-color:#7C3AED"`. Outlook ignora um, Gmail ignora o outro.
- Fonte: `Urbanist, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif`. Urbanist não vai carregar, mas quem tiver instalado ganha; o resto cai numa pilha decente.
- Sem imagem. Sem logo. O destinatário veria um placeholder quebrado até clicar em "exibir imagens", o que é pior que não ter.
- Barras são células de tabela com largura percentual — é assim que se faz gráfico sem imagem:

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"
       style="border-collapse:collapse;background-color:#EDE6FC;border-radius:4px;">
  <tr>
    <td width="97.8%" bgcolor="#7C3AED" style="background-color:#7C3AED;border-radius:4px;height:22px;
        font-size:11px;font-weight:700;color:#ffffff;text-align:right;padding:4px 8px;">1.706</td>
    <td width="2.2%" bgcolor="#B8860B" style="background-color:#B8860B;border-radius:4px;height:22px;
        font-size:0;line-height:22px;">&nbsp;</td>
  </tr>
</table>
```

Célula vazia precisa de `&nbsp;` com `font-size:0` — sem isso alguns clientes colapsam a célula e a barra some.

- Espaçador é `<td>` com `padding`, nunca `margin`. Margem em e-mail é loteria.
- Régua é `<div style="height:1px;background-color:#E4DCF3;font-size:0;line-height:1px;">&nbsp;</div>`.

## Cor no texto

Não use roxo em negrito no meio de um parágrafo. Em e-mail, texto colorido e destacado lê como link, e o leitor clica em nada. Roxo fica nos números de destaque isolados, nas barras e nos elementos de interface. Ênfase dentro de frase é negrito em `--tinta`.

## Botão de copiar

Fica fora do `#bloco`, senão ele vai junto para o e-mail. Copia `outerHTML` como `text/html` mais `innerText` como `text/plain`, para o caso de o destino não aceitar formatação:

```js
navigator.clipboard.write([new ClipboardItem({
  'text/html':  new Blob([bloco.outerHTML], { type: 'text/html' }),
  'text/plain': new Blob([bloco.innerText], { type: 'text/plain' })
})])
```

`ClipboardItem` exige contexto seguro e gesto do usuário — ambos existem num artefato publicado clicado por uma pessoa. Sempre inclua o fallback de selecionar o range e pedir Cmd+C, porque a API falha em alguns navegadores e o usuário não pode ficar sem saída.

## Link para o deck

Se o e-mail aponta para a apresentação, lembre que artefato nasce privado. Avise que o link só abre para o destinatário depois de compartilhar pelo menu do artefato — senão a pessoa manda o e-mail e o cliente recebe uma porta fechada.
