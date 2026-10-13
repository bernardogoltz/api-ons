import pandas as pd
from IPython.display import display

from api_ons.api import buscar_carga
from api_ons.transform import gerar_df_carga

if __name__ == '__main__':
    registros = buscar_carga("2024-01-01", "2024-01-02", ["RS"])
    df = gerar_df_carga(registros)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    display(df)
