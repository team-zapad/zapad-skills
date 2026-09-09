---
name: salvar
description: Grava no histórico uma ideia concluída — mostra o que mudou em português, bloqueia arquivo indevido e faz o commit no padrão da Zapad. Use quando o designer disser que quer salvar, guardar, gravar, commitar, "salvar o que fiz até aqui", ou terminar um pedaço do trabalho. Feito várias vezes por dia, não uma vez no fim.
---

# Salvar uma ideia pronta

Um commit por ideia concluída. Vários por dia.

Fale em português. A mensagem do commit é em inglês.

## Passo 1 — onde a pessoa está

Se a branch atual for `main`, **pare**. Explique que a main é a versão oficial e
ofereça criar uma branch agora (skill `nova-tarefa`) levando as alterações junto.

## Passo 2 — o que mudou

Leia `git status --short` e `git diff --stat`. Descreva em português **pelo efeito
visível**, e só depois liste os arquivos:

> Você mexeu no espaçamento do menu lateral, trocou a cor dos ícones e adicionou um
> ícone novo.
>
> `src/components/SideMenu.tsx`, `src/styles/index.css`, `public/icons/menu.svg`

## Passo 3 — a triagem

Antes de qualquer coisa, bloqueie e avise:

- `.env` ou qualquer arquivo de segredo
- `node_modules/`, `dist/`, `.vite/`, `build/`
- arquivo acima de 10 MB
- `.fig`, `.sketch`, `.psd` e outros binários de design

Se aparecer algo assim, explique por que não entra, ofereça acrescentar ao
`.gitignore`, e siga sem ele. Um `.fig` grande e um segredo têm gravidades diferentes:
o arquivo grande é chateação, o segredo é urgência — nesse caso siga o que diz a seção
de segredos das convenções.

## Passo 4 — a mensagem

Proponha uma mensagem no padrão conventional, em inglês, no imperativo:

```
feat: add side menu spacing and new icon
```

Use `feat`, `fix`, `chore`, `style` ou `refactor`. Mostre a mensagem e confirme antes
de gravar. Se o designer descreveu a tarefa em português, traduza — não peça para ele
escrever em inglês.

## Passo 5 — gravar

`git add` nos arquivos aprovados (nunca `add .` cego) e `git commit`.

## Termina com

A mensagem gravada e **quantos commits ainda não foram enviados** ao time. Se forem
três ou mais, sugira `mandar-pro-time`.
