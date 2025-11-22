from typing import Callable, Dict

import numpy as np

from core.distributions import (
    generate_binomial,
    generate_exponential,
    generate_uniform,
)


def _get_generator(dist_name: str) -> Callable:
    """Devuelve la funcion generadora segun el nombre de la distribucion."""
    generators = {
        "Uniforme": generate_uniform,
        "Exponencial": generate_exponential,
        "Binomial": generate_binomial,
    }
    if dist_name not in generators:
        raise ValueError(f"Distribucion no soportada: {dist_name}")
    return generators[dist_name]


def generate_population(dist_name: str, dist_params: Dict[str, float], size: int) -> np.ndarray:
    """Genera una poblacion grande para visualizacion."""
    generator = _get_generator(dist_name)
    return generator(**dist_params, size=size)


def simulate_sample_means(
    dist_name: str,
    dist_params: Dict[str, float],
    sample_size: int,
    n_simulations: int,
) -> np.ndarray:
    """
    Genera n_simulations muestras de tamano sample_size, calcula sus medias
    y devuelve un arreglo con las medias muestrales.
    """
    if sample_size <= 0 or n_simulations <= 0:
        raise ValueError("sample_size y n_simulations deben ser positivos.")

    generator = _get_generator(dist_name)
    # Usamos RNG vectorizado para eficiencia.
    samples = generator(**dist_params, size=(n_simulations, sample_size))
    sample_means = samples.mean(axis=1)
    return sample_means
