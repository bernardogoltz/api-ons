LIMITE_DIAS = 90

URL_BASE = 'https://apicarga.ons.org.br/prd/cargaverificada'

AREAS_CARGA: dict[str, tuple[str, ...]] = {
    'Submercado': ('SECO', 'N', 'NE', 'S'),
    'Área Geoelétrica': (
        'BASE', 'MA', 'DF', 'GO', 'MS', 'AM', 'AP', 'RR', 'PI', 'TON', 'AC',
        'RS', 'SP', 'MT', 'TOCO', 'BAOE', 'PBRN', 'PR', 'ES', 'MG', 'SC',
        'CE', 'RO', 'PA', 'RJ', 'ALPE',
    ),
    'Perdas': ('PEN', 'PES', 'PENE', 'PESE'),
}
