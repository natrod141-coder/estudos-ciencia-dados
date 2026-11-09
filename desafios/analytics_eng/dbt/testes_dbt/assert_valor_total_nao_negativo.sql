-- Teste singular, já pronto: devolve as linhas com problema.
-- O teste passa quando a consulta não devolve nenhuma linha.

select pedido_id, valor_total
from {{ ref('fct_pedidos') }}
where valor_total < 0
