---
name: socorro
description: Diagnostica e resolve problema de git ou de remoto para quem não domina git — lê o estado real, classifica em um dos seis casos comuns e propõe uma correção segura em português. Use quando o designer disser "deu ruim", "socorro", "me ajuda", "sumiu meu trabalho", "perdi tudo", "não consigo dar push", "deu conflito", "acho que quebrei alguma coisa", e sempre que um comando de git falhar de um jeito que a pessoa não vai conseguir interpretar sozinha.
---

# Socorro

Uma porta só para quando deu errado. Quem está travado **não sabe qual é o problema** —
descobrir isso é o trabalho desta skill, não do designer.

Fale em português, sempre. Nunca devolva saída crua de git como resposta.

## Passo 1 — ler o estado, sem tocar em nada

Rode, nesta ordem, e só leitura:

```
git branch --show-current
git status --short --branch
git log --oneline -8
git stash list
git rev-list --left-right --count origin/main...HEAD
```

Se houver sinal de operação em andamento, verifique também
`git rev-parse --verify MERGE_HEAD` e a existência de `.git/MERGE_HEAD`.

Não execute nada que escreva antes de ter classificado.

## Passo 2 — classificar

Encaixe em **um** dos seis casos. O procedimento completo de cada um está em
`references/casos.md` — leia a seção correspondente antes de agir.

| # | Sinal | Caso |
|---|---|---|
| 1 | `MERGE_HEAD` existe, arquivos em conflito | Conflito no meio de um merge ou pull |
| 2 | branch atual é `main` e há commits locais | Commitou direto na main |
| 3 | árvore suja bloqueando checkout ou pull | Alteração solta travando a atualização |
| 4 | push recusado, HEAD atrás do remoto | Branch desatualizada |
| 5 | "sumiu meu trabalho" | Está em outra branch, no stash ou no reflog |
| 6 | arquivo indevido no histórico | Segredo, binário grande ou `.fig` commitado |

Se não encaixar em nenhum, vá para o passo 5.

## Passo 3 — explicar antes de agir

Diga, em três partes curtas:

1. **o que aconteceu**, em português e sem jargão
2. **onde o trabalho dela está agora** — quase sempre a pergunta real por trás do pedido
3. **o que você propõe fazer**, com o que muda e o que se perde

Uma correção só. Não ofereça um menu de alternativas para quem pediu socorro.

## Passo 4 — executar depois do ok

Só depois da confirmação. Antes de qualquer passo que mexa em arquivos, crie uma
salvaguarda: `git stash push -u -m "socorro-<data>"` ou uma branch de resgate
`git branch resgate/<data>`. Diga que ela existe e como voltar.

## Passo 5 — quando não souber

Não chute. Monte a mensagem para o Discord com:

- o que a pessoa estava tentando fazer, em uma linha
- o que aconteceu, em português
- um bloco de código com branch atual, `git status --short`, `git log --oneline -5` e
  o erro cru

Diga que ela pode colar como está.

## Proibido, sem exceção

`reset --hard` · `push --force` · `branch -D` · `checkout`/`restore` que descarte
alteração · `rebase` · qualquer reescrita de histórico.

Se a única saída conhecida for uma dessas, o caso é o passo 5.

## Segredo já enviado

Caso 6 com credencial: **pare**. Deixe claro que reescrever histórico não desvaza nada e
que a chave precisa ser trocada. Escale com urgência. Não tente limpar.

## Termina com

O que foi feito e **onde o trabalho está agora**. Sempre nessa ordem.
