"""Transformação das respostas da API em DataFrame."""
import pandas as pd

from api_ons.config import AREAS_CARGA

GRUPO_POR_AREA: dict[str, str] = {
    area: grupo for grupo, areas in AREAS_CARGA.items() for area in areas
}


def gerar_df_carga(registros: list[dict]) -> pd.DataFrame:
    """Converte os registros em DataFrame, adicionando a coluna `grupo`."""
    df = pd.DataFrame(registros)
    if df.empty:
        return df
    df['grupo'] = df['cod_areacarga'].map(GRUPO_POR_AREA)
    return df
