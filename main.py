import pandas as pd
from ETL.extract import extrair_catalogo_profundo
from ETL.transform import limpar_dados_pecas
from ETL.load import carregar_para_postgres

def executar_pipeline():
    print("INICIANDO PIPELINE DE DADOS PECAS JD")
    
    # Inicio do catalogo
    url_alvo = 'https://partscatalog.deere.com/jdrc/navigation/equipment/14012'
    
    # Extract
    print("Iniciando catalogação via web scraping...")
    df_bruto = extrair_catalogo_profundo(url_alvo)
    
    # Se erro
    if df_bruto.empty:
        print("Erro: A extração não retornou dados.")
        return         
    print(f"Extração concluída: {len(df_bruto)} registros")
    
    # Transform
    df_limpo = limpar_dados_pecas(df_bruto) 
 
    # Load
    carregar_para_postgres(
        df_limpo, 
        db_usuario='usuario_catalogo', 
        db_senha='pecas', 
        db_host='localhost', 
        db_porta='5433',          
        db_nome='catalogo_jd'
    )
   


if __name__ == "__main__":
    executar_pipeline()