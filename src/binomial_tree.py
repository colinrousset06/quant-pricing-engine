import numpy as np

def binomial_tree_price(S: float, K: float, T: float, r: float, sigma: float, N: int = 100, 
                        option_type: str = "call", american: bool = False) -> float:
    """
    Tarification par Arbre Binomial CRR.
    """
    if T <= 0:
        payoff = max(0.0, S - K) if option_type.lower() == "call" else max(0.0, K - S)
        return float(payoff)

    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    q = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)
    
    # Prix du sous-jacent à l'échéance
    ST = S * (u ** np.arange(N, -1, -1)) * (d ** np.arange(0, N + 1))
    
    if option_type.lower() == "call":
        values = np.maximum(ST - K, 0)
    else:
        values = np.maximum(K - ST, 0)
        
    # Remontée de l'arbre (Induction arrière)
    for i in range(N - 1, -1, -1):
        values = discount * (q * values[:-1] + (1 - q) * values[1:])
        if american:
            S_node = S * (u ** np.arange(i, -1, -1)) * (d ** np.arange(0, i + 1))
            intrinsic = np.maximum(S_node - K, 0) if option_type.lower() == "call" else np.maximum(K - S_node, 0)
            values = np.maximum(values, intrinsic)
            
    return float(values[0])