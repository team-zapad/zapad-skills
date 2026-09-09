---
name: rodar-projeto
description: Faz um protótipo que já existe funcionar na máquina do designer — clona se preciso, instala as dependências, escreve o CLAUDE.md do projeto se ainda não houver, e sobe o servidor local. Use quando alguém pedir para abrir, rodar, clonar ou "pegar" um projeto existente, quando entrar num protótipo de outra pessoa, ou quando disser que um projeto não sobe ou parou de funcionar.
---

# Rodar um protótipo existente

Objetivo único: a pessoa vendo o projeto no navegador. Tudo aqui serve a isso.

Fale sempre em português. Nunca despeje log de erro cru.

## Passo 1 — trazer para a máquina

Se o projeto ainda não estiver aqui, clone com `gh repo clone`. Aceite tanto o nome
curto (`team-zapad/nome`) quanto a URL completa. Se falhar por autenticação, mande para
a skill `configurar`.

## Passo 2 — instalar

`pnpm install`. Se o projeto tiver `package-lock.json` em vez de `pnpm-lock.yaml`, use
`npm install` e siga — não converta o projeto.

Se a instalação falhar, **traduza o erro** e ofereça as saídas comuns em vez de
despejar o log: versão de Node incompatível, cache corrompido (`pnpm store prune`),
dependência que precisa de compilação. Duas tentativas, no máximo; depois monte a
mensagem para o Discord.

## Passo 3 — mapear o projeto

Se **não houver `CLAUDE.md`** na raiz, escreva um. Leia o projeto e registre:

- stack e versões que importam
- como rodar e em que porta
- onde ficam telas, componentes, estilos e rotas
- qualquer convenção visível no código que valha manter

Mostre o arquivo para o designer e **pergunte se pode commitar**. Se sim, commite com
`chore: add CLAUDE.md`. Assim o mapa passa a existir para o time inteiro, sem ninguém
precisar decidir isso.

Se já houver `CLAUDE.md`, leia e siga o que estiver lá.

## Passo 4 — subir

`pnpm dev` e confirme que a página carregou. Estes projetos são front puro: **não peça
variáveis de ambiente** e não trate a ausência de `.env` como problema.

## Termina com

O endereço local aberto e um resumo curto, em português, do que tem no projeto —
quantas telas, quais componentes principais, o que parece estar em construção.
