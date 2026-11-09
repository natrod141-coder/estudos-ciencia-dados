with aprovados as (
    select
        cliente_id,
        min(data_pedido) as primeiro_pedido,
        count(*) as pedidos_aprovados,
        sum(valor_total) as valor_aprovado
    from {{ ref('fct_pedidos') }}
    where status = 'aprovado'
    group by cliente_id
)

-- left join a partir dos clientes: quem nunca comprou também aparece
select
    c.cliente_id,
    c.nome,
    c.uf,
    r.regiao,
    a.primeiro_pedido,
    coalesce(a.pedidos_aprovados, 0) as pedidos_aprovados,
    coalesce(a.valor_aprovado, 0) as valor_aprovado
from {{ ref('stg_clientes') }} as c
left join aprovados as a on a.cliente_id = c.cliente_id
left join {{ ref('uf_regiao') }} as r on r.uf = c.uf
