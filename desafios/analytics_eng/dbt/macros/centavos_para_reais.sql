-- Macro centavos_para_reais: recebe uma coluna ou expressão em centavos, como texto, e devolve
-- o SQL que converte o valor para reais, com duas casas decimais.
--
-- Num modelo, a chamada centavos_para_reais('preco_unitario_centavos'), entre chaves duplas,
-- deve gerar:  round((preco_unitario_centavos) / 100.0, 2)
--
-- Uma macro fica entre as tags macro e endmacro, escritas entre chaves com sinal de porcentagem.
-- Veja o exemplo no texto do tópico.

-- escreva a macro aqui
