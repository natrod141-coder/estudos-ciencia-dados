{% macro centavos_para_reais(expressao) %}
    round(({{ expressao }}) / 100.0, 2)
{% endmacro %}
