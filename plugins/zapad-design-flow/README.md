# zapad-design-flow

O fluxo de git e de projeto para os **designers** da Zapad, em português.

Nove skills que levam um designer do zero até um protótipo de alta fidelidade no ar,
sem precisar aprender git primeiro. Diferente dos outros plugins deste marketplace,
este é escrito em português: o que fica no repositório é inglês, o que fala com a
pessoa é português.

## As nove

Digite `/zapad-design-flow` para ver todas.

### Entrada

| | |
|---|---|
| `configurar` | Prepara a máquina: Node, identidade do git, autenticação no GitHub. Uma vez por pessoa. |
| `novo-projeto` | Cria um protótipo novo em Vite + React + Tailwind e o deixa rodando. |
| `rodar-projeto` | Faz um protótipo existente funcionar aqui — e escreve o `CLAUDE.md` do projeto se ainda não houver. |

### Ciclo de git

| | |
|---|---|
| `nova-tarefa` | Abre uma branch limpa a partir da main atualizada. |
| `salvar` | Grava uma ideia concluída, com triagem do que não pode entrar. Várias vezes por dia. |
| `mandar-pro-time` | Envia, abre o PR e devolve o link de preview. |
| `socorro` | Uma porta só para quando deu errado. Classifica em seis casos e propõe a correção segura. |

### Depois

| | |
|---|---|
| `atualizar` | Traz a main para dentro da branch por merge, antes que ela apodreça. |
| `preparar-entrega` | Separa componente reaproveitável de atalho de protótipo e escreve o `HANDOFF.md`. |

## A décima peça não é uma skill

`hooks/hooks.json` roda `scripts/inject-convencoes.sh` no `SessionStart` e injeta
[`convencoes.md`](convencoes.md) no contexto — mesmo padrão do `zapad-house-rules`.

As convenções valem **com ou sem comando**: quando o designer só escreve "cria uma
branch pra mim", o padrão de nome, o formato de commit e as travas de segurança
continuam valendo. As nove skills são atalho para o caminho completo, não a única porta.

O hook só afeta quem instalar este plugin. Devs não são atingidos.

## Convenções que este plugin carrega

| | |
|---|---|
| Contexto | Repositórios de protótipo de alta fidelidade. Front puro, sem `.env`, sem acesso a produção. |
| Stack | Vite + React + Tailwind, TypeScript. Deliberadamente mais leve que o `zapad-js-stack`. |
| Branch base | Sempre `main` |
| Nome de branch | `feat/` `fix/` `chore/` + kebab-case em inglês |
| Commits | Conventional commits em inglês, um por ideia concluída |
| Pull Request | Contra a `main`, título e corpo em inglês, **nunca com merge automático** |
| Sincronizar | Merge. `rebase` está fora do fluxo. |
| Confirmações | Ler roda livre; escrever, commitar ou tocar no remoto pede ok uma vez |
| Emergência | Mensagem pronta para colar no Discord, com o estado técnico junto |

## Proibido em todas as skills

`reset --hard` · `push --force` · `branch -D` · `checkout`/`restore` que descarte
alteração · `rebase` · qualquer reescrita de histórico.

Quando a única saída conhecida é uma dessas, a skill para e escala. Trabalho perdido
aqui não volta, e um designer não tem como avaliar o risco.

## Para quem mantém

O conteúdo vive em quatro lugares:

- `convencoes.md` — as regras sempre ativas. Mudou o padrão de branch ou de commit?
  É aqui, e só aqui.
- `skills/*/SKILL.md` — o procedimento de cada comando.
- `skills/socorro/references/casos.md` — o detalhe dos seis casos de socorro.
- `README.md` — este arquivo.
