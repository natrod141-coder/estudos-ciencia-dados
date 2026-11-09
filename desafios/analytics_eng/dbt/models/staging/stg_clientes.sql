-- Exemplo pronto de modelo de staging: uma linha por cliente, com nomes e tipos padronizados.
-- Use como referência para escrever stg_pedidos e stg_itens.

select
    id as cliente_id,
    nome,
    lower(email) as email,
    upper(uf) as uf,
    cast(criado_em as date) as data_cadastro
from {{ source('loja', 'clientes') }}
where id <> 0  -- o cliente 0 é o cadastro de teste da equipe
