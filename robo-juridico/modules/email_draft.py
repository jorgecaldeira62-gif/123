"""
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
â          âï¸   MÃDULO DE CRIAÃÃO DE RASCUNHOS NO GMAIL               â
â  Usa protocolo IMAP para salvar e-mails na pasta Rascunhos.         â
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

PrÃ©-requisito:
  1. Ative a "VerificaÃ§Ã£o em duas etapas" na conta Google.
  2. Em "SeguranÃ§a" â "Senhas de app", gere uma senha para "Email".
  3. Coloque a senha no .env: SENHA_APP=xxxx xxxx xxxx xxxx
  4. Ative o acesso IMAP em: Gmail â ConfiguraÃ§Ãµes â Encaminhamento e POP/IMAP.

Pasta de rascunhos:
  - Gmail em PortuguÃªs : [Gmail]/Rascunhos
  - Gmail em InglÃªs    : [Gmail]/Drafts
  (ajuste PASTA_DRAFTS no .env)
"""

import imaplib
import time
from email.message import EmailMessage
from config import EMAIL_LOGIN, SENHA_APP, IMAP_SERVER, PASTA_DRAFTS


def criar_rascunho_cliente(dados_processo: dict, cliente: dict) -> bool:
    """
    Cria um rascunho de e-mail na pasta Rascunhos do Gmail.

    Args:
        dados_processo: dict com chaves numero, inicio, fim, prazo, texto
        cliente:        dict com chaves nome_completo, email, tratamento, nome_caso

    Returns:
        True se o rascunho foi salvo com sucesso, False caso contrÃ¡rio.
    """
    if not SENHA_APP:
        print("   â ï¸  SENHA_APP nÃ£o configurada no .env â rascunho nÃ£o criado.")
        return False

    numero         = dados_processo.get("numero", "N/A")
    data_inicio    = dados_processo.get("inicio", "N/A")
    data_fim       = dados_processo.get("fim",    "N/A")
    prazo_oral     = dados_processo.get("prazo",  "N/A")
    nome_caso      = cliente.get("nome_caso", "")
    tratamento     = cliente.get("tratamento") or "Prezado(a) Cliente"
    email_cliente  = cliente.get("email", "")
    nome_completo  = cliente.get("nome_completo", "")

    if not email_cliente:
        print(f"   â ï¸  E-mail do cliente '{nome_completo}' nÃ£o cadastrado.")
        return False

    # ââ Monta o assunto ââââââââââââââââââââââââââââââââââââââââââââââââââ
    assunto = (
        f"Comunicado: Julgamento Virtual Designado"
        + (f" â {nome_caso}" if nome_caso else f" â Proc. {numero}")
    )

    # ââ Monta o corpo do e-mail ââââââââââââââââââââââââââââââââââââââââââ
    corpo = f"""\
{tratamento},

Espero que esteja bem.

Informo que foi designada sessÃ£o de julgamento **virtual** para o seu processo.

âââââââââââââââââââââââââââââââââââ
  Processo nÂº    : {numero}
  InÃ­cio da sessÃ£o: {data_inicio}
  TÃ©rmino da sessÃ£o: {data_fim}
  â ï¸  Prazo para SustentaÃ§Ã£o Oral: {prazo_oral}
âââââââââââââââââââââââââââââââââââ

Neste momento, **nÃ£o Ã© necessÃ¡rio o seu comparecimento**. O julgamento acontece de forma eletrÃ´nica entre os magistrados.

Nossa equipe jÃ¡ estÃ¡ monitorando o prazo para eventual SustentaÃ§Ã£o Oral (manifestaÃ§Ã£o oral antes do voto), caso seja cabÃ­vel.

Assim que tivermos o resultado, entro em contato imediatamente.

Qualquer dÃºvida, estou Ã  disposiÃ§Ã£o.

Atenciosamente,

Maikon da Rocha Caldeira
Advogado â OAB/RS
"""

    # ââ Monta o objeto EmailMessage ââââââââââââââââââââââââââââââââââââââ
    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"]    = EMAIL_LOGIN
    msg["To"]      = email_cliente
    msg.set_content(corpo)

    # ââ Conecta via IMAP e salva o rascunho ââââââââââââââââââââââââââââââ
    try:
        print(f"   âï¸  Criando rascunho para {nome_completo} <{email_cliente}>...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_LOGIN, SENHA_APP)

        result = mail.append(
            PASTA_DRAFTS,
            "\\Draft",
            imaplib.Time2Internaldate(time.time()),
            msg.as_bytes(),
        )
        mail.logout()

        if result[0] == "OK":
            print(f"   â Rascunho salvo em '{PASTA_DRAFTS}'!")
            return True
        else:
            print(f"   â IMAP append retornou: {result}")
            return False

    except imaplib.IMAP4.error as exc:
        print(f"   â Erro IMAP: {exc}")
        _dica_pasta_drafts(str(exc))
        return False
    except OSError as exc:
        print(f"   â Erro de rede/SSL: {exc}")
        return False


def _dica_pasta_drafts(erro: str) -> None:
    if "select failed" in erro.lower() or "doesn't exist" in erro.lower():
        print("   ð¡ Dica: A pasta de rascunhos pode ter nome diferente.")
        print(f"      Atual: {PASTA_DRAFTS}")
        print("      Tente '[Gmail]/Drafts' (Gmail em inglÃªs) no .env: PASTA_DRAFTS=[Gmail]/Drafts")
