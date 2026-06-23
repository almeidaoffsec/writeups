# writeups.almeidaoffsec.com

Site de writeups — CTFs, labs e HackTheBox documentados em tempo real.

## Adicionar um writeup novo

1. Criar uma pasta em `_writeups/` com o slug do writeup:
   ```
   _writeups/htb-nome-da-maquina/
   ```

2. Criar `index.md` com o front matter obrigatório:
   ```yaml
   ---
   title: "HTB — NomeDaMaquina"
   permalink: /writeups/htb-nome-da-maquina/
   date: 2024-01-15
   platform: "HackTheBox"     # HackTheBox | TryHackMe | CTF
   difficulty: "medium"        # low | medium | critical | info
   tags: ["Linux", "Web"]
   description: "Frase curta sobre o que o writeup cobre."
   ---
   ```

3. Colocar imagens/vídeos usados no writeup **dentro da mesma pasta**:
   ```
   _writeups/htb-nome-da-maquina/
     index.md
     recon.png
     foothold.png
   ```

4. Referenciar imagens no markdown com caminho relativo:
   ```markdown
   ![Resultado do scan](./recon.png)
   ```

5. Fazer push para `main` — o GitHub Actions builda e publica automaticamente.

## Mapeamento de dificuldade

| Plataforma | Dificuldade | Badge |
|---|---|---|
| HTB Easy / THM Easy | `low` | verde |
| HTB Medium / THM Medium | `medium` | amarelo |
| HTB Hard / Insane | `critical` | vermelho |
| CTF genérico | `info` | roxo |

## Setup inicial (apenas uma vez)

No GitHub → Settings → Pages → Source: selecionar **GitHub Actions** (não "Deploy from a branch").

## Estrutura

```
writeups/
├── _writeups/           → um diretório por writeup (md + imagens)
├── _layouts/            → templates Jekyll
├── assets/css/          → estilos de prosa
├── i18n/                → traduções PT/EN da listagem
├── index.html           → página de listagem
└── _config.yml          → configuração Jekyll
```
