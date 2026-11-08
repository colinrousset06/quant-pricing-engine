import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.black_scholes import BlackScholesModel
from src.monte_carlo import monte_carlo_option_price
from src.binomial_tree import binomial_tree_price

st.set_page_config(page_title="Quant & Pricing Engine", layout="wide")

st.title("📊 Option Pricing & Risk Engine")
st.markdown("Moteur d'évaluation d'options et d'analyse de sensibilité (Greeks & Volatilité)")

# --- Barre latérale de configuration ---
st.sidebar.header("Paramètres du Marché")
S = st.sidebar.number_input("Prix du Sous-Jacent (S)", value=100.0, step=1.0)
K = st.sidebar.number_input("Prix d'Exercice / Strike (K)", value=100.0, step=1.0)
T = st.sidebar.slider("Maturité en années (T)", min_value=0.01, max_value=3.0, value=1.0, step=0.01)
r = st.sidebar.slider("Taux sans risque (r)", min_value=0.0, max_value=0.20, value=0.05, step=0.005)
sigma = st.sidebar.slider("Volatilité (σ)", min_value=0.01, max_value=1.50, value=0.20, step=0.01)
option_type = st.sidebar.selectbox("Type d'Option", ["call", "put"])

# --- Calculs Black-Scholes ---
bs = BlackScholesModel(S, K, T, r, sigma, option_type)
bs_price = bs.price()
greeks = bs.greeks()

# --- Affichage des métriques ---
st.subheader("Indicateurs Clés (Black-Scholes)")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Prix de l'Option", f"${bs_price:.4f}")
col2.metric("Delta", f"{greeks['Delta']:.4f}")
col3.metric("Gamma", f"{greeks['Gamma']:.4f}")
col4.metric("Vega", f"{greeks['Vega']:.4f}")
col5.metric("Theta (Journalier)", f"{greeks['Theta (Daily)']:.4f}")

st.markdown("---")

# --- Graphique interactif et comparaisons ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Impact de la Volatilité sur le Prix")
    sigmas = np.linspace(0.05, 1.0, 50)
    prices_vol = [BlackScholesModel(S, K, T, r, s, option_type).price() for s in sigmas]
    
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(x=sigmas, y=prices_vol, mode='lines', name='Prix BS', line=dict(color='royalblue', width=3)))
    fig_vol.add_vline(x=sigma, line_dash="dash", line_color="green", annotation_text="Vol actuelle")
    fig_vol.update_layout(xaxis_title="Volatilité (σ)", yaxis_title="Prix de l'Option ($)", template="plotly_white")
    st.plotly_chart(fig_vol, use_container_width=True)

with col_right:
    st.subheader("Comparaison des Modèles de Pricing")
    n_sims = st.number_input("Nombre de simulations Monte Carlo", value=50_000, step=10_000)
    
    # Calculs comparatifs
    mc_price, ci = monte_carlo_option_price(S, K, T, r, sigma, n_simulations=int(n_sims), option_type=option_type)
    bin_price = binomial_tree_price(S, K, T, r, sigma, N=150, option_type=option_type)
    
    st.write(f"• **Black-Scholes (Analytique) :** `{bs_price:.4f} $`")
    st.write(f"• **Monte Carlo :** `{mc_price:.4f} $` *(IC 95% : ±{ci:.4f})*")
    st.write(f"• **Arbre Binomial (CRR 150 pas) :** `{bin_price:.4f} $`")
    
    st.info("💡 L'arbre binomial permet également de priser des options de style américain en activant le test d'exercice anticipé.")




'''Création de la volatility_surface'''
import numpy as np
def generate_volatility_surface(strikes, maturities):
    """Génère une matrice de volatilité implicite (Smile / Skew)."""
    surface = np.zeros((len(maturities), len(strikes)))
    for i, T in enumerate(maturities):
        for j, K in enumerate(strikes):
            # Formule empirique simple simulant un smile de volatilité en fonction du strike
            base_vol = 0.20
            skew = 0.005 * (100 - K) ** 2 / 100
            smile = base_vol + skew + 0.02 * (1 / T if T > 0 else 1)
            surface[i, j] = max(0.05, smile)
    return surface





'''Création du projet du graphique en 3D'''    
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.subheader("🌐 Surface de Volatilité Animée (Bouton Play)")

# 1. Définition des axes (Strikes et Maturités)
strikes = np.linspace(80, 120, 15)
maturities = np.linspace(0.1, 2.0, 15)
K_grid, T_grid = np.meshgrid(strikes, maturities)

# 2. Création des frames d'animation (ex: évolution selon le temps ou un paramètre)
frames = []
for t_val in np.linspace(0.1, 1.0, 10):
    # Simulation d'une variation de la surface selon t_val
    z_vals = 0.20 + 0.0005 * (100 - K_grid)**2 + (0.05 / T_grid) * t_val
    frames.append(
        go.Frame(
            data=[go.Surface(z=z_vals, x=K_grid, y=T_grid, colorscale='Viridis')],
            name=f"frame_{t_val:.2f}"
        )
    )

# 3. Graphique initial (première frame)
fig = go.Figure(
    data=[
        go.Surface(
            z=0.20 + 0.0005 * (100 - K_grid)**2 + (0.05 / T_grid) * 0.1,
            x=K_grid,
            y=T_grid,
            colorscale='Viridis'
        )
    ],
    frames=frames
)

# 4. Ajout des boutons de contrôle (Play / Pause) et mise en page 3D
fig.update_layout(
    title="Évolution dynamique de la Surface de Volatilité",
    updatemenus=[{
        "type": "buttons",
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 400, "redraw": True}, "fromcurrent": True}],
                "label": "▶ Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}],
                "label": "❚❚ Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 10},
        "showactive": False,
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }],
    scene=dict(
        xaxis_title="Strike (K)",
        yaxis_title="Maturité (T)",
        zaxis_title="Volatilité Implicite",
    ),
    width=700,
    height=600
)

# 5. Affichage dans l'application Streamlit
st.plotly_chart(fig, use_container_width=True)