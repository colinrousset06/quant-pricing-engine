import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.black_scholes import BlackScholesModel
from src.monte_carlo import monte_carlo_option_price
from src.binomial_tree import binomial_tree_price

st.set_page_config(page_title="Quant & Pricing Engine", layout="wide")

# --- PERSONNALISATION CSS : Curseurs en BLEU ---
st.markdown("""
<style>
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #0066cc !important;
        border-color: #0066cc !important;
    }
    div[data-baseweb="slider"] div > div > div > div {
        background-color: #0066cc !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Option Pricing & Risk Engine")
st.markdown("Moteur d'évaluation d'options et d'analyse de sensibilité (Greeks & Volatilité)")

# --- Barre latérale de configuration unique ---
st.sidebar.header("Paramètres du Marché")
S = st.sidebar.number_input("Prix du Sous-Jacent (S)", value=100.0, step=1.0)
K = st.sidebar.slider("Prix d'Exercice / Strike (K)", min_value=50.0, max_value=150.0, value=100.0, step=1.0)
T = st.sidebar.slider("Maturité en années (T)", min_value=0.01, max_value=3.0, value=1.0, step=0.01)
r = st.sidebar.slider("Taux sans risque (r)", min_value=0.0, max_value=0.20, value=0.05, step=0.005)
sigma = st.sidebar.slider("Volatilité (σ)", min_value=0.01, max_value=1.50, value=0.20, step=0.01)

option_type = st.sidebar.selectbox("Type d'Option", ["call", "put"])
option_style = st.sidebar.selectbox("Style d'Option", ["Européenne", "Américaine"])
is_american = (option_style == "Américaine")

# --- Calculs Black-Scholes ---
bs = BlackScholesModel(S, K, T, r, sigma, option_type)
bs_price = bs.price()
greeks = bs.greeks()

# --- Affichage des métriques ---
st.subheader("Indicateurs Clés (Black-Scholes - Européenne)")
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
    
    # Calculs comparatifs avec transmission du paramètre is_american
    mc_price, ci = monte_carlo_option_price(S, K, T, r, sigma, n_simulations=int(n_sims), option_type=option_type)
    bin_price = binomial_tree_price(S, K, T, r, sigma, N=150, option_type=option_type, american=is_american)
    
    st.write(f"• **Black-Scholes (Analytique) :** `{bs_price:.4f} $`")
    st.write(f"• **Monte Carlo :** `{mc_price:.4f} $` *(IC 95% : ±{ci:.4f})*")
    st.write(f"• **Arbre Binomial ({option_style} - 150 pas) :** `{bin_price:.4f} $`")
    
    if is_american:
        st.info("💡 L'arbre binomial intègre le test d'exercice anticipé pour l'option **américaine**.")
    else:
        st.info("💡 L'arbre binomial évalue une option **européenne** standard.")

st.markdown("---")

# --- Surface de Volatilité 3D ---
st.subheader("🌐 Surface de Volatilité Interactive")

strikes = np.linspace(max(10.0, K - 50), K + 50, 20)
maturities = np.linspace(max(0.01, T - 1.5), T + 1.5, 20)
K_grid, T_grid = np.meshgrid(strikes, maturities)

vol_surface = sigma * (1.0 + 0.01 * np.abs(K_grid - K) + 0.1 / (T_grid + 0.1))

fig = go.Figure(data=[
    go.Surface(
        z=vol_surface, 
        x=K_grid, 
        y=T_grid, 
        colorscale='Viridis'
    )
])

fig.update_layout(
    title=f"Surface de Volatilité (Calibrée sur σ = {sigma:.2f}, K = {K}, T = {T})",
    scene=dict(
        xaxis_title="Strike (K)",
        yaxis_title="Maturité (T)",
        zaxis_title="Volatilité Implicite",
        zaxis=dict(range=[0.0, 2.5])
    ),
    width=700,
    height=600
)

st.plotly_chart(fig, use_container_width=True)



'''
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.black_scholes import BlackScholesModel
from src.monte_carlo import monte_carlo_option_price
from src.binomial_tree import binomial_tree_price

st.set_page_config(page_title="Quant & Pricing Engine", layout="wide")

# --- PERSONNALISATION CSS : Curseurs en BLEU ---
st.markdown("""
<style>
    /* Change la couleur de la poignée du slider en bleu */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #0066cc !important;
        border-color: #0066cc !important;
    }
    /* Change la couleur de la barre active du slider */
    div[data-baseweb="slider"] div > div > div > div {
        background-color: #0066cc !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Option Pricing & Risk Engine")
st.markdown("Moteur d'évaluation d'options et d'analyse de sensibilité (Greeks & Volatilité)")

# --- Barre latérale de configuration unique ---
st.sidebar.header("Paramètres du Marché")
S = st.sidebar.number_input("Prix du Sous-Jacent (S)", value=100.0, step=1.0)

# Remplacement du number_input par un slider pour le Strike (K) en bleu
K = st.sidebar.slider("Prix d'Exercice / Strike (K)", min_value=50.0, max_value=150.0, value=100.0, step=1.0)

# Curseur pour la Maturité (T)
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

st.markdown("---")
# --- Surface de Volatilité 3D (Dynamique et connectée aux curseurs) ---
st.subheader("🌐 Surface de Volatilité Interactive")

st.info(f"🔍 **Diagnostic en direct :** $\sigma$ = **{sigma:.4f}** | $K$ = **{K:.1f}** | $T$ = **{T:.2f}**")

# Définition de la grille 3D autour des valeurs actuelles pour plus de dynamisme
strikes = np.linspace(max(10.0, K - 50), K + 50, 20)
maturities = np.linspace(max(0.01, T - 1.5), T + 1.5, 20)
K_grid, T_grid = np.meshgrid(strikes, maturities)

# Formule rendant les curseurs K et T pleinement actifs et visibles sur le graphe
# Le niveau global s'ajuste avec T et le centre du smile s'ajuste avec K
vol_surface = sigma * (1.0 + 0.01 * np.abs(K_grid - K) + 0.1 / (T_grid + 0.1))

# Création du graphique Plotly 3D
fig = go.Figure(data=[
    go.Surface(
        z=vol_surface, 
        x=K_grid, 
        y=T_grid, 
        colorscale='Viridis'
    )
])

fig.update_layout(
    title=f"Surface de Volatilité (Calibrée sur σ = {sigma:.2f}, K = {K}, T = {T})",
    scene=dict(
        xaxis_title="Strike (K)",
        yaxis_title="Maturité (T)",
        zaxis_title="Volatilité Implicite",
        zaxis=dict(range=[0.0, 2.5])
    ),
    width=700,
    height=600
)

st.plotly_chart(fig, use_container_width=True)'''