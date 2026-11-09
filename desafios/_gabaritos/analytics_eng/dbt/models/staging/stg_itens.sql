select
    id_pedido as pedido_id,
    produto,
    quantidade,
    {{ centavos_para_reais('preco_unitario_centavos') }} as preco_unitario,
    {{ centavos_para_reais('quantidade * preco_unitario_centavos') }} as valor_item
from {{ source('loja', 'itens_pedido') }}
