CREATE TABLE dim_maquina (
    id_maquina SERIAL PRIMARY KEY,
    modelo VARCHAR(50) UNIQUE NOT NULL,
    tipo VARCHAR(50)
);

CREATE TABLE fato_pecas_colhedora (
    codigo_peca VARCHAR(50) PRIMARY KEY,
    descricao_curta VARCHAR(150),
    descricao_longa TEXT,
    sistema VARCHAR(255),
    subsistema TEXT
);