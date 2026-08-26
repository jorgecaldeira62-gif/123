"""
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
â         ð¤ ROBÃ DE MONITORAMENTO JURÃDICO â PONTO DE ENTRADA        â
â         Maikon da Rocha Caldeira â OAB/RS                           â
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

Fluxo completo:
  1. LÃª a planilha de clientes (clientes.xlsx)
  2. Consulta a API do DJEN/CNJ
  3. Para cada publicaÃ§Ã£o relevante:
     a. Extrai datas/prazos via Regex
     b. Identifica o cliente dono do processo
     c. Cria rascunho de e-mail no Gmail
     d. (Opcional) Salva o PDF no Google Drive
"""

import sys
from modules.api_djen      import buscar_publicacoes
from modules.regex_parser  import extrair_dados_sessao
from modules.excel_manager import carregar_clientes, buscar_cliente
from modules.email_draft   import criar_rascunho_cliente
from modules.drive_manager import salvar_link_no_drive
from config                import PASTA_DRIVE_ID, SALVAR_NO_DRIVE


def processar_publicacao(publicacao: dict, clientes: dict) -> None:
    numero_proc = publicacao.get("numeroProcesso", "")
    texto       = publicacao.get("texto", "")
    link_pdf    = publicacao.get("linkDocumento", "")

    print(f"\n{'â'*60}")
    print(f"ð Processo: {numero_proc}")

    # ââ 1. Extrai datas e prazos via Regex âââââââââââââââââââââââââââââ
    dados_sessao = extrair_dados_sessao(texto)

    if not dados_sessao:
        print("   â¹ï¸  Nenhuma sessÃ£o de julgamento identificada. Pulando.")
        return

    print(f"   ð InÃ­cio da sessÃ£o : {dados_sessao['inicio']}")
    print(f"   ð Fim da sessÃ£o    : {dados_sessao['fim']}")
    print(f"   â ï¸  Prazo oral (48h) : {dados_sessao['prazo_oral']}")

    # ââ 2. Identifica o cliente âââââââââââââââââââââââââââââââââââââââââ
    cliente = buscar_cliente(clientes, numero_proc)
    dados_proc = {
        "numero" : numero_proc,
        "inicio" : dados_sessao["inicio"],
        "fim"    : dados_sessao["fim"],
        "prazo"  : dados_sessao["prazo_oral"],
        "texto"  : texto[:300] + ("..." if len(texto) > 300 else ""),
    }

    if cliente:
        print(f"   ð¤ Cliente  : {cliente['nome_completo']}")
        print(f"   ð§ E-mail   : {cliente['email']}")
        # ââ 3. Cria rascunho de e-mail ââââââââââââââââââââââââââââââââââ
        criar_rascunho_cliente(dados_proc, cliente)

        # ââ 4. (Opcional) Salva PDF no Google Drive âââââââââââââââââââââââââ
        if SALVAR_NO_DRIVE and link_pdf:
            from datetime import datetime
            data_hoje   = datetime.now().strftime("%Y-%m-%d")
            nome_limpo  = cliente["nome_completo"].replace(" ", "_")
            nome_arquivo = f"{data_hoje}_Intimacao_{nome_limpo}_{numero_proc}.pdf"
            salvar_link_no_drive(link_pdf, nome_arquivo, pasta_id=PASTA_DRIVE_ID)
    else:
        print("   â ï¸  Cliente nÃ£o encontrado na planilha. Rascunho genÃ©rico ignorado.")


def main():
    print("=" * 60)
    print("  ð¤  ROBÃ JURÃDICO â INICIANDO                          ")
    print("=" * 60)

    # ââ Carrega planilha de clientes ââââââââââââââââââââââââââââââââââââ
    clientes = carregar_clientes()
    if clientes is None:
        print("â NÃ£o foi possÃ­vel carregar a planilha de clientes. Abortando.")
        sys.exit(1)
    print(f"â {len(clientes)} cliente(s) carregado(s) da planilha.\n")

    # ââ Consulta API do DJEN ââââââââââââââââââââââââââââââââââââââââââââ
    publicacoes = buscar_publicacoes()
    if not publicacoes:
        print("â¹ï¸  Nenhuma publicaÃ§Ã£o nova encontrada. Encerrando.")
        return

    print(f"ð¦ {len(publicacoes)} publicaÃ§Ã£o(Ãµes) encontrada(s). Processando...\n")

    for pub in publicacoes:
        try:
            processar_publicacao(pub, clientes)
        except Exception as exc:
            print(f"   â Erro inesperado ao processar publicaÃ§Ã£o: {exc}")

    print("\n" + "=" * 60)
    print("  â  ROBÃ JURÃDICO â CONCLUÃDO                          ")
    print("=" * 60)


if __name__ == "__main__":
    main()
