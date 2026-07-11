from sqlalchemy import create_engine

def carregar_para_postgres(df_limpo, db_usuario, db_senha, db_host, db_porta, db_nome):
    # Adicionamos o {db_porta} na string e o parâmetro client_encoding
    engine = create_engine(f'postgresql://{db_usuario}:{db_senha}@{db_host}:{db_porta}/{db_nome}?client_encoding=utf8')
    
    try:
        df_limpo.to_sql('fato_pecas_colhedora', engine, if_exists='append', index=False)
        print(f"Carga concluída com sucesso! {len(df_limpo)} peças inseridas no banco de dados.")
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")