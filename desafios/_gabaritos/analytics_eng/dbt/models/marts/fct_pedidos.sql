-- primeiro os itens viram uma linha por pedido; só depois entram no join
with itens_por_pedido as (
    select
        pedido_id,
        sum(quantidade) as unidades,
        sum(valor_item) as valor_total
    from {{ ref('stg_itens') }}
    group by pedido_id
)

select
    p.pedido_id,
    p.cliente_id,
    p.data_pedido,
    p.status,
    r.regiao,
    coalesce(i.unidades, 0) as unidades,
    coalesce(i.valor_total, 0) as valor_total
from {{ ref('stg_pedidos') }} as p
left join itens_por_pedido as i on i.pedido_id = p.pedido_id
left join {{ ref('stg_clientes') }} as c on c.cliente_id = p.cliente_id
left join {{ ref('uf_regiao') }} as r on r.uf = c.uf
