import streamlit as st

from core.metrics import compute_differences, compute_empirical_stats, compute_theoretical_stats
from core.simulation import generate_population, simulate_sample_means
from core.visualization import plot_population_hist, plot_sample_means_hist
from utils.layout import render_header, render_sidebar_controls


def main() -> None:
    st.set_page_config(page_title="Visualizador del TCL", layout="wide")
    st.markdown(
        """
        <style>
        .stApp {
            background: radial-gradient(circle at 20% 20%, #122033 0, #0b1624 35%, #070d17 100%);
            color: #e8eef7;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-left: 1.25rem;
            padding-right: 1.25rem;
        }
        /* Graficos y columnas responsivas */
        @media (max-width: 900px) {
            section[data-testid="stSidebar"] {
                width: 16rem !important;
            }
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                display: block !important;
            }
        }
        @media (max-width: 640px) {
            .block-container {
                padding-top: 1rem;
                padding-left: 0.75rem;
                padding-right: 0.75rem;
            }
            section[data-testid="stSidebar"] {
                width: 100% !important;
            }
        }
        /* Ocultar badge/boton de estado (Manage app) en la esquina inferior derecha */
        div[data-testid="stStatusWidget"],
        button[title="Manage app"],
        a[title="Manage app"],
        div[title="Manage app"] {
            display: none !important;
        }
        /* Ocultar toolbar superior completa (share, star, edit, github, menu) */
        header [data-testid="stToolbar"],
        header [data-testid="stDecoration"],
        header [data-testid="stHeader"] div:nth-child(2) {
            display: none !important;
        }
        /* Boton flotante para colapsar/mostrar barra lateral */
        div[data-testid="collapsedControl"] {
            position: fixed;
            top: 50%;
            left: 0;
            transform: translate(-40%, -50%);
            z-index: 1000;
            background: #142036;
            border: 1px solid #22365a;
            border-radius: 0 12px 12px 0;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
        }
        div[data-testid="collapsedControl"] button {
            color: #e8eef7;
            background: transparent;
            padding: 0.45rem 0.6rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    render_header()

    st.info(
        "Selecciona la distribucion y sus parametros, luego ejecuta la simulacion. "
        "Veras la poblacion sintetica y como las medias muestrales se aproximan a una curva normal."
    )

    dist_name, dist_params, sample_size, n_simulations, population_size = render_sidebar_controls()

    with st.spinner("Actualizando simulacion..."):
        population = generate_population(dist_name, dist_params, population_size)
        sample_means = simulate_sample_means(dist_name, dist_params, sample_size, n_simulations)

        pop_empirical = compute_empirical_stats(population)
        sample_empirical = compute_empirical_stats(sample_means)
        theoretical = compute_theoretical_stats(dist_name, dist_params, sample_size)

        pop_diff = compute_differences({"mean": theoretical["mean"], "std": theoretical["std"]}, pop_empirical)
        means_diff = {
            "mean": abs(sample_empirical["mean"] - theoretical["mean"]),
            "std": abs(sample_empirical["std"] - theoretical["se"]),
        }

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Distribucion poblacional sintetica**")
            st.caption("Refleja la forma original definida por los parametros elegidos.")
            fig_population = plot_population_hist(population, dist_name, dist_params)
            st.pyplot(fig_population, clear_figure=True, use_container_width=True)

        with col2:
            st.markdown("**Distribucion de medias muestrales**")
            st.caption("La curva naranja muestra la normal teorica segun el TCL.")
            fig_means = plot_sample_means_hist(
                sample_means, theoretical_mean=theoretical["mean"], theoretical_se=theoretical["se"]
            )
            st.pyplot(fig_means, clear_figure=True, use_container_width=True)

        st.markdown("---")
        st.subheader("Metricas teoricas vs empiricas")

        pop_col, means_col = st.columns(2)
        with pop_col:
            st.markdown("**Poblacion generada**")
            st.metric("Media teorica", f"{theoretical['mean']:.4f}")
            st.metric("Desviacion teorica", f"{theoretical['std']:.4f}")
            st.metric("Media empirica", f"{pop_empirical['mean']:.4f}", f"-{pop_diff.get('mean', 0):.4f}")
            st.metric(
                "Desv. empirica",
                f"{pop_empirical['std']:.4f}",
                f"-{pop_diff.get('std', 0):.4f}",
            )

        with means_col:
            st.markdown("**Medias muestrales**")
            st.metric("Media teorica (igual a poblacion)", f"{theoretical['mean']:.4f}")
            st.metric("Error estandar teorico", f"{theoretical['se']:.4f}")
            st.metric(
                "Media empirica de medias",
                f"{sample_empirical['mean']:.4f}",
                f"-{means_diff['mean']:.4f}",
            )
            st.metric(
                "Desv. empirica de medias",
                f"{sample_empirical['std']:.4f}",
                f"-{means_diff['std']:.4f}",
            )

        st.markdown(
            "Al aumentar `n`, la dispersion de las medias disminuye y la curva normal se vuelve mas angosta. "
            "Incluso cuando la poblacion es sesgada, las medias muestrales se acercan a la forma normal gracias al TCL."
        )


if __name__ == "__main__":
    main()
