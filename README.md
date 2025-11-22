# Visualizador Interactivo del Teorema Central del Limite

Aplicacion en Python + Streamlit que demuestra de forma empirica el Teorema Central del Limite (TCL) mediante simulacion Monte Carlo. Permite elegir una distribucion poblacional (Uniforme, Exponencial o Binomial), configurar sus parametros, definir el tamano de la muestra y el numero de simulaciones, y visualizar la poblacion original junto con la distribucion de las medias muestrales y su curva normal teorica.

## Requisitos

- Python 3.9 o superior
- streamlit, numpy, matplotlib, scipy (ver `requirements.txt`)

## Instalacion

```bash
pip install -r requirements.txt
```

## Ejecucion

```bash
streamlit run app.py
```

## Que muestra la app

- Histograma de la poblacion sintetica segun la distribucion elegida.
- Histograma de las medias muestrales calculadas a partir de `k` simulaciones de tamano `n`.
- Curva normal teorica superpuesta (media poblacional y error estandar teorico `sigma / sqrt(n)`).
- Panel de metricas que contrasta valores teoricos y empiricos.

## Recordatorio del TCL

El Teorema Central del Limite establece que, al promediar muestras independientes de una poblacion con media y varianza finitas, la distribucion de las medias tiende a una normal conforme el tamano de muestra crece, independientemente de la forma original. La aplicacion permite experimentar con poblaciones simetricas o sesgadas y observar como las medias muestrales se acercan a una curva normal al incrementar `n` y `k`.
