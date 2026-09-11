# Os seis casos

Procedimento por caso. Leia só a seção do caso classificado.

Em todos: explique antes, confirme, crie salvaguarda, execute, diga onde o trabalho ficou.

---

## 1. Conflito no meio de um merge ou pull

**Sinais:** `.git/MERGE_HEAD` existe; `git status` lista "both modified".

**Como explicar:** duas pessoas mexeram na mesma linha do mesmo arquivo e o git parou
para alguém decidir qual versão vale. Nada foi perdido — as duas versões estão ali.

**Procedimento:**

1. Liste os arquivos em conflito e, para cada um, mostre os dois lados em português:
   "a sua versão" e "a versão que veio do time", com o trecho de cada.
2. Para arquivo de código ou estilo, proponha a resolução que preserva as duas
   intenções quando forem compatíveis. Diga qual escolha está fazendo e por quê.
3. Se o conflito for em `pnpm-lock.yaml` ou `package-lock.json`, resolva regerando:
   aceite a versão da `main` e rode a instalação de novo.
4. Se for em binário (imagem, fonte), pergunte qual das duas fica — não decida.
5. `git add` nos resolvidos e `git commit` com a mensagem de merge padrão.

**Se travar:** `git merge --abort` devolve tudo ao estado anterior sem perder nada.
Essa é a saída segura, e pode ser oferecida a qualquer momento.

---

## 2. Commitou direto na main

**Sinais:** branch atual é `main`, com commits que não estão em `origin/main`.

**Como explicar:** o trabalho está salvo, só está no lugar errado. Vai ser movido para
uma branch própria e a main volta ao que era.

**Procedimento:**

1. Conte quantos commits estão à frente e mostre as mensagens.
2. Crie a branch a partir de onde está: `git branch feat/<nome>`.
3. Volte a main para o remoto **sem descartar nada**: `git reset --keep origin/main`.
   `--keep` recusa a operação se houver alteração não salva, em vez de destruí-la.
4. `git checkout feat/<nome>` e confirme que os commits estão lá.

**Nunca** use `reset --hard` aqui.

---

## 3. Alteração solta travando a atualização

**Sinais:** checkout ou pull recusado com "your local changes would be overwritten".

**Como explicar:** existe trabalho não gravado que seria sobrescrito, e o git parou
para proteger.

**Procedimento:**

1. Liste em português o que está solto, pelo efeito visível.
2. Ofereça: gravar agora (chame a skill `salvar`), ou guardar com
   `git stash push -u -m "antes de atualizar"`.
3. Faça a atualização.
4. Se guardou, avise que existe trabalho no stash e devolva com `git stash pop`
   assim que der. **Nunca deixe a pessoa sair da conversa com stash esquecido.**

---

## 4. Branch desatualizada, push recusado

**Sinais:** push rejeitado, "behind"; `rev-list` mostra commits atrás.

**Como explicar:** o time subiu coisa nova desde que ela começou, e o git quer que ela
incorpore isso antes de enviar.

**Procedimento:** encaminhe para a skill `atualizar` (merge, nunca rebase) e volte ao
push depois. Se o merge der conflito, é o caso 1.

---

## 5. "Sumiu meu trabalho"

Quase nunca sumiu. Procure nesta ordem e pare no primeiro que achar.

1. **Outra branch** — `git branch -a` e `git log --all --oneline -20`. É a causa mais
   comum: a pessoa trocou de branch e não percebeu.
2. **Stash** — `git stash list`. Mostre o conteúdo com `git stash show -p` antes de
   devolver.
3. **Commit fora de branch** — `git reflog -30`. Se achar, crie uma branch de resgate
   apontando para aquele ponto: `git branch resgate/<data> <sha>`. Não faça checkout
   direto no sha.
4. **Nunca foi gravado** — se nada disso encontrar, o trabalho não chegou a virar
   commit. Diga isso com clareza, sem rodeio e sem culpar. Explique que `salvar` de
   hora em hora é o que evita isso, e siga em frente.

---

## 6. Arquivo indevido no histórico

Separe por gravidade antes de qualquer coisa.

### Segredo (`.env`, token, chave)

**Pare.** Não tente limpar.

Diga, nesta ordem: a chave precisa ser **trocada** — apagar do histórico não desvaza
nada, porque o valor já saiu da máquina. Depois, acrescente ao `.gitignore` e remova do
rastreamento (`git rm --cached`) para não repetir. Então escale para o Discord com
urgência marcada.

### Binário grande ou arquivo de design

Sem urgência. Não reescreva histórico por isso — nestes repositórios de protótipo o
custo é só peso.

1. `git rm --cached <arquivo>` e acrescente ao `.gitignore`.
2. Commite a remoção.
3. Explique que o arquivo continua no histórico antigo, que isso é normal, e que só
   pesa um pouco no clone.
