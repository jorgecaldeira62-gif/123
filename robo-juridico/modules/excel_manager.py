"""
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
â            ð  MÃDULO DE GESTÃO DA PLANILHA DE CLIENTES             â
â  LÃª clientes.xlsx e fornece busca por nÃºmero de processo.           â
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

Estrutura esperada da planilha (cabeÃ§alho na linha 1):

  | processo | nome_completo | email | tratamento | nome_caso |
  |----------|---------------|-------|------------|-----------|

  â ï¸  Formate a coluna "processo" como TEXTO no Excel para evitar
     truncamento de zeros e perda de pontuaÃ§Ã£o.
"""

import re
from typing import Optional
import pandas as pd
from config import ARQUIVO_CLIENTES

# Colunas obrigatÃ³rias
_COLUNAS_OBRIGATORIAS = {"processo", "nome_completo", "email"}


def carregar_clientes() -> Optional[dict[str, dict]]:
    """
    LÃª a planilha de clientes e retorna um dicionÃ¡rio indexado por nÃºmero
    de processo (normalizado: apenas dÃ­gitos e hifens/pontos).

    Retorna None em caso de erro crÃ­tico.
    """
    try:
        df = pd.read_excel(ARQUIVO_CLIENTES, dtype=str)
    except FileNotFoundError:
        print(f"â Planilha nÃ£o encontrada: '{ARQUIVO_CLIENTES}'")
        print("   â Crie o arquivo conforme o modelo no README.")
        return None
    except Exception as exc:
        print(f"â Erro ao ler a planilha: {exc}")
        return None

    # Normaliza nomes de colunas
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Valida colunas obrigatÃ³rias
    faltando = _COLUNAS_OBRIGATORIAS - set(df.columns)
    if faltando:
        print(f"â Colunas ausentes na planilha: {faltando}")
        print(f"   Colunas encontradas: {list(df.columns)}")
        return None

    # Preenche colunas opcionais com valor padrÃ£o
    if "tratamento"  not in df.columns: df["tratamento"]  = ""
    if "nome_caso"   not in df.columns: df["nome_caso"]   = ""

    clientes: dict[str, dict] = {}
    for _, row in df.iterrows():
        proc_raw = str(row.get("processo", "")).strip()
        if not proc_raw or proc_raw == "nan":
            continue

        # Normaliza o nÃºmero do processo para comparaÃ§Ã£o (remove espaÃ§os extras)
        proc_norm = _normalizar_processo(proc_raw)

        clientes[proc_norm] = {
            "processo"      : proc_raw,
            "nome_completo" : str(row.get("nome_completo", "")).strip(),
            "email"         : str(row.get("email",         "")).strip(),
            "tratamento"    : str(row.get("tratamento",    "")).strip(),
            "nome_caso"     : str(row.get("nome_caso",     "")).strip(),
        }

    return clientes


def buscar_cliente(clientes: dict[str, dict], numero_processo: str) -> Optional[dict]:
    """
    Busca o cliente pelo nÃºmero do processo.
    Faz comparaÃ§Ã£o normalizada para tolerar diferenÃ§as de formataÃ§Ã£o.
    """
    chave = _normalizar_processo(numero_processo)
    return clientes.get(chave)


def _normalizar_processo(numero: str) -> str:
    """
    Remove espaÃ§os e converte para minÃºsculas.
    MantÃ©m pontos, hÃ­fens e dÃ­gitos (padrÃ£o CNJ: NNNNNNN-DD.AAAA.J.TT.OOOO).
    """
    return re.sub(r"\s+", "", numero).lower()
