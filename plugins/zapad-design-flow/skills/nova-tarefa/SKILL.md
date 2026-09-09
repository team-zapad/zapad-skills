---
name: nova-tarefa
description: Abre uma branch de trabalho limpa a partir da main atualizada, seguindo a convenção da Zapad. Use quando o designer for começar uma tarefa nova, pedir uma branch, disser "vou mexer em X", "começar uma alteração", ou quando ele estiver prestes a editar arquivos estando na main.
---

# Começar uma tarefa

Uma tarefa é uma branch. Esta skill garante que ela nasce de uma `main` em dia e com
o nome certo.

Fale em português. O nome da branch é em inglês.

## Passo 1 — o estado atual

Rode `git status --short` e `git branch --show-current`.

**Se houver alteração não gravada**, liste em português o que mudou — pelo efeito
visível, não só o caminho dos arquivos — e ofereça três saídas:

1. **Levar junto** para a branch nova (o padrão quando o trabalho é do mesmo assunto)
2. **Guardar para depois** com `git stash push -m`, e avise em uma frase onde isso
   ficou e como voltar
3. **Parar**, se a pessoa não reconhecer o que está ali

Não escolha por ela. Nada acontece sem resposta.

## Passo 2 — main em dia

`git checkout main` e `git pull`. Se o pull der conflito, mande para a skill `socorro`.

## Passo 3 — criar a branch

Derive o nome da descrição da tarefa:

- prefixo: `feat/` para tela ou funcionalidade nova, `fix/` para correção,
  `chore/` para ajuste de projeto
- descrição curta em **inglês**, kebab-case

`git checkout -b feat/side-menu`

Mostre o nome escolhido e a tradução ("essa branch é a sua via para mexer no menu
lateral") antes de criar.

## Travas

- Nunca deixe a pessoa trabalhar direto na `main`.
- Nunca descarte alteração não gravada.
- Se a branch já existir, ofereça entrar nela em vez de criar outra com sufixo.

## Termina com

"Você está na branch `feat/side-menu`, criada a partir da main de hoje." Diga que a
partir daqui ela pode mexer à vontade, e que `salvar` grava cada pedaço pronto.
