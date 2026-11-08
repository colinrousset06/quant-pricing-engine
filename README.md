# 📈 Quantitative Option Pricing & Risk Engine

Ce projet implémente un moteur de tarification d'options financières et d'analyse de risques (Greeks) en utilisant trois approches clés : **Black-Scholes**, **Simulations de Monte Carlo**, et les **Arbres Binomiaux (Cox-Ross-Rubinstein)**.

## 🚀 Fonctionnalités
- **Modèle Analytique de Black-Scholes** avec calcul analytique précis des Greeks ($\Delta, \Gamma, \mathcal{V}, \Theta, \rho$).
- **Moteur Monte Carlo** vectorisé sous NumPy avec calcul d'intervalle de confiance à 95%.
- **Arbre Binomial CRR** adapté aux options européennes et américaines.
- **Interface Web Interactive** propulsée par Streamlit et visualisée avec Plotly pour analyser l'impact de la volatilité en temps réel.

## 🛠️ Stack Technique
- **Langage :** Python 3.10+
- **Calcul Numérique :** NumPy, SciPy
- **Interface & Visualisation :** Streamlit, Plotly

## 📌 Installation & Utilisation locale

1. Cloner le dépôt :
   ```bash
   git clone [https://github.com/colinrousset06/quant-pricing-engine.git](https://github.com/colinrousset06/quant-pricing-engine.git)
   cd quant-pricing-engine
