import numpy as np

def monte_carlo_option_price(S: float, K: float, T: float, r: float, sigma: float, 
                             n_simulations: int = 100_000, option_type: str = "call") -> tuple[float, float]:
    """
    Simulation Monte Carlo (Mouvement Brownien Géométrique) avec intervalle de confiance à 95%.
    """
    if T <= 0:
        payoff = max(0.0, S - K) if option_type.lower() == "call" else max(0.0, K - S)
        return float(payoff), 0.0

    Z = np.random.standard_normal(n_simulations)
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    
    if option_type.lower() == "call":
        payoffs = np.maximum(ST - K, 0)
    else:
        payoffs = np.maximum(K - ST, 0)
        
    discounted_payoffs = np.exp(-r * T) * payoffs
    price = np.mean(discounted_payoffs)
    std_error = np.std(discounted_payoffs) / np.sqrt(n_simulations)
    
    return float(price), float(1.96 * std_error)