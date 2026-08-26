"""
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
â                   âï¸  CONFIGURAÃÃES CENTRAIS                        â
â  Carrega variÃ¡veis do arquivo .env (nunca commite o .env no Git!)   â
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
"""

import os
from dotenv import load_dotenv

# Carrega o arquivo .env da raiz do projeto
load_dotenv()

# ââ Gmail (IMAP) ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
EMAIL_LOGIN  : str  = os.getenv("EMAIL_LOGIN",  "seu_email@gmail.com")
SENHA_APP    : str  = os.getenv("SENHA_APP",    "")
IMAP_SERVER  : str  = os.getenv("IMAP_SERVER",  "imap.gmail.com")
PASTA_DRAFTS : str  = os.getenv("PASTA_DRAFTS", "[Gmail]/Rascunhos")

# ââ Planilha de clientes âââââââââââââââââââââââââââââââââââââââââââââââââââââ
ARQUIVO_CLIENTES : str = os.getenv("ARQUIVO_CLIENTES", "clientes.xlsx")

# ââ API do DJEN / CNJ ââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
#   Endpoint de comunicaÃ§Ãµes do DJEN v1.0.3
DJEN_API_URL : str = os.getenv(
    "DJEN_API_URL",
    "https://comunicaapi.pje.jus.br/api/v1/comunicacao"
)
DJEN_TOKEN : str = os.getenv("DJEN_TOKEN", "")

# ââ Chave PEM e CPF para auto-geraÃ§Ã£o de JWT (PDPJ / DJEN) ââââââââââââââââââ
#   Se DJEN_TOKEN estiver vazio, o sistema tentarÃ¡ gerar o token automaticamente
#   usando a chave privada PEM registrada no PDPJ/CNJ.
PDPJ_PEM_PRIVATE_KEY : str = os.getenv("PDPJ_PEM_PRIVATE_KEY", "")
ADVOGADO_CPF         : str = os.getenv("ADVOGADO_CPF", "")

# ââ Google Drive (opcional) ââââââââââââââââââââââââââââââââââââââââââââââââââ
SALVAR_NO_DRIVE : bool = os.getenv("SALVAR_NO_DRIVE", "false").lower() == "true"
PASTA_DRIVE_ID  : str  = os.getenv("PASTA_DRIVE_ID",  "")
