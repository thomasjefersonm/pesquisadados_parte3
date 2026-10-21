-- Banco de dados de ORIGEM (LojaDB) - PostgreSQL externo ao Databricks
-- Executar uma única vez no SQL Editor do Supabase / Neon (ou psql).
-- Mesmo DDL e mesmos dados dos trabalhos 1 e 2.

DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
  id_cliente INT          NOT NULL PRIMARY KEY,
  nome       VARCHAR(100) NOT NULL,
  cidade     VARCHAR(100),
  uf         CHAR(2)
);

CREATE TABLE pedidos (
  id_pedido      INT            NOT NULL PRIMARY KEY,
  id_cliente     INT            NOT NULL REFERENCES clientes (id_cliente),
  produto        VARCHAR(100)   NOT NULL,
  quantidade     INT            NOT NULL,
  valor_unitario DECIMAL(10,2)  NOT NULL,
  data_pedido    DATE           NOT NULL,
  status         VARCHAR(20)    NOT NULL
);

INSERT INTO clientes VALUES
  (1, 'Ana Souza',  'Criciúma',      'SC'),
  (2, 'Bruno Lima', 'Florianópolis', 'SC'),
  (3, 'Carla Dias', 'Porto Alegre',  'RS'),
  (4, 'Diego Melo', 'Curitiba',      'PR');

INSERT INTO pedidos VALUES
  (101, 1, 'Notebook', 1, 4500.00, DATE '2026-09-01', 'PAGO'),
  (102, 2, 'Mouse',    2,   80.00, DATE '2026-09-02', 'PAGO'),
  (103, 3, 'Monitor',  1, 1200.00, DATE '2026-09-03', 'PENDENTE'),
  (104, 1, 'Teclado',  1,  250.00, DATE '2026-09-05', 'PENDENTE'),
  (105, 4, 'Headset',  1,  300.00, DATE '2026-09-06', 'CANCELADO');

SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
