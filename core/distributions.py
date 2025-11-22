import numpy as np
from typing import Tuple

# Generadores de datos poblacionales


def generate_uniform(a: float, b: float, size: int) -> np.ndarray:
    """Genera datos de una distribucion Uniforme(a, b)."""
    return np.random.uniform(a, b, size)


def generate_exponential(lam: float, size: int) -> np.ndarray:
    """Genera datos de una distribucion Exponencial con tasa lam."""
    return np.random.exponential(1 / lam, size)


def generate_binomial(n_trials: int, p: float, size: int) -> np.ndarray:
    """Genera datos de una distribucion Binomial(n_trials, p)."""
    return np.random.binomial(n_trials, p, size)


# Parametros teoricos


def theoretical_params_uniform(a: float, b: float) -> Tuple[float, float]:
    """Retorna media y desviacion estandar teoricas para Uniforme(a, b)."""
    mean = (a + b) / 2
    std = (b - a) / np.sqrt(12)
    return mean, std


def theoretical_params_exponential(lam: float) -> Tuple[float, float]:
    """Retorna media y desviacion estandar teoricas para Exponencial(lam)."""
    mean = 1 / lam
    std = 1 / lam
    return mean, std


def theoretical_params_binomial(n_trials: int, p: float) -> Tuple[float, float]:
    """Retorna media y desviacion estandar teoricas para Binomial(n_trials, p)."""
    mean = n_trials * p
    std = np.sqrt(n_trials * p * (1 - p))
    return mean, std
