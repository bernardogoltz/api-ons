"""
    dat_inicio [str] = '2021-01-01'
    dat_fim [str] = '2021-02-01'
    
    se maior que 90 dias quebra em trimestres 
    
    [(2021-01-01,2021-03-01),
    (2021-03-01,2021-06-01],
    (2021-06-01,2021-07-01)]
""" 
import pytest 

from api_ons.periodos import trimestres

def test_quebra_em_trimestres_quando_maior_que_90_dias():
    resultado = trimestres('2021-01-01', '2021-07-01')
    assert resultado == [
        ('2021-01-01', '2021-03-01'),
        ('2021-03-01', '2021-06-01'),
        ('2021-06-01', '2021-07-01'),
    ]

def test_data_inicio_nao_pode_ser_maior_que_data_fim():
    with pytest.raises(ValueError):
        trimestres('2021-02-01', '2021-01-01')


def test_nao_quebra_quando_ate_90_dias():
    resultado = trimestres('2021-01-01', '2021-02-01')
    assert resultado == [('2021-01-01', '2021-02-01')]


@pytest.mark.parametrize('dat_inicio, dat_fim', [
    ('01/01/2021', '2021-02-01'),
    ('2021-01-01', '01-02-2021'),
    ('2021-13-01', '2021-02-01'),
    ('abc', '2021-02-01'),
])
def test_formato_de_data_invalido(dat_inicio, dat_fim):
    with pytest.raises(ValueError):
        trimestres(dat_inicio, dat_fim)
