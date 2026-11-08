import numpy as np
from scipy.stats import norm

class BlackScholesModel:
    def __init__(self, S: float, K: float, T: float, r: float, sigma: float, option_type: str = "call"):
        self.S = float(S)
        self.K = float(K)
        self.T = float(T)
        self.r = float(r)
        self.sigma = float(sigma)
        self.option_type = option_type.lower()
        
    def _d1_d2(self):
        # Éviter une division par zéro si T ou sigma est trop proche de 0
        T = max(self.T, 1e-8)
        sigma = max(self.sigma, 1e-8)
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return d1, d2

    def price(self) -> float:
        if self.T <= 0:
            if self.option_type == "call":
                return max(0.0, self.S - self.K)
            else:
                return max(0.0, self.K - self.S)
                
        d1, d2 = self._d1_d2()
        if self.option_type == "call":
            return float(self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2))
        else:
            return float(self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1))

    def greeks(self) -> dict:
        if self.T <= 0:
            return {"Delta": 0.0, "Gamma": 0.0, "Vega": 0.0, "Theta (Daily)": 0.0, "Rho": 0.0}
            
        d1, d2 = self._d1_d2()
        pdf_d1 = norm.pdf(d1)
        
        # Delta
        delta = norm.cdf(d1) if self.option_type == "call" else norm.cdf(d1) - 1.0
        
        # Gamma
        gamma = pdf_d1 / (self.S * self.sigma * np.sqrt(self.T))
        
        # Vega (exprimé pour une variation de 1% de volatilité)
        vega = (self.S * pdf_d1 * np.sqrt(self.T)) / 100.0
        
        # Theta annualisé converti en journalier (/ 365)
        if self.option_type == "call":
            theta = (- (self.S * pdf_d1 * self.sigma) / (2 * np.sqrt(self.T)) 
                     - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2))
        else:
            theta = (- (self.S * pdf_d1 * self.sigma) / (2 * np.sqrt(self.T)) 
                     + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2))
        theta_daily = theta / 365.0
        
        # Rho (exprimé pour une variation de 1% du taux)
        if self.option_type == "call":
            rho = (self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(d2)) / 100.0
        else:
            rho = (- self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-d2)) / 100.0

        return {
            "Delta": float(delta),
            "Gamma": float(gamma),
            "Vega": float(vega),
            "Theta (Daily)": float(theta_daily),
            "Rho": float(rho)
        }