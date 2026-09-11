---
name: configurar
description: Prepara a máquina de um designer para trabalhar com código na Zapad — verifica o Node, configura nome e email do git e autentica no GitHub. Use na primeira vez que a pessoa for mexer em código, e sempre que algo falhar por autenticação ou permissão ("pede senha", "não consigo clonar", "permission denied", "não tenho acesso ao repositório"), ou quando outra skill do zapad-design-flow parar por falta de configuração.
---

# Configurar a máquina

Roda uma vez por pessoa, por máquina. Sem isto, todas as outras skills falham com
mensagens de erro que o designer não tem como interpretar.

Fale sempre em português. Nunca despeje saída crua de terminal sem traduzir.

## Passo 1 — Node

Verifique com `node --version` e `pnpm --version`.

- Se o Node existir e for 20 ou maior, siga.
- Se faltar ou for antigo: **não instale nada por conta própria.** Diga qual é o
  problema, entregue o caminho de instalação (nodejs.org, ou `brew install node` se a
  pessoa já usar Homebrew) e pare até ela confirmar que instalou.
- Se faltar `pnpm`, ofereça `npm install -g pnpm` e execute só depois do ok.

## Passo 2 — identidade do git

Leia `git config --global user.name` e `git config --global user.email`.

Se algum estiver vazio, explique que isso é o nome que vai aparecer em cada alteração
que ela gravar, pergunte os dois valores e configure. Use o email corporativo.

## Passo 3 — GitHub

Verifique com `gh auth status`.

- Se o `gh` não existir, entregue o caminho de instalação e pare.
- Se não estiver autenticado, rode `gh auth login` e acompanhe a pessoa pelo fluxo,
  explicando cada escolha em português. Prefira autenticação por navegador.
- Autenticado: confirme o acesso à organização com `gh repo list team-zapad --limit 1`.
  Se der erro de permissão, diga que falta liberar o acesso e monte a mensagem para o
  Discord pedindo isso.

## Passo 4 — fechamento

Mostre um checklist em português com o resultado de cada item e um estado claro:

```
Node 22.11         ok
pnpm 9.12          ok
git (nome e email) ok — Ana Souza <ana@zapad.com.br>
GitHub             ok — autenticada como anasouza, com acesso a team-zapad
```

Termine com **"você está pronta"** e diga qual é o próximo comando: `novo-projeto`
para começar um protótipo, `rodar-projeto` para abrir um que já existe.

## Travas

- Não instale nada sem confirmação explícita.
- Não tente adivinhar gerenciador de pacotes do sistema.
- Se um passo falhar duas vezes, pare e monte a mensagem para o Discord em vez de
  continuar tentando variações.
