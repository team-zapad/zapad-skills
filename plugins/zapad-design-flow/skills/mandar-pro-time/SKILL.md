---
name: mandar-pro-time
description: Envia a branch para o GitHub, abre o Pull Request e devolve o link de preview para o designer compartilhar. Use quando o designer disser que terminou, que quer mandar, enviar, publicar, subir, mostrar para o time, pedir revisão ou abrir um PR.
---

# Mandar para o time

Fecha o ciclo: envia, abre o PR e entrega o link que o time de fato usa — o do preview.

Fale em português. Título e corpo do PR em inglês.

## Passo 1 — confirmar o conjunto

Liste os commits que vão junto (`git log main..HEAD --oneline`) e resuma **em
português** o que a branch inteira faz. Confirme antes de enviar.

Se houver alteração ainda não gravada, ofereça rodar `salvar` antes.

## Passo 2 — enviar

`git push -u origin <branch>`.

Se o push for recusado por estar atrás da `main`, **não force nada**: mande para a
skill `atualizar` e volte aqui depois.

## Passo 3 — abrir o Pull Request

`gh pr create --base main`, com:

- **título** em inglês, no mesmo padrão dos commits
- **corpo** em inglês, com duas seções: o que mudou, e como testar (por qual tela
  entrar e o que olhar)

O PR fica **aguardando revisão**. Nunca faça o merge, nem sugira que a pessoa faça.

## Passo 4 — o link de preview

Cada push gera uma URL de preview automática. Procure-a nos checks do PR
(`gh pr checks`) ou no comentário do bot de deploy. Espere um pouco e tente de novo se
ainda não existir.

Se o repositório for só local (sem remoto), diga isso em uma linha e pare no passo 1 —
não há para onde enviar ainda.

## Termina com

Três coisas, nesta ordem:

1. o **link de preview** — é este que circula no time
2. o link do PR
3. uma mensagem pronta em português para colar no Discord, com o que mudou em uma
   frase e os dois links

## Travas

- Nunca `--force`.
- Nunca merge.
- Nunca abra o PR contra outra coisa que não a `main`.
