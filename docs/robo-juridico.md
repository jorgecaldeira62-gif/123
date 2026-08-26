# RobÃ´ JurÃ­dico - IntegraÃ§Ã£o com a Plataforma

O robÃ´ jurÃ­dico foi integrado Ã  plataforma como um serviÃ§o API, permitindo a automaÃ§Ã£o do monitoramento de publicaÃ§Ãµes jurÃ­dicas e criaÃ§Ã£o de rascunhos de e-mails para clientes.

## Funcionalidades

- **Monitoramento AutomÃ¡tico**: Consulta a API do DJEN/CNJ para novas publicaÃ§Ãµes
- **IdentificaÃ§Ã£o de Clientes**: Relaciona processos com clientes na planilha
- **CriaÃ§Ã£o de Rascunhos**: Gera e-mails no Gmail com informaÃ§Ãµes das publicaÃ§Ãµes
- **Armazenamento de Documentos**: Salva PDFs no Google Drive (opcional)

## ConfiguraÃ§Ã£o

### VariÃ¡veis de Ambiente

As seguintes variÃ¡veis de ambiente devem ser configuradas no arquivo `.env`:

```env
# Gmail (IMAP) - Para criaÃ§Ã£o de rascunhos de e-mail
EMAIL_LOGIN=seu_email@gmail.com
SENHA_APP=sua_senha_de_aplicativo
IMAP_SERVER=imap.gmail.com
PASTA_DRAFTS=[Gmail]/Rascunhos

# Planilha de clientes
ARQUIVO_CLIENTES=clientes.xlsx

# API do DJEN / CNJ
DJEN_API_URL=https://comunicaapi.pje.jus.br/api/v1/comunicacao
DJEN_TOKEN=seu_token_djen

# Google Drive (opcional)
SALVAR_NO_DRIVE=false
PASTA_DRIVE_ID=sua_id_da_pasta_no_drive
```

### Planilha de Clientes

A planilha de clientes (`clientes.xlsx`) deve conter as seguintes colunas:

- `nome_completo`: Nome completo do cliente
- `email`: E-mail do cliente
- `processos`: Lista de nÃºmeros de processos do cliente (separados por vÃ­rgula)

## Uso

### Via Interface Web

1. Acesse a seÃ§Ã£o de RobÃ´ JurÃ­dico na interface
2. Verifique o status de configuraÃ§Ã£o
3. Execute o robÃ´ manualmente quando necessÃ¡rio

### Via API

#### Verificar Status

```bash
curl -X GET http://localhost:5000/api/robo-juridico/status \
  -H "Content-Type: application/json" \
  -H "Cookie: connect.sid=..."
```

#### Executar o RobÃ´

```bash
curl -X POST http://localhost:5000/api/robo-juridico/executar \
  -H "Content-Type: application/json" \
  -H "Cookie: connect.sid=..."
```

## Estrutura de Resposta

### Status

```json
{
  "success": true,
  "data": {
    "status": "ativo",
    "arquivos": {
      "main.py": true,
      "config.py": true,
      // ...
    },
    "configuracoes": {
      "EMAIL_LOGIN": true,
      "SENHA_APP": true,
      // ...
    },
    "todos_configurados": true,
    "mensagem": "RobÃ´ jurÃ­dico configurado corretamente"
  }
}
```

### ExecuÃ§Ã£o

```json
{
  "success": true,
  "data": {
    "message": "Processamento concluÃ­do: 5 processadas, 1 com erro, 2 ignoradas",
    "results": [
      {
        "processo": "0000000-00.0000.0.00.0000",
        "status": "concluÃ­do",
        "acoes_realizadas": [
          "extraÃ§Ã£o de dados da sessÃ£o",
          "criaÃ§Ã£o de rascunho de e-mail"
        ]
      }
    ],
    "statistics": {
      "total_publicacoes": 8,
      "processadas": 5,
      "com_erro": 1,
      "ignoradas": 2
    },
    "timestamp": "2024-01-01T12:00:00"
  }
}
```

## SoluÃ§Ã£o de Problemas

### RobÃ´ nÃ£o estÃ¡ ativo

Verifique se todas as variÃ¡veis de ambiente estÃ£o configuradas corretamente, especialmente:

- `EMAIL_LOGIN` e `SENHA_APP` para acesso ao Gmail
- `DJEN_TOKEN` para acesso Ã  API do DJEN
- `ARQUIVO_CLIENTES` aponta para um arquivo existente

### Erros de autenticaÃ§Ã£o no Gmail

Certifique-se de que:

1. A autenticaÃ§Ã£o de dois fatores estÃ¡ ativada na conta Google
2. A senha de aplicativo foi gerada corretamente
3. O login estÃ¡ correto (deve ser o e-mail completo)

### Erros na API do DJEN

Verifique se o token do DJEN Ã© vÃ¡lido e se tem permissÃ£o para acessar a API.

## PrÃ³ximos Passos

- Agendamento automÃ¡tico de execuÃ§Ã£o
- Interface web para configuraÃ§Ã£o do robÃ´
- RelatÃ³rios detalhados de execuÃ§Ã£o
- IntegraÃ§Ã£o com outros serviÃ§os de e-mail