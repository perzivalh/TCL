from typing import Dict, Tuple

import numpy as np

from core.distributions import (
    theoretical_params_binomial,
    theoretical_params_exponential,
    theoretical_params_uniform,
)


def compute_empirical_stats(data: np.ndarray) -> Dict[str, float]:
    """Calcula media y desviacion estandar empiricas."""
    mean = float(np.mean(data))
    std = float(np.std(data, ddof=0))
    return {"mean": mean, "std": std, "size": len(data)}


def _theoretical_population_params(dist_name: str, dist_params: Dict[str, float]) -> Tuple[float, float]:
    if dist_name == "Uniforme":
        return theoretical_params_uniform(dist_params["a"], dist_params["b"])
    if dist_name == "Exponencial":
        return theoretical_params_exponential(dist_params["lam"])
    if dist_name == "Binomial":
        return theoretical_params_binomial(dist_params["n_trials"], dist_params["p"])
    raise ValueError(f"Distribucion no soportada: {dist_name}")


def compute_theoretical_stats(
    dist_name: str, dist_params: Dict[str, float], sample_size: int
) -> Dict[str, float]:
    """Calcula parametros teoricos de la poblacion y el error estandar de la media."""
    pop_mean, pop_std = _theoretical_population_params(dist_name, dist_params)
    se_mean = pop_std / np.sqrt(sample_size)
    return {"mean": pop_mean, "std": pop_std, "se": se_mean}


def compute_differences(theoretical: Dict[str, float], empirical: Dict[str, float]) -> Dict[str, float]:
    """Diferencias absolutas entre valores teoricos y empiricos."""
    diff = {}
    for key in theoretical:
        if key in empirical:
            diff[key] = abs(float(theoretical[key]) - float(empirical[key]))
    return diff
