from typing import Dict, Tuple

import streamlit as st


def render_header() -> None:
    st.title("Visualizador Interactivo del Teorema Central del Limite")
    st.markdown(
        "Explora como las medias de muchas muestras independientes se acercan a una distribucion normal, "
        "sin importar la forma inicial de la poblacion. Ajusta la distribucion, el tamano de muestra y "
        "el numero de simulaciones para ver el TCL en accion."
    )


def _uniform_controls() -> Dict[str, float]:
    st.subheader("Parametros Uniforme")
    a = st.slider("Limite inferior (a)", -10.0, 10.0, 0.0, step=0.5, help="Valor minimo de la distribucion.")
    b = st.slider(
        "Limite superior (b)",
        a + 0.5,
        20.0,
        max(a + 1.0, 5.0),
        step=0.5,
        help="Debe ser mayor que a; controla la amplitud.",
    )
    return {"a": float(a), "b": float(b)}


def _exponential_controls() -> Dict[str, float]:
    st.subheader("Parametros Exponencial")
    lam = st.slider("Tasa (lambda)", 0.1, 5.0, 1.0, step=0.1, help="Mayor lambda implica colas mas cortas.")
    return {"lam": float(lam)}


def _binomial_controls() -> Dict[str, float]:
    st.subheader("Parametros Binomial")
    n_trials = st.slider("Numero de ensayos (n)", 1, 60, 20, step=1, help="Cantidad de ensayos por prueba.")
    p = st.slider("Probabilidad de exito (p)", 0.01, 0.99, 0.5, step=0.01, help="Probabilidad en cada ensayo.")
    return {"n_trials": int(n_trials), "p": float(p)}


def render_sidebar_controls() -> Tuple[str, Dict[str, float], int, int, int]:
    dist_name = st.sidebar.selectbox(
        "Distribucion poblacional",
        ["Uniforme", "Exponencial", "Binomial"],
        help="Elige la forma base de la poblacion.",
    )

    with st.sidebar:
        if dist_name == "Uniforme":
            dist_params = _uniform_controls()
        elif dist_name == "Exponencial":
            dist_params = _exponential_controls()
        else:
            dist_params = _binomial_controls()

    sample_size = st.sidebar.slider(
        "Tamano de la muestra (n)",
        5,
        500,
        40,
        step=5,
        help="Medias de muestras mas grandes tienen menor dispersion (error estandar menor).",
    )
    n_simulations = st.sidebar.slider(
        "Numero de simulaciones (k)",
        100,
        5000,
        1000,
        step=100,
        help="Cuantas medias muestrales se generan para el histograma.",
    )
    population_size = st.sidebar.slider(
        "Tamano de poblacion para graficar",
        5000,
        200000,
        100000,
        step=5000,
        help="Cantidad de datos sinteticos para visualizar la distribucion original.",
    )
    return dist_name, dist_params, sample_size, n_simulations, population_size
