from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde, norm, skew


def _describe_shape(data: np.ndarray) -> str:
    skewness = skew(data)
    if abs(skewness) < 0.1:
        return "Simetrica"
    if skewness > 0:
        return "Sesgo positivo (cola a la derecha)"
    return "Sesgo negativo (cola a la izquierda)"


def plot_population_hist(population_data: np.ndarray, dist_name: str, dist_params: Dict[str, float]) -> plt.Figure:
    """Histograma de la poblacion generada con curva suavizada."""
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    fig.patch.set_facecolor("#0d1523")
    ax.set_facecolor("#0d1523")

    counts, bins, patches = ax.hist(
        population_data,
        bins=40,
        color="#6da7ff",
        edgecolor="#dbe9ff",
        alpha=0.8,
        density=True,
        label="Poblacion",
    )

    # Suavizado con KDE para dar una lectura mas estetica.
    kde = gaussian_kde(population_data)
    xs = np.linspace(min(population_data), max(population_data), 300)
    ax.plot(xs, kde(xs), color="#ffeb3b", linewidth=2.6, label="Suavizado KDE")

    # Linea de la media poblacional empirica
    mean_val = np.mean(population_data)
    ax.axvline(mean_val, color="#ff7043", linestyle="--", linewidth=2.2, label="Media empirica")

    ax.set_title(
        f"Distribucion Poblacional - {dist_name}",
        loc="left",
        fontsize=12,
        fontweight="bold",
        color="#e8eef7",
    )
    ax.set_xlabel("Valor", color="#d9e5ff")
    ax.set_ylabel("Densidad", color="#d9e5ff")
    ax.tick_params(colors="#c7d5f5")

    shape_text = _describe_shape(population_data)
    ax.text(
        0.98,
        0.92,
        shape_text,
        ha="right",
        va="top",
        transform=ax.transAxes,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#1c2a3f", edgecolor="#324665"),
        color="#e8eef7",
    )
    ax.grid(alpha=0.18, linestyle="--", color="#4b6584")
    ax.legend(frameon=False, loc="upper left", labelcolor="#e8eef7")
    fig.tight_layout(pad=1.2)
    return fig


def plot_sample_means_hist(
    sample_means: np.ndarray, theoretical_mean: float, theoretical_se: float
) -> plt.Figure:
    """Histograma de medias muestrales con curva normal teorica superpuesta."""
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    fig.patch.set_facecolor("#0d1523")
    ax.set_facecolor("#0d1523")

    counts, bins, _ = ax.hist(
        sample_means,
        bins=30,
        color="#6ad59a",
        edgecolor="#e5ffe5",
        alpha=0.85,
        density=True,
        label="Medias muestrales",
    )

    xs = np.linspace(min(sample_means), max(sample_means), 300)
    ys = norm.pdf(xs, loc=theoretical_mean, scale=theoretical_se)
    ax.fill_between(xs, ys, color="#ffb74d", alpha=0.35, label="Normal teorica")
    ax.plot(xs, ys, color="#ff9100", linewidth=2.6)

    emp_mean = np.mean(sample_means)
    ax.axvline(emp_mean, color="#63a4ff", linestyle="--", linewidth=2.2, label="Media empirica")
    ax.axvline(theoretical_mean, color="#ff9100", linestyle=":", linewidth=2.2, label="Media teorica")

    ax.set_title(
        "Distribucion de las medias muestrales",
        loc="left",
        fontsize=12,
        fontweight="bold",
        color="#e8eef7",
    )
    ax.set_xlabel("Media de la muestra", color="#d9e5ff")
    ax.set_ylabel("Densidad", color="#d9e5ff")
    ax.tick_params(colors="#c7d5f5")
    ax.grid(alpha=0.18, linestyle="--", color="#4b6584")
    ax.legend(frameon=False, loc="upper left", labelcolor="#e8eef7")
    fig.tight_layout(pad=1.2)
    return fig
