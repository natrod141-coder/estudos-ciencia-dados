select
    id as pedido_id,
    id_cliente as cliente_id,
    cast(criado_em as date) as data_pedido,
    lower(trim(status)) as status
from {{ source('loja', 'pedidos') }}
where id_cliente <> 0  -- pedidos de teste da equipe
