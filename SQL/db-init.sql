CREATE TABLE dim_maquina (
    id_maquina SERIAL PRIMARY KEY,
    modelo VARCHAR(50) UNIQUE NOT NULL,
    tipo VARCHAR(50)
);

CREATE TABLE fato_pecas_colhedora (
    codigo_peca VARCHAR(50) PRIMARY KEY,
    id_maquina INT REFERENCES dim_maquina(id_maquina),
    descricao VARCHAR(255) NOT NULL,
    categoria VARCHAR(100),
    preco_estimado DECIMAL(10, 2),
    data_extracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);