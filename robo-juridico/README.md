# ð¤ RobÃ´ de Monitoramento JurÃ­dico

> AutomaÃ§Ã£o completa para advocacia: monitora o DJEN, extrai prazos,
> identifica clientes e cria rascunhos de e-mail prontos para envio.

**Advogado:** Maikon da Rocha Caldeira â OAB/RS

---

## ð Funcionalidades

| # | MÃ³dulo | O que faz |
|---|--------|-----------|
| 1 | `api_djen.py` | Consulta a API do DJEN/CNJ (`/comunicacao`) com paginaÃ§Ã£o automÃ¡tica |
| 2 | `regex_parser.py` | Extrai datas de inÃ­cio/fim de sessÃµes virtuais e calcula o prazo de SustentaÃ§Ã£o Oral (48h) |
| 3 | `excel_manager.py` | LÃª `clientes.xlsx` e identifica o dono do processo |
| 4 | `email_draft.py` | Cria rascunho de e-mail no Gmail via IMAP (sem enviar â vocÃª revisa antes) |
| 5 | `drive_manager.py` | (Opcional) Baixa PDF do tribunal e envia direto ao Google Drive |

---

## ð  PrÃ©-requisitos

- **Python 3.10+**
- **Node.js 18+** (para gerar tokens JWT com `jwt-tools`)
- Conta Gmail com **Senha de Aplicativo** ativada (nÃ£o use a senha normal)

---

## ð¦ InstalaÃ§Ã£o

```bash
# 1. Acesse a pasta
cd robo-juridico

# 2. Crie ambiente virtual
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Instale dependÃªncias
pip install -r requirements.txt

# 4. (Opcional) Se usar Google Drive
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

## âï¸ ConfiguraÃ§Ã£o

### 1. Arquivo `.env`

Copie o exemplo e preencha os valores:

```bash
cp .env.example .env
```

| VariÃ¡vel | DescriÃ§Ã£o |
|----------|-----------|
| `EMAIL_LOGIN` | Seu endereÃ§o Gmail |
| `SENHA_APP` | Senha de Aplicativo do Google (4 grupos de 4 letras) |
| `PASTA_DRAFTS` | `[Gmail]/Rascunhos` (PT) ou `[Gmail]/Drafts` (EN) |
| `ARQUIVO_CLIENTES` | Caminho da planilha Excel (padrÃ£o: `clientes.xlsx`) |
| `DJEN_TOKEN` | Token JWT gerado com `jwt-tools` |
| `SALVAR_NO_DRIVE` | `true` para ativar upload de PDFs |
| `PASTA_DRIVE_ID` | ID da pasta do Google Drive (opcional) |

### 2. Planilha de Clientes (`clientes.xlsx`)

Crie a planilha com estas colunas (**linha 1 = cabeÃ§alho**):

| processo | nome_completo | email | tratamento | nome_caso |
|----------|---------------|-------|------------|-----------|
| 6002755-35.2024.4.06.3819 | Maria do Carmo Silva | maria@email.com | Prezada Maria | Aposentadoria |

> â ï¸ Formate a coluna `processo` como **Texto** no Excel para evitar perda de zeros.

### 3. Token JWT para o DJEN

```bash
cd jwt-tools
npm install

node gen_pjud.js \
  --key  "caminho/chave_privada.pem" \
  --sub  "09494128648" \
  --iss  "https://seu-issuer.pdpj.jus.br" \
  --aud  "https://gateway.stg.cloud.pje.jus.br" \
  --name "Maikon da Rocha Caldeira" \
  --exp  3600 \
  --out  pjud_token.txt
```

Copie o conteÃºdo de `pjud_token.txt` e cole no `.env` como `DJEN_TOKEN=eyJ...`.

---

## â¶ï¸ Como Usar

```bash
# Executa o robÃ´ manualmente
python main.py
```

O robÃ´ irÃ¡:
1. Ler a planilha de clientes
2. Consultar a API do DJEN
3. Para cada publicaÃ§Ã£o com sessÃ£o virtual:
   - Extrair datas e prazo de SustentaÃ§Ã£o Oral
   - Identificar o cliente
   - Salvar rascunho de e-mail no Gmail
   - (Se ativo) Fazer upload do PDF no Google Drive

---

## ð§ª Testes

```bash
# Instale o pytest
pip install pytest

# Execute os testes
python -m pytest tests/ -v
```

---

## â° Agendamento AutomÃ¡tico

### Windows (Agendador de Tarefas)

1. Abra **"Agendador de Tarefas"** â **"Criar Tarefa BÃ¡sica"**
2. Defina o horÃ¡rio (ex: todos os dias Ã s 08:00)
3. AÃ§Ã£o: **"Iniciar um programa"**
4. Programa: `C:\caminho\robo-juridico\venv\Scripts\python.exe`
5. Argumentos: `C:\caminho\robo-juridico\main.py`

### Linux / Mac (Cron)

```bash
# Abra o crontab
crontab -e

# Adicione a linha (executa todo dia Ã s 08:00)
0 8 * * * /caminho/robo-juridico/venv/bin/python /caminho/robo-juridico/main.py >> /caminho/robo-juridico/robo.log 2>&1
```

---

## ð Estrutura do Projeto

```
robo-juridico/
âââ main.py                  # Ponto de entrada â orquestra tudo
âââ config.py                # Carrega variÃ¡veis do .env
âââ requirements.txt         # DependÃªncias Python
âââ .env.example             # Modelo de configuraÃ§Ã£o (copie para .env)
âââ .gitignore               # Protege dados sensÃ­veis
âââ clientes.xlsx            # (nÃ£o commitado) Base de clientes
â
âââ modules/
â   âââ api_djen.py          # Consulta Ã  API do DJEN/CNJ
â   âââ regex_parser.py      # ExtraÃ§Ã£o de datas via Regex
â   âââ excel_manager.py     # Leitura da planilha de clientes
â   âââ email_draft.py       # CriaÃ§Ã£o de rascunhos no Gmail
â   âââ drive_manager.py     # Upload de PDFs no Google Drive
â
âââ tests/
â   âââ test_regex_parser.py # Testes do parser de datas
â   âââ test_excel_manager.py# Testes da busca de clientes
â
âââ jwt-tools/               # Ferramentas Node.js para tokens JWT
    âââ sign.js              # Gera token simples (PDPJ)
    âââ gen_pjud.js          # Gera token configurÃ¡vel (PJUD)
    âââ genpub.js            # Extrai chave pÃºblica do PEM
    âââ verify.js            # Verifica/decodifica token
    âââ call_pjud.js         # Chama API autenticada
    âââ README.md            # DocumentaÃ§Ã£o dos JWT tools
```

---

## ð¡ SeguranÃ§a

- â `.gitignore` protege `.env`, `*.pem`, `token.json`, `credentials.json` e `clientes.xlsx`
- â Senhas armazenadas apenas no `.env` (nunca no cÃ³digo)
- â Tokens JWT com validade curta (5 min para `client_assertion`)
- â ï¸ **Nunca** compartilhe `chave_privada.pem` â somente `maikon.pub.pem` Ã© pÃºblico

---

## âï¸ Aviso Legal

Este software Ã© uma ferramenta auxiliar de produtividade.
**NÃ£o substitui a conferÃªncia manual** das publicaÃ§Ãµes e prazos nos sistemas
oficiais (PJe / Eproc). O advogado responsÃ¡vel deve sempre validar as
informaÃ§Ãµes antes de enviar comunicaÃ§Ãµes aos clientes.
