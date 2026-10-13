"""
pd.DataFrame()
    - cod_areacarga
    - grupo @ (config.AREAS_CARGA.keys())
    "val_cargaglobal": 3017.382,
    "val_cargaglobalcons": 3017.382,
    "val_cargaglobalsmmgd": 3004.592,
    "val_cargasupervisionada": 2727.4866,
    "val_carganaosupervisionada": 277.1055,
    "val_cargammgd": 12.79,
    "val_consistencia": 0
    
src/tests/fixtures
"""

import json
from pathlib import Path

import pandas as pd
import pytest

from api_ons.config import AREAS_CARGA
from api_ons.transform import gerar_df_carga

FIXTURES = Path(__file__).parent / "fixtures"

COLUNAS_VALORES = [
    "val_cargaglobal",
    "val_cargaglobalcons",
    "val_cargaglobalsmmgd",
    "val_cargasupervisionada",
    "val_carganaosupervisionada",
    "val_cargammgd",
    "val_consistencia",
]


def carregar(nome: str) -> list[dict]:
    return json.loads((FIXTURES / f"carga_{nome}.json").read_text())


def test_retorna_dataframe_com_uma_linha_por_registro():
    registros = carregar("rs")

    df = gerar_df_carga(registros)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == len(registros)


def test_contem_cod_areacarga_grupo_e_colunas_de_valores():
    df = gerar_df_carga(carregar("rs"))

    assert "cod_areacarga" in df.columns
    assert "grupo" in df.columns
    assert set(COLUNAS_VALORES) <= set(df.columns)


@pytest.mark.parametrize("nome, grupo", [
    ("rs", "Área Geoelétrica"),
    ("seco", "Submercado"),
    ("pen", "Perdas"),
])
def test_grupo_e_chave_de_areas_carga(nome, grupo):
    df = gerar_df_carga(carregar(nome))

    assert grupo in AREAS_CARGA
    assert (df["grupo"] == grupo).all()
    assert df["cod_areacarga"].isin(AREAS_CARGA[grupo]).all()


def test_valores_numericos_preservados():
    df = gerar_df_carga(carregar("rs"))
    primeira = df.iloc[0]

    assert primeira["val_cargaglobal"] == pytest.approx(3017.382)
    assert primeira["val_cargaglobalcons"] == pytest.approx(3017.382)
    assert primeira["val_cargaglobalsmmgd"] == pytest.approx(3004.592)
    assert primeira["val_cargasupervisionada"] == pytest.approx(2727.4866)
    assert primeira["val_carganaosupervisionada"] == pytest.approx(277.1055)
    assert primeira["val_cargammgd"] == pytest.approx(12.79)
    assert primeira["val_consistencia"] == 0


def test_combina_varias_areas_com_grupos_distintos():
    df = gerar_df_carga(carregar("rs") + carregar("seco") + carregar("pen"))

    assert df.groupby("cod_areacarga")["grupo"].first().to_dict() == {
        "RS": "Área Geoelétrica",
        "SECO": "Submercado",
        "PEN": "Perdas",
    }


def test_resposta_vazia_gera_dataframe_vazio():
    df = gerar_df_carga(carregar("vazia"))

    assert isinstance(df, pd.DataFrame)
    assert df.empty
