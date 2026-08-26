"""
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
â          ð  MÃDULO DE EXTRAÃÃO DE DADOS VIA REGEX                  â
â  LÃª o texto de intimaÃ§Ã£o e extrai datas de sessÃ£o virtual.          â
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

PadrÃµes reconhecidos:
  - "... entre os dias DD/MM/AAAA e DD/MM/AAAA ..."
  - "... perÃ­odo de DD/MM/AAAA a DD/MM/AAAA ..."
  - "... julgamento virtual de DD/MM/AAAA atÃ© DD/MM/AAAA ..."
  - "... inÃ­cio em DD/MM/AAAA e tÃ©rmino em DD/MM/AAAA ..."
"""

import re
from datetime import datetime, timedelta
from typing import Optional


# PadrÃ£o de data DD/MM/AAAA
_DATA = r"(\d{2}/\d{2}/\d{4})"

# VariaÃ§Ãµes de conectivos entre as datas
_CONECTIVOS = r"(?:e|a|atÃ©|ao|com tÃ©rmino em|com tÃ©rmino)"

# Regex principal: captura inÃ­cio e fim da sessÃ£o
_PADROES = [
    # "entre os dias DD/MM/AAAA e DD/MM/AAAA"
    re.compile(
        rf"entre\s+os\s+dias\s+{_DATA}\s+{_CONECTIVOS}\s+{_DATA}",
        re.IGNORECASE,
    ),
    # "perÃ­odo de DD/MM/AAAA a DD/MM/AAAA"
    re.compile(
        rf"per[Ã­i]odo\s+de\s+{_DATA}\s+{_CONECTIVOS}\s+{_DATA}",
        re.IGNORECASE,
    ),
    # "julgamento virtual de DD/MM/AAAA atÃ© DD/MM/AAAA"
    re.compile(
        rf"julgamento\s+(?:virtual\s+)?de\s+{_DATA}\s+{_CONECTIVOS}\s+{_DATA}",
        re.IGNORECASE,
    ),
    # "inÃ­cio em DD/MM/AAAA e tÃ©rmino em DD/MM/AAAA"
    re.compile(
        rf"in[Ã­i]cio\s+(?:em\s+)?{_DATA}.*?t[eÃ©]rmino\s+(?:em\s+)?{_DATA}",
        re.IGNORECASE | re.DOTALL,
    ),
    # "de DD/MM/AAAA a DD/MM/AAAA" (genÃ©rico)
    re.compile(
        rf"\bde\s+{_DATA}\s+{_CONECTIVOS}\s+{_DATA}",
        re.IGNORECASE,
    ),
]


def _parse_data(texto: str) -> Optional[datetime]:
    """Converte string DD/MM/AAAA em datetime. Retorna None se invÃ¡lida."""
    try:
        return datetime.strptime(texto.strip(), "%d/%m/%Y")
    except ValueError:
        return None


def extrair_dados_sessao(texto: str) -> Optional[dict]:
    """
    Analisa o texto de intimaÃ§Ã£o e retorna um dicionÃ¡rio com:
      - inicio      (str)      : data de inÃ­cio da sessÃ£o   (DD/MM/AAAA)
      - fim         (str)      : data de fim da sessÃ£o      (DD/MM/AAAA)
      - prazo_oral  (str)      : data limite para sustentaÃ§Ã£o oral (48h antes do inÃ­cio)
      - inicio_dt   (datetime) : data de inÃ­cio como objeto datetime
      - fim_dt      (datetime) : data de fim como objeto datetime

    Retorna None se nÃ£o encontrar datas no texto.
    """
    for padrao in _PADROES:
        match = padrao.search(texto)
        if match:
            str_inicio, str_fim = match.group(1), match.group(2)

            dt_inicio = _parse_data(str_inicio)
            dt_fim    = _parse_data(str_fim)

            if not dt_inicio or not dt_fim:
                continue

            # Prazo para sustentaÃ§Ã£o oral = 48 horas antes do inÃ­cio
            dt_prazo = dt_inicio - timedelta(hours=48)

            return {
                "inicio"     : dt_inicio.strftime("%d/%m/%Y"),
                "fim"        : dt_fim.strftime("%d/%m/%Y"),
                "prazo_oral" : dt_prazo.strftime("%d/%m/%Y Ã s %H:%M"),
                "inicio_dt"  : dt_inicio,
                "fim_dt"     : dt_fim,
            }

    return None  # Nenhum padrÃ£o reconhecido
