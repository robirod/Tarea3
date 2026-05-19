import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

dfOperacionesPath = 'dataset_operaciones'
dfAmbientalesPath = 'dataset_ambientales'

from functionsUnidad3 import (
    importCsv,
    createCsv,
    createPkl
)

df = importCsv('dataset_set_A_aguas_residuales')

df['ratio_lodos_caudal'] = df['lodos_generados_kg_d'] / df['caudal_entrada_m3_d']
df['cumplimiento_texto'] = np.where(df['cumplimiento_norma'] == 1, 'Cumple', 'No Cumple')

colOperaciones = [
        'fecha_registro', 'planta', 'caudal_entrada_m3_d', 
        'DBO_entrada_mg_L', 'DBO_salida_mg_L', 
        'energia_aeracion_kWh', 'lodos_generados_kg_d'
    ]

colAmbientales = ['fecha_registro', 'planta', 'DBO_salida_mg_L', 'cumplimiento_norma']

createCsv(dfOperacionesPath, df, colOperaciones)
createCsv(dfAmbientalesPath, df, colAmbientales)

dfOperaciones = importCsv(dfOperacionesPath)
dfAmbientales = importCsv(dfAmbientalesPath)

createPkl('df_operaciones_persistente', dfOperaciones)

dfOperaciones['fecha_registro'] = pd.to_datetime(dfOperaciones['fecha_registro'])
dfSortOperaciones = dfOperaciones.sort_values('fecha_registro')

plantas = dfSortOperaciones['planta'].unique()

dfAmbientales['cumplimiento_norma'] = dfAmbientales['cumplimiento_norma'].astype(int)
dfSortAmbientales = dfAmbientales.sort_values('fecha_registro')

dboSalidaArray = dfSortAmbientales['DBO_salida_mg_L'].to_numpy()
sesgoDbo = stats.skew(dboSalidaArray)

figure = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Entrada y Salida DBO", 
        "Lodos por Caudal de Entrada",
        "Cumplimiento Norma",
        "Plantas Cumpliendo Normas"
    ),
    vertical_spacing=0.15,
    horizontal_spacing=0.12,
)

for planta in enumerate(plantas):
    dfPlanta = dfSortOperaciones[dfSortOperaciones['planta'] == planta]

    figure.add_trace(
        go.Scatter(
            x=dfPlanta['fecha_registro'],
            y=dfPlanta['DBO_entrada_mg_L'],
            mode='lines+markers',
            marker=dict(size=5, line=dict(width=1, color='black')),
            name=planta,
            legendgroup=planta,
            legendgrouptitle_text=planta,
            customdata=dfPlanta['DBO_salida_mg_L'],
            hovertemplate="<b>Fecha:</b> %{x}<br><b>DBO Entrada:</b> %{y} mg/L<br><b>DBO Salida:</b> %{customdata} mg/L",
        ),
        row=1, col=1
    )

    figure.add_trace(
        go.Scatter(
            x=dfPlanta['fecha_registro'],
            y=dfPlanta['caudal_entrada_m3_d'],
            mode='lines+markers',
            marker=dict(size=6, line=dict(width=1, color='black')),
            name=planta,
            legendgroup=planta,
            legendgrouptitle_text=planta,
            showlegend=False,
            customdata=dfPlanta['lodos_generados_kg_d'],
            hovertemplate="<b>Fecha:</b> %{x}<br><b>Caudal Entrada:</b> %{y} m3<br><b>Lodos de Salida:</b> %{customdata} kg"
        ),
        row=1, col=2
    )

for plantaAmb in plantas:
    dfPlantaAmb = dfSortAmbientales[dfSortAmbientales['planta'] == plantaAmb]
    markerColors = np.where(dfPlantaAmb['cumplimiento_norma'] == 1, '#2ca02c', '#d62728')

    figure.add_trace(
        go.Scatter(
            x=dfPlantaAmb['fecha_registro'],
            y=dfPlantaAmb['DBO_salida_mg_L'],
            mode='lines+markers',
            marker=dict(size=7, color=markerColors),
            name=plantaAmb,
            legendgroup=plantaAmb,
            legendgrouptitle_text=plantaAmb,
            customdata=dfPlantaAmb['cumplimiento_norma'],
            hovertemplate="<b>Fecha:</b> %{x}<br><b>DBO Salida:</b> %{y} mg/L<br><b>Cumplimiento de Normas:</b> %{customdata}",
        ),
        row=2, col=1
    )

cumplimientoNormaAmb = (dfSortAmbientales.groupby(['planta', 'cumplimiento_norma']).size().reset_index(name='cantidad'))

for norma in [1, 0]:
    message = 'Lograda' if norma == 1 else 'No logradas'
    dfNorma = cumplimientoNormaAmb[cumplimientoNormaAmb['cumplimiento_norma'] == norma]

    figure.add_trace(
        go.Bar(
            x=dfNorma['planta'],
            y=dfNorma['cantidad'],
            name=f'Norma: {message}',
            marker=dict(color='#2ca02c' if norma == 1 else '#d62728'),
            legendgroup=f"norma_{norma}",
            hovertemplate=f"<b>Planta:</b> %{{x}}<br><b>Cant. {message}:</b> %{{y}}<extra></extra>"
        ),
        row=2, col=2
    )   

figure.update_layout(
    title_text="<b>Dashboard Analítico Integrado - AquaLimpia S.A.</b>",
    title_x=0.5,
    height=850,
    margin=dict(l=80, r=80, t=100, b=80),
)

figure.update_xaxes(title_text="Fechas", row=1, col=1, type='date', tickformat='%Y-%m-%d', automargin=True)
figure.update_yaxes(title_text="DBO entrada mg/L", row=1, col=1, automargin=True)
figure.update_xaxes(title_text="Fechas", row=1, col=2, type='date', tickformat='%Y-%m-%d', automargin=True)
figure.update_yaxes(title_text="Caudal entrada m³", row=1, col=2, automargin=True)
figure.update_xaxes(title_text="Fechas", row=2, col=1, type='date', tickformat='%Y-%m-%d', automargin=True)
figure.update_yaxes(title_text="DBO salida mg/L", row=2, col=1, automargin=True)
figure.update_xaxes(title_text="Planta", row=2, col=2, automargin=True)
figure.update_yaxes(title_text="Frecuencia Muestras", row=2, col=2, automargin=True)

figure.show()