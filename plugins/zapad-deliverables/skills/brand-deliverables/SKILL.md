---
name: brand-deliverables
description: Build client-facing deliverables in Zapad's visual identity — presentation decks, email-pasteable summaries, and WhatsApp/social image cards. Use this skill whenever you are producing something a Zapad client will actually see: a results deck, a status or findings presentation, a "show the impact" report, an email summary of a project, a shareable stat card, or any artifact that should carry Zapad branding. Trigger it even when the user only says "make a presentation", "turn this into a deck", "send this to the client", "put this in the Zapad standard", "versão pocket pra e-mail", or "algo pra mandar no WhatsApp" — if the audience is a client or a client's stakeholder, this skill applies. Also use it when someone asks about Zapad brand colors, fonts, or slide structure. Do not use it for internal code documentation, README files, or generic charts with no client audience.
metadata:
  version: 1.0.0
---

# Zapad Brand Deliverables

Three output formats share one identity. Pick the format from the audience, then build it from the matching template — don't start from a blank file, because the templates already encode the brand tokens, the slide anatomy, and the fixes for problems that are easy to hit and annoying to diagnose.

| Format | When | Reference |
|---|---|---|
| **Deck** | A meeting, a stakeholder read, anything that needs narrative | `references/deck.md` |
| **E-mail** | Pasted into a message body; the recipient will not click a link | `references/email.md` |
| **Card** | WhatsApp, status, social — one image, no clicking | `references/card.md` |

Read only the reference for the format you're building. They're independent.

---

## Brand tokens

Copy these verbatim. They were validated together for contrast and color-vision separation, so changing one quietly breaks the set.

```css
--roxo:        #7C3AED;  /* principal — trilha Zapad */
--roxo-medio:  #A78BFA;  /* destaque sobre fundo escuro */
--roxo-claro:  #CFC0FA;
--roxo-pale:   #EDE6FC;  /* trilho de barra, fundo de gráfico */
--roxo-borda:  #8B5CF6;  /* borda de caixa em destaque */
--roxo-escuro: #4C1D95;

--ouro:        #B8860B;  /* trilha do cliente */
--ouro-claro:  #E3CC8F;
--ouro-pale:   #F5EDD9;

--tinta:       #1A1A1F;  /* título */
--tinta-2:     #55555F;  /* corpo */
--tinta-3:     #8A8A96;  /* eyebrow, rodapé */

--regua:       #E4DCF3;  /* régua sob o cabeçalho */
--caixa-borda: #DFD9EA;  /* caixa secundária */
--branco:      #ffffff;
--chao:        #f1eff7;  /* fundo atrás dos slides */
--mesh-base:   #1b0230;  /* cor sob a imagem de fundo */
```

**Tipografia:** Urbanist, pesos 400/500/600/700/800.
`https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700;800&display=swap`

Urbanist não existe em cliente de e-mail. Ali a marca é carregada pela cor e pela estrutura — veja `references/email.md`.

### A regra de cor que importa

**Roxo = Zapad, o novo, o automático. Ouro = o cliente, o antigo, o manual.**

Essa dupla vem do próprio padrão de apresentação da Zapad, que separa trilha Zapad de trilha do cliente. Reaproveitá-la para o par "antes × depois" de qualquer análise funciona porque o significado já é o mesmo: uma cor é o que a Zapad trouxe, a outra é o estado anterior.

A cor pertence à entidade, não à posição no gráfico. Se um slide usa ouro para "manual", nenhum outro slide do mesmo deck pode usar ouro para outra coisa — em uma barra de proporção, o resto que não é a categoria principal fica em `--roxo-pale` ou cinza, nunca na outra cor da marca. Duas leituras para a mesma cor no mesmo documento é o erro que mais corrói a confiança em um gráfico.

O par `#7C3AED` + `#B8860B` passa em faixa de luminosidade, piso de croma, separação para daltonismo e contraste ≥3:1 sobre branco. Se precisar de uma terceira cor categórica, valide antes com o skill `dataviz` em vez de escolher a olho — a trinca roxo/ouro/vermelho, por exemplo, reprova em modo escuro.

---

## Assets

`assets/zapad-logo.png` e `assets/mesh.jpg` (o fundo roxo da capa) são os dois arquivos de marca. Se estiverem faltando, `scripts/inline_assets.py` avisa e cai para um gradiente CSS aproximado — o deck funciona, mas não fica idêntico ao padrão. Peça os originais.

**O logo do cliente nunca mora aqui.** Peça a cada projeto e trate como arquivo de sessão. Dois cuidados que aparecem sempre:

- Logo de cliente costuma vir sem transparência, com fundo branco sólido. Por isso a capa coloca o logo dentro de um recorte branco — resolve o problema e é o padrão da marca de qualquer jeito.
- Logo em PNG pequeno (abaixo de ~200px de largura) borra em tela retina. Peça SVG ou uma versão maior antes de finalizar.

---

## Fluxo de construção

Os templates usam marcadores `__ASSET_NOME__` no lugar das imagens. O build troca cada marcador por um data URI, o que deixa o arquivo final autocontido — sem requisição externa, sem imagem quebrada quando o cliente abre offline.

```bash
S="${CLAUDE_PLUGIN_ROOT}/skills/brand-deliverables"

cp $S/assets/deck.template.html deck.src.html
# edite deck.src.html com o conteúdo do projeto

python3 $S/scripts/inline_assets.py deck.src.html deck.html \
  --asset MESH=$S/assets/mesh.jpg \
  --asset ZAPAD=$S/assets/zapad-logo.png \
  --asset CLIENTE=./logo-do-cliente.png
```

Edite sempre o `.src.html`, nunca o arquivo com os data URIs dentro — base64 no meio do HTML é impossível de revisar e fácil de corromper.

Para gerar imagem (card, ou um slide virando PNG):

```bash
$S/scripts/render_png.sh card.html card.png 1080 1350
```

---

## Publicar

Deck e e-mail são artefatos. Card é arquivo local.

**O sandbox do artefato bloqueia download iniciado pela própria página.** Um botão "salvar PNG" fica inerte para quem abre o link, então imagem sempre é renderizada localmente com `render_png.sh` e entregue como arquivo — nunca prometa um download dentro do artefato.

Ao publicar deck e e-mail como artefatos separados, use caminhos de arquivo diferentes: republicar o mesmo caminho substitui o artefato anterior e derruba o link já compartilhado.

Antes de publicar um deck, vale renderizar e olhar uma vez — de preferência os slides com gráfico, que é onde erro de escala aparece. Para pré-visualizar local, sirva com charset explícito, senão acentuação vira mojibake e você perde tempo caçando um bug que não existe:

```bash
python3 -c "
import http.server, socketserver
class H(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, '.html':'text/html; charset=utf-8'}
socketserver.TCPServer.allow_reuse_address = True
socketserver.TCPServer(('127.0.0.1',8899), H).serve_forever()" &
```

---

## Escrita

O padrão Zapad é de consultoria: afirmação curta no título, número grande, texto mínimo. O que faz um slide funcionar é a frase do título carregar a conclusão — "A origem dos pedidos se inverteu" em vez de "Análise de origem dos pedidos". O leitor entende o slide sem ler o corpo.

Alguns hábitos que se pagam:

- Rótulo em português, na língua da operação do cliente. "Digitado à mão", não "manual input".
- Ressalva fica no rodapé cinza, não sumida. Um mês com um dia de dados marcado com asterisco preserva a credibilidade do resto.
- Quando a análise revelar que um número que você já reportou estava errado, corrija no material e diga por quê. O deck que admite "o real é 98,4%, não 95,8%" é mais forte do que o que só mostra o número bom.
- Termo técnico não sobe para o cliente. Nome de arquivo, função, coluna de banco e código HTTP viram linguagem de negócio, sempre.
