import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv('dataset_set_A_aguas_residuales.csv', sep=';', decimal=',')

df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])
df['cumplimiento_cat'] = df['cumplimiento_norma'].replace({1: 'Cumple', 0: 'No Cumple'})

dfSort = df.sort_values('fecha_registro')
plantas = dfSort['planta'].unique()

figure = make_subplots(
    rows=2, cols=1,
    subplot_titles=(
        "1. Tendencia Temporal: DBO de Salida por Planta", 
        "2. Cumplimiento de norma en base a cantidad a DBO de salida"
    ),
)



""" 
    Operaciones: fecha de registro, planta de tratamiento, caudal entrada, nivel DBO entrada y salida, consumo de energía aireación, cantidad de lodos generados 

    x=tiempo, y=cantidad de lodos generados respecto del caudal de entrada en el tiempo por planta



    Gestion ambiental: fecha, planta tratamiento, niveles DBO del efluente tratatdo, estado cumplimiento normativo.
    x=tiempo, y=DBO de salida, z= cumple por planta

"""

for planta in plantas:
    dfPlanta = dfSort[dfSort['planta'] == planta]
    figure.add_trace(
        go.Scatter(
            x=dfPlanta['fecha_registro'],
            y=dfPlanta['DBO_salida_mg_L'],
            mode='lines+markers',

            marker=dict(
                size=7,
                line=dict(width=2, color='black')
            ),

            customdata=dfPlanta['cumplimiento_norma'],
            name=f"{planta}",
            legendgroup="Plantas",
            legendgrouptitle_text="Plantas",
            hovertemplate="<b>Fecha:</b> %{x}<br><b>DBO Salida:</b> %{y} mg/L<br><b>Estado:</b> %{customdata}<extra></extra>",
        ),
        row=2, col=1
    )



for planta in plantas:

    dfPlanta = dfSort[dfSort['planta'] == planta]
    figure.add_trace(
        go.Scatter(
            x=dfPlanta['fecha_registro'],
            y=dfPlanta['DBO_salida_mg_L'],
            mode='lines+markers',

            marker=dict(
                size=7,
                line=dict(width=2, color='black')
            ),

            customdata=dfPlanta['cumplimiento_norma'],
            name=f"{planta}",
            legendgroup="Plantas",
            legendgrouptitle_text="Plantas",
            hovertemplate="<b>Fecha:</b> %{x}<br><b>DBO Salida:</b> %{y} mg/L<br><b>Estado:</b> %{customdata}<extra></extra>",
        ),
        row=2, col=1
    )


# Mostrar el dashboard
figure.show()