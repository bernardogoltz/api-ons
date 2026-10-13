"""Funções para consultar a API de carga verificada do ONS."""
from urllib.parse import ParseResult, urlencode, urlparse

import httpx
import pandas as pd

from api_ons.config import AREAS_CARGA, URL_BASE
from api_ons.periodos import trimestres




def normalizar_area(area: str) -> str:
    """Remove espaços e converte para maiúsculas."""
    return area.strip().upper()


def validar_area(area: str) -> None:
    """Raises:
        ValueError: Área fora de config.AREAS_CARGA.
    """
    if not any(area in areas for areas in AREAS_CARGA.values()):
        raise ValueError(f'Área inválida: {area}')


def formatar_request(
    dat_inicio: str,
    dat_fim: str,
    area: str,
) -> ParseResult | list[ParseResult]:
    """Monta a(s) URL(s) da requisição; lista se o período exceder o limite."""
    urls = [
        urlparse(f'{URL_BASE}?' + urlencode({
            'dat_inicio': inicio,
            'dat_fim': fim,
            'cod_areacarga': area,
        }))
        for inicio, fim in trimestres(dat_inicio, dat_fim)
    ]
    return urls[0] if len(urls) == 1 else urls


def formatar_requests(
    dat_inicio: str,
    dat_fim: str,
    areas: list[str],
) -> list[ParseResult]:
    """Monta as URLs de todas as áreas, achatando períodos quebrados."""
    urls: list[ParseResult] = []
    for area in areas:
        url = formatar_request(dat_inicio, dat_fim, area)
        urls.extend(url if isinstance(url, list) else [url])
    return urls


def buscar_carga(
    dat_inicio: str,
    dat_fim: str,
    areas: list[str],
) -> list[dict]:
    """Busca a carga verificada das áreas e retorna o json das respostas."""
    areas = [normalizar_area(a) for a in areas]
    for area in areas:
        validar_area(area)

    registros: list[dict] = []
    with httpx.Client(timeout=60) as client:
        for url in formatar_requests(dat_inicio, dat_fim, areas):
            resposta = client.get(url.geturl())
            resposta.raise_for_status()
            registros.extend(resposta.json())
    return registros

