# Anatomia dos plugins

Gerado por `discovery/scripts/plugins.py`.

Papel atribuido por heuristica de nome de modulo/simbolo `[inferido]` (ordem: validacao externa > parser > gerador > regra de negocio > outro). `generico?` = existe funcao com corpo >65% similar em OUTRO plugin.

## Resumo por plugin

| plugin | arquivos | simbolos de topo | linhas | papeis |
|---|---:|---:|---:|---|
| `cadoc_3026` | 5 | 6 | 242 | gerador de saida: 2, regra de negocio: 2, outro: 1, validacao externa: 1 |
| `cadoc_3040` | 13 | 56 | 1219 | regra de negocio: 21, gerador de saida: 18, validacao externa: 8, outro: 7, parser de entrada: 2 |
| `cadoc_3044` | 10 | 47 | 966 | regra de negocio: 23, parser de entrada: 15, validacao externa: 7, outro: 2 |
| `cadoc_3050` | 7 | 31 | 759 | parser de entrada: 11, regra de negocio: 10, gerador de saida: 6, validacao externa: 3, outro: 1 |
| `cadoc_cosif` | 4 | 8 | 138 | parser de entrada: 3, validacao externa: 3, gerador de saida: 1, outro: 1 |

## Simbolos por plugin

### `cadoc_3026`

| arquivo | simbolo | tipo | papel | l. | generico? |
|---|---|---|---|---:|:-:|
| `cadoc_3026/plugin.py` | `Cadoc3026Plugin` | classe | outro | 28 | - |
| `cadoc_3026/scr3026_generator.py` | `generate_doc3026_xml` | funcao | gerador de saida | 34 | - |
| `cadoc_3026/validator_3026.py` | `validate_3026` | funcao | validacao externa | 63 | - |
| `cadoc_3026/engine/builder.py` | `build_doc3026` | funcao | gerador de saida | 48 | - |
| `cadoc_3026/engine/selector.py` | `select_conglomerados` | funcao | regra de negocio | 48 | - |
| `cadoc_3026/engine/selector.py` | `clientes_sem_conglomerado` | funcao | regra de negocio | 21 | - |

### `cadoc_3040`

| arquivo | simbolo | tipo | papel | l. | generico? |
|---|---|---|---|---:|:-:|
| `cadoc_3040/completude.py` | `modalidade_valida` | funcao | regra de negocio | 3 | - |
| `cadoc_3040/completude.py` | `leiaute_suporta_rendmes` | funcao | regra de negocio | 10 | - |
| `cadoc_3040/completude.py` | `_classe_modalidade` | funcao | regra de negocio | 4 | - |
| `cadoc_3040/completude.py` | `exige_rendmes` | funcao | regra de negocio | 18 | - |
| `cadoc_3040/completude.py` | `aplicar_rendimento` | funcao | regra de negocio | 11 | - |
| `cadoc_3040/completude.py` | `avaliar_completude` | funcao | regra de negocio | 46 | - |
| `cadoc_3040/plugin.py` | `Cadoc3040Plugin` | classe | outro | 25 | - |
| `cadoc_3040/schema.py` | `validate_field` | funcao | outro | 62 | sim |
| `cadoc_3040/schema.py` | `validate_header` | funcao | outro | 6 | - |
| `cadoc_3040/schema.py` | `validate_client` | funcao | outro | 27 | - |
| `cadoc_3040/schema.py` | `validate_operation` | funcao | outro | 54 | - |
| `cadoc_3040/scr3042_generator.py` | `generate_doc3042_xml` | funcao | gerador de saida | 57 | - |
| `cadoc_3040/scr_generator.py` | `bloco_4966_defaults` | funcao | gerador de saida | 16 | - |
| `cadoc_3040/scr_generator.py` | `_digits` | funcao | gerador de saida | 2 | - |
| `cadoc_3040/scr_generator.py` | `_dec` | funcao | gerador de saida | 4 | - |
| `cadoc_3040/scr_generator.py` | `_fmt2` | funcao | gerador de saida | 2 | - |
| `cadoc_3040/scr_generator.py` | `_class` | funcao | gerador de saida | 3 | - |
| `cadoc_3040/scr_generator.py` | `_prov` | funcao | gerador de saida | 3 | - |
| `cadoc_3040/scr_generator.py` | `_faixa_valor` | funcao | gerador de saida | 13 | - |
| `cadoc_3040/scr_generator.py` | `_build_agreg_elements` | funcao | gerador de saida | 40 | - |
| `cadoc_3040/scr_generator.py` | `compute_ipoc` | funcao | gerador de saida | 18 | - |
| `cadoc_3040/scr_generator.py` | `_cli_identity` | funcao | gerador de saida | 35 | - |
| `cadoc_3040/scr_generator.py` | `compute_ipoc_map` | funcao | gerador de saida | 23 | - |
| `cadoc_3040/scr_generator.py` | `_build_cli_element` | funcao | gerador de saida | 30 | - |
| `cadoc_3040/scr_generator.py` | `_build_op_element` | funcao | gerador de saida | 65 | - |
| `cadoc_3040/scr_generator.py` | `generate_doc3040_xml` | funcao | gerador de saida | 57 | - |
| `cadoc_3040/validator.py` | `validate_schema_3040` | funcao | validacao externa | 13 | - |
| `cadoc_3040/validator.py` | `validate_business_rules_3040` | funcao | validacao externa | 60 | - |
| `cadoc_3040/validator_3042.py` | `validate_3042` | funcao | validacao externa | 65 | - |
| `cadoc_3040/xsd_validator.py` | `_schema` | funcao | validacao externa | 2 | - |
| `cadoc_3040/xsd_validator.py` | `validate_3040_xml` | funcao | validacao externa | 16 | sim |
| `cadoc_3040/engine/builder.py` | `_dec` | funcao | gerador de saida | 4 | - |
| `cadoc_3040/engine/builder.py` | `particionar_por_cliente` | funcao | gerador de saida | 16 | - |
| `cadoc_3040/engine/builder.py` | `build_clientes` | funcao | gerador de saida | 66 | - |
| `cadoc_3040/engine/own_validator.py` | `_err` | funcao | validacao externa | 2 | - |
| `cadoc_3040/engine/own_validator.py` | `_is_error` | funcao | validacao externa | 2 | - |
| `cadoc_3040/engine/own_validator.py` | `validate_document_3040` | funcao | validacao externa | 30 | - |
| `cadoc_3040/engine/substituicao_parcial.py` | `_op_payload` | funcao | regra de negocio | 3 | - |
| `cadoc_3040/engine/substituicao_parcial.py` | `diff_3042` | funcao | regra de negocio | 71 | - |
| `cadoc_3040/engine/synthetic.py` | `_modalidade_sintetica_ok` | funcao | regra de negocio | 6 | - |
| `cadoc_3040/engine/synthetic.py` | `_rand_inicio` | funcao | regra de negocio | 4 | - |
| `cadoc_3040/engine/synthetic.py` | `_dv_mod11` | funcao | regra de negocio | 4 | - |
| `cadoc_3040/engine/synthetic.py` | `cpf_check_digits` | funcao | regra de negocio | 5 | - |
| `cadoc_3040/engine/synthetic.py` | `cnpj_check_digits` | funcao | regra de negocio | 7 | - |
| `cadoc_3040/engine/synthetic.py` | `is_valid_cpf` | funcao | regra de negocio | 4 | - |
| `cadoc_3040/engine/synthetic.py` | `is_valid_cnpj` | funcao | regra de negocio | 4 | - |
| `cadoc_3040/engine/synthetic.py` | `_gen_cpf` | funcao | regra de negocio | 3 | - |
| `cadoc_3040/engine/synthetic.py` | `_gen_cnpj` | funcao | regra de negocio | 3 | - |
| `cadoc_3040/engine/synthetic.py` | `_fmt_n2` | funcao | regra de negocio | 4 | - |
| `cadoc_3040/engine/synthetic.py` | `_fmt_field` | funcao | regra de negocio | 10 | - |
| `cadoc_3040/engine/synthetic.py` | `_build_line` | funcao | regra de negocio | 5 | - |
| `cadoc_3040/engine/synthetic.py` | `generate_synthetic_3040` | funcao | regra de negocio | 73 | - |
| `cadoc_3040/engine/transmitido_snapshot.py` | `parse_doc3040_xml` | funcao | parser de entrada | 22 | - |
| `cadoc_3040/engine/transmitido_snapshot.py` | `_parse_root` | funcao | parser de entrada | 36 | - |
| `cadoc_3040/engine/transmitido_snapshot.py` | `transmitido_3040` | funcao | outro | 37 | - |
| `cadoc_3040/engine/transmitido_snapshot.py` | `operacoes_transmitidas` | funcao | outro | 8 | - |

### `cadoc_3044`

| arquivo | simbolo | tipo | papel | l. | generico? |
|---|---|---|---|---:|:-:|
| `cadoc_3044/plugin.py` | `Cadoc3044Plugin` | classe | outro | 25 | - |
| `cadoc_3044/schema.py` | `validate_event` | funcao | outro | 42 | sim |
| `cadoc_3044/validator.py` | `validate_schema_3044` | funcao | validacao externa | 6 | - |
| `cadoc_3044/validator.py` | `validate_business_rules_3044` | funcao | validacao externa | 59 | - |
| `cadoc_3044/engine/consolidator.py` | `_to_dec` | funcao | regra de negocio | 11 | - |
| `cadoc_3044/engine/consolidator.py` | `_to_iso_date` | funcao | regra de negocio | 10 | - |
| `cadoc_3044/engine/consolidator.py` | `_lpad_class3050` | funcao | regra de negocio | 5 | - |
| `cadoc_3044/engine/consolidator.py` | `parse_ops_from_payload` | funcao | parser de entrada | 68 | - |
| `cadoc_3044/engine/consolidator.py` | `_aggregate_mov` | funcao | regra de negocio | 32 | - |
| `cadoc_3044/engine/consolidator.py` | `consolidate_ops` | funcao | regra de negocio | 65 | - |
| `cadoc_3044/engine/consolidator.py` | `normalize` | funcao | regra de negocio | 21 | - |
| `cadoc_3044/engine/consolidator.py` | `consolidate` | funcao | regra de negocio | 20 | - |
| `cadoc_3044/engine/layouts.py` | `LayoutField` | classe | parser de entrada | 11 | - |
| `cadoc_3044/engine/layouts.py` | `Layout` | classe | parser de entrada | 10 | - |
| `cadoc_3044/engine/layouts.py` | `_build_layout` | funcao | parser de entrada | 8 | - |
| `cadoc_3044/engine/layouts.py` | `get_layout` | funcao | parser de entrada | 5 | - |
| `cadoc_3044/engine/own_validator.py` | `_err` | funcao | validacao externa | 2 | - |
| `cadoc_3044/engine/own_validator.py` | `_date_only` | funcao | validacao externa | 4 | - |
| `cadoc_3044/engine/own_validator.py` | `validate_document` | funcao | validacao externa | 53 | - |
| `cadoc_3044/engine/portability_parser.py` | `_iso` | funcao | parser de entrada | 9 | - |
| `cadoc_3044/engine/portability_parser.py` | `parse_portability` | funcao | parser de entrada | 14 | - |
| `cadoc_3044/engine/positional_parser.py` | `_parse_a` | funcao | parser de entrada | 3 | - |
| `cadoc_3044/engine/positional_parser.py` | `_parse_a10` | funcao | parser de entrada | 12 | - |
| `cadoc_3044/engine/positional_parser.py` | `_parse_n` | funcao | parser de entrada | 3 | - |
| `cadoc_3044/engine/positional_parser.py` | `_parse_n2` | funcao | parser de entrada | 11 | - |
| `cadoc_3044/engine/positional_parser.py` | `_parse_field` | funcao | parser de entrada | 13 | - |
| `cadoc_3044/engine/positional_parser.py` | `parse_line` | funcao | parser de entrada | 17 | - |
| `cadoc_3044/engine/positional_parser.py` | `parse_file` | funcao | parser de entrada | 5 | - |
| `cadoc_3044/engine/positional_parser.py` | `parse_file_enumerado` | funcao | parser de entrada | 13 | - |
| `cadoc_3044/engine/rules.py` | `_dec` | funcao | regra de negocio | 7 | - |
| `cadoc_3044/engine/rules.py` | `_approx_equal` | funcao | regra de negocio | 2 | - |
| `cadoc_3044/engine/rules.py` | `_janela_limite` | funcao | regra de negocio | 10 | - |
| `cadoc_3044/engine/rules.py` | `status_to_atraso` | funcao | regra de negocio | 7 | - |
| `cadoc_3044/engine/rules.py` | `must_zero_saldo` | funcao | regra de negocio | 3 | - |
| `cadoc_3044/engine/rules.py` | `is_reneg` | funcao | regra de negocio | 2 | - |
| `cadoc_3044/engine/rules.py` | `IPOCState` | classe | regra de negocio | 16 | - |
| `cadoc_3044/engine/rules.py` | `build_states` | funcao | regra de negocio | 50 | - |
| `cadoc_3044/engine/rules.py` | `HistoryLookup` | classe | regra de negocio | 16 | - |
| `cadoc_3044/engine/rules.py` | `_build_concessoes` | funcao | regra de negocio | 28 | - |
| `cadoc_3044/engine/rules.py` | `_build_pagamentos` | funcao | regra de negocio | 44 | - |
| `cadoc_3044/engine/rules.py` | `_apply_janela_movimentos` | funcao | regra de negocio | 18 | - |
| `cadoc_3044/engine/rules.py` | `_apply_troca_titularidade` | funcao | regra de negocio | 42 | - |
| `cadoc_3044/engine/rules.py` | `build_operations` | funcao | regra de negocio | 55 | - |
| `cadoc_3044/engine/rules.py` | `build_carta_fianca_operations` | funcao | regra de negocio | 22 | - |
| `cadoc_3044/engine/rules.py` | `operacoes_por_role` | funcao | regra de negocio | 8 | - |
| `cadoc_3044/engine/validator_client.py` | `ValidatorClient` | classe | validacao externa | 73 | - |
| `cadoc_3044/engine/validator_client.py` | `validador_meta` | funcao | validacao externa | 6 | - |

### `cadoc_3050`

| arquivo | simbolo | tipo | papel | l. | generico? |
|---|---|---|---|---:|:-:|
| `cadoc_3050/equivalencia.py` | `EquivalenciaRule` | classe | regra de negocio | 10 | - |
| `cadoc_3050/equivalencia.py` | `_normalize_label` | funcao | regra de negocio | 11 | - |
| `cadoc_3050/equivalencia.py` | `resolve_label` | funcao | regra de negocio | 10 | - |
| `cadoc_3050/equivalencia.py` | `_parse_modalidade_3040` | funcao | parser de entrada | 17 | - |
| `cadoc_3050/equivalencia.py` | `codigos_3040_para_modalidade` | funcao | regra de negocio | 23 | - |
| `cadoc_3050/equivalencia.py` | `coverage` | funcao | regra de negocio | 10 | - |
| `cadoc_3050/layout_v11.py` | `_xsd_root` | funcao | validacao externa | 2 | - |
| `cadoc_3050/layout_v11.py` | `_load` | funcao | parser de entrada | 43 | - |
| `cadoc_3050/layout_v11.py` | `_type_scales` | funcao | parser de entrada | 23 | - |
| `cadoc_3050/layout_v11.py` | `_load_scales` | funcao | parser de entrada | 26 | - |
| `cadoc_3050/layout_v11.py` | `attr_scale` | funcao | parser de entrada | 8 | - |
| `cadoc_3050/layout_v11.py` | `all_modalities` | funcao | parser de entrada | 7 | - |
| `cadoc_3050/layout_v11.py` | `attrs_for_model` | funcao | parser de entrada | 21 | - |
| `cadoc_3050/layout_v11.py` | `model_of` | funcao | parser de entrada | 7 | - |
| `cadoc_3050/layout_v11.py` | `model_for` | funcao | parser de entrada | 28 | - |
| `cadoc_3050/layout_v11.py` | `container_children` | funcao | parser de entrada | 9 | - |
| `cadoc_3050/layout_v11.py` | `placement_for` | funcao | parser de entrada | 61 | - |
| `cadoc_3050/plugin.py` | `Cadoc3050Plugin` | classe | outro | 28 | - |
| `cadoc_3050/scr3050_generator.py` | `_fmt_attr` | funcao | gerador de saida | 19 | - |
| `cadoc_3050/scr3050_generator.py` | `_emit_modalidades` | funcao | gerador de saida | 8 | - |
| `cadoc_3050/scr3050_generator.py` | `_emit_credito` | funcao | gerador de saida | 22 | - |
| `cadoc_3050/scr3050_generator.py` | `generate_doc3050_xml` | funcao | gerador de saida | 52 | - |
| `cadoc_3050/xsd_validator_3050.py` | `_schema` | funcao | validacao externa | 2 | - |
| `cadoc_3050/xsd_validator_3050.py` | `validate_3050_xml` | funcao | validacao externa | 16 | sim |
| `cadoc_3050/engine/aggregator.py` | `_q` | funcao | regra de negocio | 9 | - |
| `cadoc_3050/engine/aggregator.py` | `_weighted_mean` | funcao | regra de negocio | 10 | - |
| `cadoc_3050/engine/aggregator.py` | `_composite_charge` | funcao | regra de negocio | 22 | - |
| `cadoc_3050/engine/aggregator.py` | `_compute` | funcao | regra de negocio | 96 | - |
| `cadoc_3050/engine/aggregator.py` | `aggregate` | funcao | regra de negocio | 43 | - |
| `cadoc_3050/engine/builder.py` | `normalize_tel_contato` | funcao | gerador de saida | 32 | - |
| `cadoc_3050/engine/builder.py` | `build_doc_txb` | funcao | gerador de saida | 84 | - |

### `cadoc_cosif`

| arquivo | simbolo | tipo | papel | l. | generico? |
|---|---|---|---|---:|:-:|
| `cadoc_cosif/cosif_generator.py` | `gerar_cosif_xml` | funcao | gerador de saida | 14 | - |
| `cadoc_cosif/cosif_parser.py` | `_to_dec` | funcao | parser de entrada | 13 | - |
| `cadoc_cosif/cosif_parser.py` | `parse_cosif_xml` | funcao | parser de entrada | 26 | - |
| `cadoc_cosif/cosif_parser.py` | `parse_9011_json` | funcao | parser de entrada | 21 | - |
| `cadoc_cosif/plugin.py` | `CadocCosifPlugin` | classe | outro | 37 | - |
| `cadoc_cosif/xsd_validator_cosif.py` | `_schema_for` | funcao | validacao externa | 5 | - |
| `cadoc_cosif/xsd_validator_cosif.py` | `has_schema` | funcao | validacao externa | 3 | - |
| `cadoc_cosif/xsd_validator_cosif.py` | `validate_cosif_leiaute` | funcao | validacao externa | 19 | sim |

## Funcoes com corpo similar entre plugins diferentes (4)

| similaridade | A | B | papel |
|---:|---|---|---|
| 100% | `cadoc_3040::validate_3040_xml` | `cadoc_3050::validate_3050_xml` | validacao externa |
| 86% | `cadoc_3040::validate_3040_xml` | `cadoc_cosif::validate_cosif_leiaute` | validacao externa |
| 86% | `cadoc_3050::validate_3050_xml` | `cadoc_cosif::validate_cosif_leiaute` | validacao externa |
| 68% | `cadoc_3040::validate_field` | `cadoc_3044::validate_event` | outro |

## Mesmo nome de simbolo em 2+ plugins (4)

| simbolo | plugins |
|---|---|
| `_dec` | cadoc_3040, cadoc_3044 |
| `_err` | cadoc_3040, cadoc_3044 |
| `_schema` | cadoc_3040, cadoc_3050 |
| `_to_dec` | cadoc_3044, cadoc_cosif |
