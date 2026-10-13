# API-ONS
- 5%
Módulo python para ler dados da API de carga verif. do ONS em formato pd.DataFrame()

- [Dicionário de Dados PDF](https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/carga_verificada_tm/DicionarioDados_Carga_Verificada.pdf)
- **Request url:**
```bash
https://apicarga.ons.org.br/prd/cargaverificada?dat_inicio=YYYY-MM-DD&dat_fim=YYYY-MM-DD&cod_areacarga=AREA
```

## Estrutura
```
src
    api_ons
        periodos.py
    tests
        test_periodos.py
```
