---
name: atualizar
description: Traz a main para dentro da branch do designer por merge, antes que ela fique velha demais. Use quando alguém pedir para atualizar ou sincronizar a branch, "pegar o que o time subiu", quando um push for recusado por estar atrás, ou quando uma branch estiver aberta há vários dias.
---

# Atualizar a branch

Preventivo do `socorro`: a maioria dos conflitos vem de branch que ficou velha.

Fale em português.

## Passo 1 — situar

`git fetch origin` e `git rev-list --left-right --count origin/main...HEAD`.

Diga em português quanto a branch está atrás e há quanto tempo ela nasceu. Se estiver
em dia, diga isso e pare — não faça merge à toa.

## Passo 2 — mostrar o que vem

Liste os commits da `main` que ainda não estão aqui (`git log HEAD..origin/main
--oneline`), traduzidos para o que mudou de verdade. Se algum tocar nos mesmos arquivos
que a pessoa está mexendo, avise que é ali que pode dar conflito.

## Passo 3 — árvore limpa

Se houver alteração não gravada, ofereça `salvar` antes. Não faça merge por cima de
trabalho solto.

## Passo 4 — merge

`git merge origin/main`. **Merge sempre. `rebase` nunca** — é onde designer mais perde
trabalho, porque o conflito volta commit a commit.

Se der conflito, entregue direto para a skill `socorro`, caso 1.

## Termina com

"Sua branch está em dia com a main." Se houve merge, diga em uma linha o que entrou.
