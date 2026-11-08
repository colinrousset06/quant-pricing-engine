import pytest
import numpy as np
from src.black_scholes import black_scholes_call
from src.monte_carlo import monte_carlo_pricing
from src.binomial_tree import binomial_tree_pricing

def test_convergence_monte_carlo():
    S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.2
    bs_price = black_scholes_call(S, K, T, r, sigma)
    
    # Avec un grand nombre de simulations, l'écart doit être très faible
    mc_price = monte_carlo_pricing(S, K, T, r, sigma, n_simulations=500_000)
    
    # Tolérance de 1%
    assert abs(mc_price - bs_price) / bs_price < 0.01

def test_convergence_binomial_tree():
    S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.2
    bs_price = black_scholes_call(S, K, T, r, sigma)
    
    # Avec un nombre d'étapes élevé (N=500), l'arbre binomial converge vers Black-Scholes
    tree_price = binomial_tree_pricing(S, K, T, r, sigma, N=500, option_type="call")
    
    # Tolérance de 0.5%
    assert abs(tree_price - bs_price) / bs_price < 0.005