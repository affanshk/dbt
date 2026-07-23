{% macro model_name(source, table) -%}
{{ ('staging__' ~ source ~ '__' ~ table).lower() }}
{%- endmacro %}

{% macro ref_silver(source, table) -%}
{{ ref(model_name(source, table)) }}
{%- endmacro %}
