"""
Funciones basicas para generar datos y simular el comportamiento del Teorema Central del Limite (TCL).
La idea: crear poblaciones con distintas formas y repetir muchas muestras independientes para mostrar
que las medias muestrales se aproximan a una distribucion normal al aumentar el numero de simulaciones.
"""
from typing import Callable, Dict

import numpy as np

from core.distributions import (
    generate_binomial,
    generate_exponential,
    generate_uniform,
)


def _get_generator(dist_name: str) -> Callable:
    """
    Devuelve la funcion generadora segun el nombre de la distribucion.
    Elegir el generador aqui desacopla la interfaz (string elegida en UI) de la implementacion real.
    """
    generators = {
        "Uniforme": generate_uniform,
        "Exponencial": generate_exponential,
        "Binomial": generate_binomial,
    }
    if dist_name not in generators:
        raise ValueError(f"Distribucion no soportada: {dist_name}")
    return generators[dist_name]


def generate_population(dist_name: str, dist_params: Dict[str, float], size: int) -> np.ndarray:
    """
    Genera una poblacion grande para visualizacion.
    Sirve para mostrar la forma original (asimetrica o no) antes de aplicar el TCL con medias muestrales.
    """
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
    Este es el paso clave donde se evidencia el TCL: sin importar la forma original,
    la distribucion de estas medias tiende a ser normal si k (n_simulations) es grande.
    """
    if sample_size <= 0 or n_simulations <= 0:
        raise ValueError("sample_size y n_simulations deben ser positivos.")

    generator = _get_generator(dist_name)
    # Usamos RNG vectorizado para eficiencia y reproducibilidad con la API de numpy (mas rapido que bucles).
    samples = generator(**dist_params, size=(n_simulations, sample_size))
    sample_means = samples.mean(axis=1)
    return sample_means
