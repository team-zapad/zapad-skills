---
name: preparar-entrega
description: Transforma um protótipo aprovado em insumo para o desenvolvimento — separa componente reaproveitável de atalho de protótipo e escreve o resumo técnico da entrega. Use quando o protótipo for aprovado, quando alguém pedir para entregar, passar para o dev, fazer o handoff, ou documentar o que dá para reaproveitar do protótipo.
---

# Preparar a entrega

O protótipo aprovado vira insumo para o dev, não só referência visual. O dev vai
**reaproveitar componentes** — esta skill diz quais valem a pena.

Fale em português com o designer. O documento entregue é em inglês.

## Passo 1 — ler o projeto

Percorra `src/components` e `src/screens`. Para cada componente, decida em qual balde
ele cai:

- **Reaproveitável** — lógica contida, props claras, sem dado fixo no meio, sem
  dependência de outra tela. Porta para o projeto real com pouco ajuste.
- **Atalho de protótipo** — dado fixo embutido, estado global improvisado, medida em
  pixel cravada, tratamento de erro ausente, cópia de outro componente com uma
  diferença. Serve como referência visual, não como código.

Seja honesto no segundo balde. Um protótipo é feito para ser rápido, e marcar tudo
como aproveitável destrói a utilidade do documento.

## Passo 2 — o que precisa sobreviver

Registre as decisões visuais que o dev não tem como adivinhar do código: escala de
espaçamento, hierarquia de tipografia, estados de interação, comportamento em telas
estreitas, e qualquer animação que carregue significado.

## Passo 3 — escrever o documento

Crie `HANDOFF.md` na raiz do projeto, em **inglês**, com:

1. **What this prototype is** — uma frase, e o link de preview
2. **Reusable components** — tabela com caminho, o que faz e o que ajustar ao portar
3. **Prototype shortcuts** — o que foi atalho e por quê, para ninguém copiar por engano
4. **Visual decisions that matter** — o do passo 2
5. **Dependencies added** — o que entrou além do stack base e para quê

Lembre que o stack do protótipo (Vite + React + Tailwind) é mais leve que o de
produção. Aponte onde a diferença vai exigir tradução, sem transformar isso em defeito.

## Passo 4 — entregar

Commite o `HANDOFF.md` e, se houver branch aberta, mande para `mandar-pro-time`.

## Termina com

O caminho do documento e uma mensagem pronta em português para o Discord, dizendo que o
protótipo está pronto para desenvolvimento, com o link de preview e o do documento.
