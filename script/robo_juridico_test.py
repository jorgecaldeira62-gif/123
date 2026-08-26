"""
Script de teste para o robÃ´ jurÃ­dico.
Demonstra como executar o robÃ´ programaticamente.
"""

import sys
import os
import json
from datetime import datetime

# Adiciona o caminho do projeto ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "../robo-juridico"))

def main():
    """
    FunÃ§Ã£o principal para executar o teste do robÃ´ jurÃ­dico.
    """
    print("ð¤ Iniciando teste do RobÃ´ JurÃ­dico")
    print(f"ð Data e hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("â" * 50)
    
    try:
        # Importa a classe do robÃ´ jurÃ­dico
        from robo_juridico_api import RoboJuridico
        
        # Cria uma instÃ¢ncia do robÃ´
        robo = RoboJuridico()
        
        # Executa o robÃ´
        print("ð Executando robÃ´ jurÃ­dico...")
        resultado = robo.executar()
        
        # Exibe os resultados
        print("\nð Resultados:")
        print("â" * 50)
        
        if resultado["sucesso"]:
            print(f"â Sucesso: {resultado['mensagem']}")
            
            # EstatÃ­sticas
            estatisticas = resultado['estatisticas']
            print(f"\nð EstatÃ­sticas:")
            print(f"  Total de publicaÃ§Ãµes: {estatisticas['total_publicacoes']}")
            print(f"  Processadas com sucesso: {estatisticas['processadas']}")
            print(f"  Com erro: {estatisticas['com_erro']}")
            print(f"  Ignoradas: {estatisticas['ignoradas']}")
            
            # Resultados detalhados
            if resultado['resultados']:
                print(f"\nð Detalhes das publicaÃ§Ãµes:")
                for r in resultado['resultados']:
                    status_emoji = "â" if r["status"] == "concluÃ­do" else "â ï¸" if "erro" in r["status"] else "â¹ï¸"
                    print(f"  {status_emoji} {r['processo']}: {r['status']}")
                    
                    if r['erros']:
                        for erro in r['erros']:
                            print(f"    â {erro}")
        else:
            print(f"â Erro: {resultado.get('erro', 'Erro desconhecido')}")
            
        # Salva os resultados em um arquivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resultado_robo_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        
        print(f"\nð¾ Resultados salvos em: {filename}")
        
    except ImportError as e:
        print(f"â Erro de importaÃ§Ã£o: {e}")
        print("Verifique se o caminho do robÃ´ jurÃ­dico estÃ¡ correto e todos os mÃ³dulos estÃ£o instalados.")
        sys.exit(1)
        
    except Exception as e:
        print(f"â Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()