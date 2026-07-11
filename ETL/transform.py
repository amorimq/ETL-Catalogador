import pandas as pd
import unicodedata
import re

# Remover caracteres especiais
def remover_acentos_e_especiais(texto):
    if pd.isna(texto):
        return texto   
    texto = str(texto).strip()   
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto = re.sub(r'[^a-zA-Z0-9\s]', '', texto)
    return texto

def limpar_dados_pecas(df_bruto):
    print("Iniciando tratamento de dados e padronização...")
    
    df_limpo = df_bruto.copy()
    df_limpo.dropna(subset=['codigo_peca'], inplace=True)
    
    colunas_texto = ['codigo_peca', 'descricao', 'sistema', 'subsistema']
    for col in colunas_texto:
        df_limpo[col] = df_limpo[col].apply(remover_acentos_e_especiais).str.upper()
        
    df_limpo['descricao_curta'] = df_limpo['descricao'].str.split().str[0]
    df_limpo.rename(columns={'descricao': 'descricao_longa'}, inplace=True)
    colunas_finais = ['codigo_peca', 'descricao_curta', 'descricao_longa', 'sistema', 'subsistema']
    df_limpo = df_limpo[colunas_finais]
    
    tamanho_antes = len(df_limpo)
    df_limpo = df_limpo.drop_duplicates(subset=['codigo_peca'], keep='first')
    tamanho_depois = len(df_limpo)
    
    duplicadas_removidas = tamanho_antes - tamanho_depois
    
    if duplicadas_removidas > 0:
        print(f"Tratamento de dados: {duplicadas_removidas} peças duplicadas foram bloqueadas e removidas.")
        
    print(f"Dados saneados e padronizados com sucesso. {len(df_limpo)} peças catalogadas.")  
    return df_limpo