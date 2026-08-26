"""
Testes automÃ¡ticos para o mÃ³dulo regex_parser.
Execute com: python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.regex_parser import extrair_dados_sessao


# ââ Casos que DEVEM ser reconhecidos âââââââââââââââââââââââââââââââââââââââââ

def test_padrao_entre_os_dias():
    texto = (
        "JULGAMENTO VIRTUAL. O julgamento ocorrerÃ¡ de forma virtual "
        "entre os dias 26/11/2025 e 02/12/2025."
    )
    resultado = extrair_dados_sessao(texto)
    assert resultado is not None
    assert resultado["inicio"] == "26/11/2025"
    assert resultado["fim"] == "02/12/2025"


def test_padrao_periodo_de():
    texto = "SessÃ£o virtual designada para o perÃ­odo de 10/12/2025 a 17/12/2025."
    resultado = extrair_dados_sessao(texto)
    assert resultado is not None
    assert resultado["inicio"] == "10/12/2025"
    assert resultado["fim"] == "17/12/2025"


def test_padrao_julgamento_virtual_de():
    texto = "Pauta: julgamento virtual de 05/01/2026 atÃ© 12/01/2026."
    resultado = extrair_dados_sessao(texto)
    assert resultado is not None
    assert resultado["inicio"] == "05/01/2026"
    assert resultado["fim"] == "12/01/2026"


def test_padrao_inicio_termino():
    texto = "InÃ­cio em 20/02/2026 e tÃ©rmino em 27/02/2026."
    resultado = extrair_dados_sessao(texto)
    assert resultado is not None
    assert resultado["inicio"] == "20/02/2026"
    assert resultado["fim"] == "27/02/2026"


def test_prazo_oral_48h_antes():
    texto = "Julgamento virtual entre os dias 28/11/2025 e 04/12/2025."
    resultado = extrair_dados_sessao(texto)
    assert resultado is not None
    # Prazo oral = 48h antes do inÃ­cio (28/11 â 26/11)
    assert "26/11/2025" in resultado["prazo_oral"]


# ââ Casos que NÃO devem ser reconhecidos âââââââââââââââââââââââââââââââââââââ

def test_texto_sem_datas():
    texto = "Processo em andamento. Nenhuma data designada."
    resultado = extrair_dados_sessao(texto)
    assert resultado is None


def test_texto_vazio():
    resultado = extrair_dados_sessao("")
    assert resultado is None
