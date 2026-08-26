"""
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
â             ð¡  MÃDULO DE CONSULTA Ã API DO DJEN / CNJ              â
â  Endpoint: /comunicacao  (DJEN v1.0.3)                              â
ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

A API do DJEN exige um Bearer Token JWT (RS256). O mÃ³dulo tenta:
  1. Usar DJEN_TOKEN do .env (se configurado)
  2. Gerar automaticamente via PDPJ_PEM_PRIVATE_KEY + ADVOGADO_CPF do .env

Configure pelo menos PDPJ_PEM_PRIVATE_KEY e ADVOGADO_CPF no .env.
"""

import json
import time
import requests
from typing import List, Dict
from config import DJEN_API_URL, DJEN_TOKEN, PDPJ_PEM_PRIVATE_KEY, ADVOGADO_CPF

# NÃºmero de pÃ¡ginas a consultar por execuÃ§Ã£o (ajuste conforme volume)
MAX_PAGINAS = 5
ITENS_POR_PAGINA = 20


def _gerar_token_pem() -> str:
    """Gera JWT RS256 automaticamente usando a chave PEM do .env."""
    if not PDPJ_PEM_PRIVATE_KEY or not ADVOGADO_CPF:
        return ""
    try:
        import jwt as pyjwt  # PyJWT
        pem = PDPJ_PEM_PRIVATE_KEY.replace("\\n", "\n").strip()
        cpf_limpo = "".join(c for c in ADVOGADO_CPF if c.isdigit())
        if len(cpf_limpo) != 11:
            print("â ï¸  ADVOGADO_CPF invÃ¡lido no .env â deve ter 11 dÃ­gitos.")
            return ""
        now = int(time.time())
        payload = {
            "sub": cpf_limpo,
            "iss": "pdpj-br",
            "aud": "https://comunicaapi.pje.jus.br",
            "iat": now,
            "exp": now + 3600,
            "jti": f"djen-{now}",
        }
        token = pyjwt.encode(payload, pem, algorithm="RS256")
        # PyJWT >= 2.x retorna str, < 2.x retorna bytes
        return token if isinstance(token, str) else token.decode("utf-8")
    except ImportError:
        print("â ï¸  PyJWT nÃ£o instalado. Execute: pip install PyJWT cryptography")
        return ""
    except Exception as exc:
        print(f"â ï¸  Erro ao gerar JWT automÃ¡tico: {exc}")
        return ""


def _obter_token() -> str:
    """Retorna token: primeiro do .env, depois tenta gerar via PEM."""
    if DJEN_TOKEN:
        return DJEN_TOKEN
    token = _gerar_token_pem()
    if token:
        print("   ð Token JWT gerado automaticamente via PDPJ_PEM_PRIVATE_KEY.")
    return token


def buscar_publicacoes() -> List[Dict]:
    """
    Consulta a API do DJEN e retorna a lista de publicaÃ§Ãµes.
    Tenta DJEN_TOKEN do .env primeiro; se ausente, gera JWT via PEM automaticamente.
    Retorna lista vazia em caso de erro ou sem resultados.
    """
    token = _obter_token()
    if not token:
        print("â ï¸  Sem token disponÃ­vel (DJEN_TOKEN vazio e PEM nÃ£o configurado).")
        print("   â Rodando em modo SIMULADO com dados de exemplo.\n")
        return _dados_simulados()

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    todas_publicacoes: list[dict] = []

    for pagina in range(1, MAX_PAGINAS + 1):
        params = {
            "pagina": pagina,
            "itensPorPagina": ITENS_POR_PAGINA,
        }
        try:
            print(f"   ð¡ Consultando DJEN â pÃ¡gina {pagina}...")
            resp = requests.get(DJEN_API_URL, headers=headers, params=params, timeout=15)

            if resp.status_code == 401:
                print("   â 401 Unauthorized â Token invÃ¡lido ou expirado.")
                print("      â Configure PDPJ_PEM_PRIVATE_KEY e ADVOGADO_CPF no .env para auto-geraÃ§Ã£o.")
                break

            if resp.status_code == 403:
                print("   â 403 Forbidden â IP bloqueado ou chave nÃ£o registrada no PDPJ.")
                break

            if resp.status_code != 200:
                print(f"   â Erro HTTP {resp.status_code}: {resp.text[:200]}")
                break

            dados = resp.json()

            # A API pode retornar { "comunicacoes": [...] } ou diretamente uma lista
            itens = dados.get("comunicacoes") or dados.get("data") or dados
            if isinstance(itens, dict):
                itens = list(itens.values())

            if not itens:
                print(f"   â¹ï¸  PÃ¡gina {pagina} vazia. Encerrando paginaÃ§Ã£o.")
                break

            todas_publicacoes.extend(itens)
            print(f"   â {len(itens)} item(ns) recebido(s) na pÃ¡gina {pagina}.")

            # Verifica se hÃ¡ mais pÃ¡ginas
            total = dados.get("total") or dados.get("totalItens") or 0
            if total and len(todas_publicacoes) >= int(total):
                break

        except requests.exceptions.Timeout:
            print("   â Timeout ao conectar na API do DJEN.")
            break
        except requests.exceptions.ConnectionError as exc:
            print(f"   â Erro de conexÃ£o: {exc}")
            break
        except json.JSONDecodeError:
            print("   â Resposta da API nÃ£o Ã© JSON vÃ¡lido.")
            break

    return todas_publicacoes


# ââ Dados simulados para testes sem token âââââââââââââââââââââââââââââââââââ
def _dados_simulados() -> list[dict]:
    return [
        {
            "numeroProcesso": "6002755-35.2024.4.06.3819",
            "texto": (
                "JULGAMENTO VIRTUAL. Processo nÂº 6002755-35.2024.4.06.3819. "
                "O julgamento ocorrerÃ¡ de forma virtual entre os dias "
                "26/11/2025 e 02/12/2025. Partes: Maikon da Rocha Caldeira. "
                "Assunto: Aposentadoria por Tempo de ContribuiÃ§Ã£o."
            ),
            "linkDocumento": "",
        },
        {
            "numeroProcesso": "0001234-56.2023.8.21.0001",
            "texto": (
                "PAUTA VIRTUAL. Processo nÂº 0001234-56.2023.8.21.0001. "
                "SessÃ£o virtual de julgamento designada para o perÃ­odo de "
                "10/12/2025 a 17/12/2025. Recurso de apelaÃ§Ã£o."
            ),
            "linkDocumento": "",
        },
    ]
