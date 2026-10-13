"""Utilitários para divisão de períodos de datas."""
import pandas as pd

from api_ons.config import LIMITE_DIAS


def trimestres(
    dat_inicio: str, 
    dat_fim: str) -> list[tuple[str, str]]:
    """Quebra o período em trimestres se exceder trimestre

    Args:
        dat_inicio: 'YYYY-MM-DD'.
        dat_fim: 'YYYY-MM-DD'.
    Returns:
        Lista de tuplas (início, fim).
    Raises:
        ValueError: Data inválida ou início maior que fim.
    """
    inicio = pd.to_datetime(dat_inicio, format='%Y-%m-%d')
    fim = pd.to_datetime(dat_fim, format='%Y-%m-%d')
    if inicio > fim:
        raise ValueError('dat_inicio não pode ser maior que dat_fim')
    if (fim - inicio).days <= LIMITE_DIAS:
        return [(dat_inicio, dat_fim)]

    quebras = pd.date_range(inicio, fim, freq='QS-MAR', inclusive='neither')
    limites = pd.DatetimeIndex([inicio, *quebras, fim]).strftime('%Y-%m-%d')
    return list(zip(limites[:-1], limites[1:]))
