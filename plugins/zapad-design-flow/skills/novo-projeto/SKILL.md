---
name: novo-projeto
description: Cria um protótipo de alta fidelidade novo da Zapad em Vite + React + Tailwind e o deixa rodando no navegador. Use quando o designer disser que quer começar um protótipo, criar um projeto ou um repositório novo, "montar uma tela do zero", ou iniciar um novo trabalho para um cliente.
---

# Novo protótipo

O comando mais usado do conjunto: cada protótipo é um projeto novo.

Fale sempre em português. Nome de pasta, de arquivo e de componente em inglês.

## Passo 1 — o que é

Se o designer não descreveu, pergunte em uma frase o que o protótipo vai mostrar.
Derive daí um nome em **kebab-case, em inglês** (ex: `client-portal-onboarding`) e
confirme antes de criar.

## Passo 2 — existe repositório remoto?

**Pergunte sempre.** Não crie repositório no GitHub por conta própria.

- **Existe**: peça o endereço, clone e monte o projeto dentro dele.
- **Não existe**: monte só local, com `git init` e um primeiro commit. Avise em uma
  linha que o projeto ainda está só nesta máquina, e que o deploy e o link de preview
  ficam para quando o repositório existir. Não trate isso como problema.

## Passo 3 — montar

Stack fixo, sem substituições:

```
pnpm create vite . --template react-ts
pnpm add -D tailwindcss @tailwindcss/vite
```

Estrutura padrão:

```
src/
  components/     componentes reutilizáveis
  screens/        as telas do protótipo
  lib/            utilidades
  styles/         index.css com as diretivas do Tailwind
public/
```

Configure o Tailwind pelo plugin do Vite, deixe o TypeScript em modo estrito e escreva
um `README.md` curto dizendo o que é o protótipo e como rodar.

Escreva também um `CLAUDE.md` na raiz com o stack, como rodar e onde ficam as telas e
os componentes — é o que faz as próximas sessões começarem já orientadas.

Confirme que o `.gitignore` cobre `node_modules`, `dist` e `.env`.

## Passo 4 — primeiro commit

`chore: initial commit`. Só depois de mostrar o que vai entrar.

## Passo 5 — ver funcionando

Suba com `pnpm dev` e confirme que a página respondeu de verdade antes de dizer que
está pronto. Entregue o endereço local.

## Travas

- **Nunca escreva dentro de pasta que já tem conteúdo.** Se houver, pare e proponha
  outro nome.
- Não puxe TanStack Start, Prisma, SST nem MUI: protótipo aqui é deliberadamente mais
  leve que o `zapad-js-stack`.
- Não crie repositório remoto sem pedido explícito.

## Termina com

O projeto aberto no navegador, o endereço local, e uma frase dizendo o que fazer em
seguida — normalmente `nova-tarefa` antes da primeira alteração de verdade.
