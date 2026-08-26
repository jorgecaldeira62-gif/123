# ð jwt-tools

UtilitÃ¡rios Node.js para gerar e verificar tokens JWT RS256 â
compatÃ­veis com **PDPJ** e **PJUD** (sistema CNJ/tribunais federais).

---

## PrÃ©-requisitos

- **Node.js 18+** (usa `fetch` global nativo)
- Sua chave privada RSA em formato PEM

---

## InstalaÃ§Ã£o

```bash
cd jwt-tools
npm install
```

---

## Arquivos

| Arquivo        | FunÃ§Ã£o |
|----------------|--------|
| `genpub.js`    | Extrai a chave pÃºblica `.pub.pem` a partir da chave privada |
| `sign.js`      | Gera JWT simples (modo PDPJ/Swagger, 1 hora de validade) |
| `gen_pjud.js`  | Gera JWT configurÃ¡vel para PJUD (`client_assertion`) |
| `verify.js`    | Verifica e decodifica um JWT usando a chave pÃºblica |
| `call_pjud.js` | Faz chamada autenticada Ã  API do PJUD com o token salvo |

---

## Fluxo completo

### 1. Gerar chave pÃºblica (enviar ao PDPJ para registro)

```bash
node genpub.js "C:/Users/Caldeira/chave_privada.pem"
```
â Gera `maikon.pub.pem`

---

### 2. Gerar token para o Swagger/HomologaÃ§Ã£o

```bash
node sign.js "C:/Users/Caldeira/chave_privada.pem" 09494128648
```
â Imprime o token. Cole no campo `Authorization: Bearer <TOKEN>` do Swagger.

---

### 3. Gerar token `client_assertion` para PJUD

```bash
node gen_pjud.js \
  --key  "C:/Users/Caldeira/chave_privada.pem" \
  --sub  "09494128648" \
  --iss  "https://seu-issuer.pdpj.jus.br" \
  --aud  "https://gateway.stg.cloud.pje.jus.br" \
  --name "Maikon da Rocha Caldeira" \
  --exp  3600 \
  --out  pjud_token.txt
```

**ParÃ¢metros disponÃ­veis:**

| Flag     | DescriÃ§Ã£o | PadrÃ£o |
|----------|-----------|--------|
| `--key`  | Caminho da chave privada PEM | `chave_privada.pem` |
| `--sub`  | CPF (11 dÃ­gitos, sem pontos/traÃ§os) | `00000000000` |
| `--iss`  | Issuer (URL registrada no PDPJ) | `https://seu-issuer.example` |
| `--aud`  | Audience (URL do gateway) | `https://gateway.stg.cloud.pje.jus.br` |
| `--name` | Nome completo (claim `name`) | *(omitido)* |
| `--exp`  | Validade: segundos (`3600`) ou shorthand (`1h`, `5m`) | `5m` |
| `--out`  | Arquivo de saÃ­da | `pjud_token.txt` |

---

### 4. Verificar um token

```bash
node verify.js maikon.pub.pem "eyJ..."
```

---

### 5. Chamar a API do PJUD autenticado

```bash
node call_pjud.js \
  --url "https://comunicaapi.pje.jus.br/api/v1/comunicacao" \
  --tokenfile pjud_token.txt
```

---

### 6. Trocar JWT por `access_token` (OAuth2 `client_credentials`)

```bash
curl -X POST "https://TOKEN_ENDPOINT_PDPJ/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer\
&client_id=SEU_CLIENT_ID\
&client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer\
&client_assertion=$(cat pjud_token.txt)"
```

> Confirme o `token_endpoint` com a equipe PDPJ â ele muda entre homologaÃ§Ã£o e produÃ§Ã£o.

---

## DiagnÃ³stico de erros comuns

| Erro | Causa | SoluÃ§Ã£o |
|------|-------|---------|
| `error:0909006C:PEM routines` | Quebras de linha ausentes na chave | O script corrige automaticamente |
| `invalid signature` | Chave pÃºblica diferente da privada | Regere com `genpub.js` |
| `jwt expired` | Token vencido | Gere novo com `gen_pjud.js` |
| `401 Unauthorized` | Chave nÃ£o registrada no PDPJ | Envie `maikon.pub.pem` por e-mail ao suporte |
| `403 Forbidden` | IP fora do Brasil | Use servidor brasileiro |

---

## SeguranÃ§a

- â ï¸ **Nunca** compartilhe `chave_privada.pem`
- â Compartilhe apenas `maikon.pub.pem` para registro no PDPJ
- Use validade curta (`5m`) para `client_assertion`
- Adicione `*.pem` ao `.gitignore`
