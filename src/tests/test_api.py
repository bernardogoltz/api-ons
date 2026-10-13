"""Testes de api.py.

URL:
    https://apicarga.ons.org.br/prd/cargaverificada
    ?dat_inicio=YYYY-MM-DD&dat_fim=YYYY-MM-DD&cod_areacarga=AREA

Parâmetros:
    dat_inicio, dat_fim: quebrados em trimestres por periodos.py.
    cod_areacarga: valores válidos (config.AREAS_CARGA):
        - Submercado: SECO (Sudeste/C. Oeste), N (Norte), NE (Nordeste),
          S (Sul)
        - Área Geoelétrica: BASE (Bahia/Sergipe), MA (Maranhão),
          DF (Distrito Federal), GO (Goiás), MS (Mato Grosso do Sul),
          AM (Amazonas), AP (Amapá), RR (Roraima), PI (Piauí),
          TON (Tocantins Norte), AC (Acre), RS (Rio Grande do Sul),
          SP (São Paulo), MT (Mato Grosso), TOCO (Tocantins),
          BAOE (Bahia Oeste), PBRN (Paraíba/Rio Grande do Norte),
          PR (Paraná), ES (Espírito Santo), MG (Minas Gerais),
          SC (Santa Catarina), CE (Ceará), RO (Rondônia), PA (Pará),
          RJ (Rio de Janeiro), ALPE (Alagoas/Pernambuco)
        - Perdas: PEN (Perdas Norte), PES (Perdas Sul),
          PENE (Perdas Nordeste), PESE (Perdas Sudeste)
"""
from urllib.parse import ParseResult, parse_qs

import pytest

from api_ons.api import formatar_request
from api_ons.api import formatar_requests
from api_ons.api import normalizar_area
from api_ons.api import validar_area
from api_ons.api import buscar_carga


def test_formatar_request():
    url = formatar_request("2024-01-01", "2024-03-31", "RS")

    assert isinstance(url, ParseResult)
    assert url.scheme == "https"
    assert url.netloc == "apicarga.ons.org.br"
    assert url.path == "/prd/cargaverificada"
    assert parse_qs(url.query) == {
        "dat_inicio": ["2024-01-01"],
        "dat_fim": ["2024-03-31"],
        "cod_areacarga": ["RS"],
    }



def test_formatar_request_gera_lista_quando_excede_limite_dias():
    urls = formatar_request("2021-01-01", "2021-07-01", "RS")

    assert isinstance(urls, list)
    assert all(isinstance(url, ParseResult) for url in urls)
    assert [
        (parse_qs(u.query)["dat_inicio"][0], parse_qs(u.query)["dat_fim"][0])
        for u in urls
    ] == [
        ("2021-01-01", "2021-03-01"),
        ("2021-03-01", "2021-06-01"),
        ("2021-06-01", "2021-07-01"),
    ]


def test_formatar_requests_gera_url_por_area():
    urls = formatar_requests("2024-01-01", "2024-01-31", ["RS", "SP"])

    assert len(urls) == 2
    assert [parse_qs(u.query)["cod_areacarga"][0] for u in urls] == ["RS", "SP"]


def test_validar_area_aceita_codigo_nas_tuplas_e_rejeita_invalido():
    validar_area("RS")
    validar_area("SECO")
    validar_area("PEN")
    with pytest.raises(ValueError):
        validar_area("XX")


@pytest.mark.parametrize("entrada, esperado", [
    ("rs", "RS"),
    ("  rs  ", "RS"),
    ("Seco", "SECO"),
    ("\tpbrn\n", "PBRN"),
])
def test_normalizar_area_upper_e_remove_espacos(entrada, esperado):
    assert normalizar_area(entrada) == esperado
