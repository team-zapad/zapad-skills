# Zapad — convenções de código para designers

Estas regras valem em toda sessão desta pessoa, com ou sem comando. As skills do
`zapad-design-flow` são atalhos para o caminho completo; estas convenções valem
também quando o designer só escreve normalmente ("cria uma branch pra mim").

## Quem está do outro lado

Um designer, trabalhando sozinho, em repositórios de **protótipo de alta fidelidade**.
Front puro, sem variáveis de ambiente, sem acesso a produção. A pessoa não domina git
e não deve precisar dominar. O pior caso possível aqui é ela perder o próprio trabalho —
não existe produção para derrubar.

## Idioma

- **O que fica no repositório é inglês**: nome de branch, mensagem de commit, título e
  corpo de Pull Request, comentário em código, nome de arquivo e de componente.
- **O que fala com a pessoa é português**: explicação, pergunta, aviso, erro, resumo do
  que mudou. Nunca despeje saída crua de git ou log de erro sem traduzir o que aconteceu.

## Git

- Branch base é sempre `main`. Nunca deixe a pessoa trabalhar direto na `main`: se ela
  estiver lá e for fazer uma alteração, ofereça criar a branch antes.
- Nome de branch: prefixo semântico em inglês (`feat/`, `fix/`, `chore/`) mais uma
  descrição curta em kebab-case, também em inglês. Ex: `feat/side-menu`.
- Commit: conventional commits em inglês, no imperativo. Ex: `feat: add side menu spacing`.
  Um commit por ideia concluída — vários por dia, não um no fim.
- Pull Request: aberto contra a `main`, título e corpo em inglês, dizendo o que mudou e
  como testar. **Nunca faça o merge** — o PR fica aguardando revisão de gente.
- Sincronizar branch é sempre **merge**. `rebase` está fora deste fluxo.

## Confirmações

Ler o estado roda livre: `status`, `log`, `diff`, `branch`, `remote`, `stash list`, `reflog`.

Tudo que **cria commit, altera arquivo ou toca no remoto** pede ok uma vez, dizendo em
português qual é o efeito. Uma confirmação clara vale mais que cinco genéricas — não
pergunte tanto que a pessoa comece a aprovar sem ler.

## Proibido, sempre

Nunca execute, nem sugira como saída fácil:

- `git reset --hard`
- `git push --force` / `--force-with-lease`
- `git branch -D`
- `git checkout` / `git restore` que descarte alteração não salva
- `git rebase` em qualquer forma
- reescrita de histórico (`filter-branch`, `filter-repo`, `commit --amend` em algo já enviado)

Se a única saída conhecida for uma dessas, **pare** e monte a mensagem para o Discord
(ver abaixo). Trabalho perdido aqui não volta, e a pessoa não tem como avaliar o risco.

## Antes de qualquer commit

Bloqueie e avise, em português, antes de gravar:

- `.env` e qualquer arquivo de segredo
- `node_modules/`, `dist/`, `.vite/`, `build/`
- arquivo acima de 10 MB
- `.fig`, `.sketch`, `.psd` e outros binários de design

Se um segredo **já foi enviado**: pare, deixe claro que reescrever histórico não desvaza
nada e que a chave precisa ser trocada, e escale para o Discord. Não tente consertar.

## Saída de emergência

Quando o problema passar do que estas skills cobrem, não improvise: monte uma mensagem
pronta para o designer colar no **Discord** do time, contendo, nesta ordem:

1. o que a pessoa estava tentando fazer, em uma linha
2. o que aconteceu, em português
3. um bloco de código com o estado técnico (branch atual, `git status --short`,
   `git log --oneline -5`, e o erro cru)

Diga que ela pode colar isso como está.

## Stack dos protótipos

Vite + React + Tailwind, TypeScript. É deliberadamente mais leve que o stack de produção
da Zapad (`zapad-js-stack`) — não puxe TanStack Start, Prisma, SST nem MUI para um
protótipo, e não trate a diferença como erro a corrigir.

## Como falar

- Nomeie as coisas pelo que a pessoa reconhece: "sua pasta", "o histórico do time",
  "a versão que você salvou" — não "working tree", "origin/main", "o objeto".
- Ao mostrar o que mudou, descreva o efeito visível ("você mexeu no espaçamento do menu
  e adicionou um ícone"), e só depois liste os arquivos.
- Erro explica o que houve e o que fazer em seguida. Sem pedido de desculpa e sem jargão.
- Termine sempre dizendo **onde o trabalho está agora** e qual é o próximo passo.
