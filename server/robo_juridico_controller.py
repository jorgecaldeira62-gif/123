import sys
import os
import json
from typing import Dict, Any

# Adiciona o caminho do robÃ´ jurÃ­dico ao sys.path para importaÃ§Ã£o
sys.path.append(os.path.join(os.path.dirname(__file__), "../robo-juridico"))

class RoboJuridicoController:
    """
    Controlador para integraÃ§Ã£o do robÃ´ jurÃ­dico com a API web.
    Gerencia a execuÃ§Ã£o do robÃ´ e formataÃ§Ã£o dos resultados para resposta HTTP.
    """
    
    @staticmethod
    def executar_robo() -> Dict[str, Any]:
        """
        Executa o robÃ´ jurÃ­dico e retorna resultados formatados para API.
        """
        try:
            # Importa a classe do robÃ´ jurÃ­dico
            from robo_juridico_api import RoboJuridico
            
            # Executa o robÃ´
            robo = RoboJuridico()
            resultado = robo.executar()
            
            return {
                "success": resultado["sucesso"],
                "data": {
                    "message": resultado.get("mensagem", ""),
                    "results": resultado.get("resultados", []),
                    "statistics": resultado.get("estatisticas", {}),
                    "timestamp": resultado.get("timestamp", "")
                }
            }
            
        except ImportError as e:
            return {
                "success": False,
                "error": f"Erro ao importar mÃ³dulos do robÃ´ jurÃ­dico: {str(e)}",
                "data": {}
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao executar robÃ´ jurÃ­dico: {str(e)}",
                "data": {}
            }
    
    @staticmethod
    def obter_status() -> Dict[str, Any]:
        """
        Retorna o status do robÃ´ jurÃ­dico e sua configuraÃ§Ã£o.
        """
        try:
            # Verifica se os arquivos necessÃ¡rios existem
            robo_dir = os.path.join(os.path.dirname(__file__), "../robo-juridico")
            arquivos_necessarios = [
                "main.py",
                "config.py",
                "modules/api_djen.py",
                "modules/regex_parser.py",
                "modules/excel_manager.py",
                "modules/email_draft.py",
                "modules/drive_manager.py"
            ]
            
            arquivos_existentes = {}
            for arquivo in arquivos_necessarios:
                caminho = os.path.join(robo_dir, arquivo)
                arquivos_existentes[arquivo] = os.path.exists(caminho)
            
            # Verifica configuraÃ§Ãµes essenciais
            from dotenv import load_dotenv
            load_dotenv()
            
            configuracoes = {
                "EMAIL_LOGIN": os.getenv("EMAIL_LOGIN", "") != "",
                "SENHA_APP": os.getenv("SENHA_APP", "") != "",
                "DJEN_TOKEN": os.getenv("DJEN_TOKEN", "") != "",
                "ARQUIVO_CLIENTES": os.path.exists(os.getenv("ARQUIVO_CLIENTES", "clientes.xlsx"))
            }
            
            todos_configurados = all(configuracoes.values())
            
            return {
                "success": True,
                "data": {
                    "status": "ativo" if todos_configurados else "configuraÃ§Ã£o_incompleta",
                    "arquivos": arquivos_existentes,
                    "configuracoes": configuracoes,
                    "todos_configurados": todos_configurados,
                    "mensagem": "RobÃ´ jurÃ­dico configurado corretamente" if todos_configurados else "ConfiguraÃ§Ã£o incompleta. Verifique as variÃ¡veis de ambiente e arquivos necessÃ¡rios."
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao verificar status do robÃ´ jurÃ­dico: {str(e)}",
                "data": {}
            }