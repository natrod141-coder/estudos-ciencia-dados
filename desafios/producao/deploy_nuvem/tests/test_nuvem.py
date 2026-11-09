import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from pydantic import SecretStr, ValidationError

from solucao import Configuracao, acompanhar_orcamento, custo_mensal, decidir_lancamento, linha_de_log

PRECOS = json.loads((Path(__file__).parent.parent / "data" / "precos_cloud_run.json").read_text(encoding="utf-8"))
CHAVE = "chave-de-teste-1234567890"
CHAVE_ANTHROPIC = "sk-ant-teste-que-nao-pode-vazar"
SAO_PAULO = timezone(timedelta(hours=-3))


@pytest.fixture(autouse=True)
def ambiente_limpo(monkeypatch):
    """Cada teste começa sem as variáveis da API, mesmo que o seu computador tenha alguma."""
    for nome in ("CHAVE_API", "ANTHROPIC_API_KEY", "PORT", "NIVEL_LOG", "K_REVISION", "MAX_LOTE"):
        monkeypatch.delenv(nome, raising=False)
    monkeypatch.setenv("CHAVE_API", CHAVE)
    monkeypatch.setenv("ANTHROPIC_API_KEY", CHAVE_ANTHROPIC)


def test_configuracao_le_o_ambiente(monkeypatch):
    monkeypatch.setenv("PORT", "9000")
    monkeypatch.setenv("NIVEL_LOG", "DEBUG")
    monkeypatch.setenv("K_REVISION", "api-cancelamento-00007-xyz")
    config = Configuracao()
    assert config.port == 9000, "O valor de uma variável de ambiente é sempre texto: converta para int."
    assert config.nivel_log == "DEBUG"
    assert config.revisao == "api-cancelamento-00007-xyz", "O Cloud Run informa a revisão em K_REVISION."
    assert config.chave_api.get_secret_value() == CHAVE
    assert config.anthropic_api_key.get_secret_value() == CHAVE_ANTHROPIC


def test_configuracao_padroes():
    config = Configuracao()
    assert (config.port, config.nivel_log, config.revisao, config.max_lote) == (8080, "INFO", "local", 100)


@pytest.mark.parametrize("nome, valor", [
    ("CHAVE_API", None),
    ("ANTHROPIC_API_KEY", None),
    ("CHAVE_API", "curta-demais"),
    ("PORT", "oitenta"),
    ("PORT", "70000"),
    ("NIVEL_LOG", "VERBOSO"),
])
def test_configuracao_invalida_impede_a_subida(monkeypatch, nome, valor):
    if valor is None:
        monkeypatch.delenv(nome)
    else:
        monkeypatch.setenv(nome, valor)
    with pytest.raises(ValidationError) as erro:
        Configuracao()
    if valor:
        assert valor not in str(erro.value), "A mensagem de erro vai para o registro: ela não pode mostrar o valor recebido."


def test_segredos_nao_aparecem():
    config = Configuracao()
    assert isinstance(config.chave_api, SecretStr) and isinstance(config.anthropic_api_key, SecretStr)
    for texto in (repr(config), str(config), config.model_dump_json()):
        assert CHAVE not in texto and CHAVE_ANTHROPIC not in texto, "Use SecretStr para as chaves."


def test_linha_de_log():
    momento = datetime(2026, 11, 9, 11, 30, 0, 250000, tzinfo=SAO_PAULO)
    linha = linha_de_log("INFO", "Previsão concluída", momento, rota="/previsoes", duracao_ms=12.5, risco="medio")
    assert "\n" not in linha, "Um registro por linha: é assim que a plataforma separa um do outro."
    assert "Previsão" in linha, "Use ensure_ascii=False para manter os acentos legíveis."
    assert json.loads(linha) == {
        "severity": "INFO",
        "message": "Previsão concluída",
        "time": "2026-11-09T14:30:00.250Z",
        "rota": "/previsoes",
        "duracao_ms": 12.5,
        "risco": "medio",
    }


def test_log_esconde_segredos_e_exige_fuso():
    momento = datetime(2026, 11, 9, 14, 30, tzinfo=timezone.utc)
    registro = json.loads(linha_de_log("WARNING", "Chave recusada", momento, chave_recebida="abc123", Token_GitHub="ghp_x", usuario="ana"))
    assert registro["chave_recebida"] == "***" and registro["Token_GitHub"] == "***" and registro["usuario"] == "ana"
    with pytest.raises(ValueError):
        linha_de_log("INFO", "Sem fuso", datetime(2026, 11, 9, 14, 30))
    with pytest.raises(ValueError):
        linha_de_log("VERBOSO", "Nível que não existe", momento)


def test_custo_dentro_da_cota_gratuita():
    uso = {"requisicoes": 300_000, "duracao_media_s": 0.2, "concorrencia": 1, "vcpu": 1, "memoria_gib": 0.5, "instancias_minimas": 0}
    assert custo_mensal(uso, PRECOS) == {"cpu": 0, "memoria": 0, "requisicoes": 0, "ociosidade": 0, "total": 0}


def test_custo_concorrencia_e_instancias_minimas():
    uso = {"requisicoes": 10_000_000, "duracao_media_s": 0.4, "concorrencia": 1, "vcpu": 1, "memoria_gib": 0.5, "instancias_minimas": 0}
    assert custo_mensal(uso, PRECOS) == {"cpu": 91.68, "memoria": 4.1, "requisicoes": 3.2, "ociosidade": 0, "total": 98.98}
    compartilhando = custo_mensal({**uso, "concorrencia": 5}, PRECOS)
    assert compartilhando["total"] == 18.18, "Com 5 requisições por instância, o tempo de instância cai para um quinto."
    sempre_ligada = {"requisicoes": 300_000, "duracao_media_s": 0.2, "concorrencia": 1, "vcpu": 1, "memoria_gib": 1, "instancias_minimas": 1}
    assert custo_mensal(sempre_ligada, PRECOS) == {"cpu": 0, "memoria": 0, "requisicoes": 0, "ociosidade": 12.66, "total": 12.66}


def test_acompanhar_orcamento():
    assert acompanhar_orcamento([1.55] * 12, orcamento=50, dias_no_mes=30) == {
        "gasto": 18.6, "projecao": 46.5, "alertas": [], "alertas_previstos": [0.5, 0.9],
    }
    assert acompanhar_orcamento([2.6] * 20, orcamento=50, dias_no_mes=30) == {
        "gasto": 52.0, "projecao": 78.0, "alertas": [0.5, 0.9, 1.0], "alertas_previstos": [0.5, 0.9, 1.0],
    }


def test_decidir_lancamento():
    atual = {"requisicoes": 20_000, "erros": 40, "latencia_p95_ms": 180}
    assert decidir_lancamento(atual, {"requisicoes": 300, "erros": 0, "latencia_p95_ms": 150})[0] == "aguardar"
    decisao, motivo = decidir_lancamento(atual, {"requisicoes": 1_000, "erros": 30, "latencia_p95_ms": 190})
    assert decisao == "reverter" and "erro" in motivo.lower()
    decisao, motivo = decidir_lancamento(atual, {"requisicoes": 1_000, "erros": 3, "latencia_p95_ms": 260})
    assert decisao == "reverter" and "latência" in motivo.lower()
    assert decidir_lancamento(atual, {"requisicoes": 1_000, "erros": 5, "latencia_p95_ms": 200})[0] == "promover"
    assert decidir_lancamento(atual, {"requisicoes": 1_000, "erros": 5, "latencia_p95_ms": 200}, minimo_de_requisicoes=2_000)[0] == "aguardar"
