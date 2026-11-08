import time
import numpy as np
from numba import jit
from black_scholes import black_scholes_call

# 1. Version Python pur (boucle)
def monte_carlo_pure_python(S, K, T, r, sigma, n_simulations):
    import random
    payoffs = 0.0
    # Simulation naïve avec des boucles lentes
    for _ in range(n_simulations):
        z = random.gauss(0.0, 1.0)
        ST = S * math.exp((r - 0.5 * sigma**2) * T + sigma * math.sqrt(T) * z)
        payoff = max(ST - K, 0.0)
        payoffs += math.exp(-r * T) * payoff
    return payoffs / n_simulations

# 2. Version NumPy vectorisée
def monte_carlo_numpy(S, K, T, r, sigma, n_simulations):
    z = np.random.standard_normal(n_simulations)
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)
    payoffs = np.maximum(ST - K, 0.0)
    return np.exp(-r * T) * np.mean(payoffs)

# 3. Version Numba (JIT compilation)
@jit(nopython=True)
def monte_carlo_numba_loop(S, K, T, r, sigma, n_simulations):
    sum_payoff = 0.0
    for i in range(n_simulations):
        # Générateur pseudo-aléatoire simple pour l'exemple JIT
        z = np.random.randn() # ou équivalent
        ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)
        sum_payoff += max(ST - K, 0.0)
    return np.exp(-r * T) * (sum_payoff / n_simulations)

if __name__ == "__main__":
    import math
    n = 100_000
    print(f"--- Benchmark sur {n} simulations ---")
    
    # Test NumPy
    start = time.time()
    res_np = monte_carlo_numpy(100, 100, 1, 0.05, 0.2, n)
    t_np = time.time() - start
    print(f"NumPy vectorisé : {t_np:.4f} secondes (Résultat: {res_np:.2f})")