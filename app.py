import streamlit as st
import numpy as np
import scipy.stats as stats
import math
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(
    page_title="SuperCalculadora & Analytics",
    page_icon="📱",
    layout="wide"
)

# 2. CSS con Paleta Clara y Luminosa (Modo Claro Moderno)
st.markdown("""
<style>
/* Fondo general claro e iluminado */
.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    color: #0f172a;
}

/* Tarjetas e íconos con fondos blancos limpios y bordes suaves */
div[data-testid="stVerticalBlock"] > div {
    background-color: #ffffff;
    border-radius: 12px;
    border: 1px solid #cbd5e1;
    padding: 16px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
}

/* Botones principales estilo azul profesional */
.stButton>button {
    border-radius: 8px;
    font-weight: 600;
    background-color: #ffffff;
    color: #1e293b;
    border: 1px solid #cbd5e1;
    transition: all 0.2s ease-in-out;
}

.stButton>button:hover {
    background-color: #0284c7;
    color: #ffffff;
    border-color: #0284c7;
    box-shadow: 0px 2px 8px rgba(2, 132, 199, 0.3);
}

/* Cajas de texto de entrada de números y datos */
input {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    border: 1px solid #94a3b8 !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}

/* Métricas numéricas destacadas en azul */
div[data-testid="stMetricValue"] {
    color: #0284c7 !important;
}

/* Barra lateral en tono gris claro elegante */
section[data-testid="stSidebar"] {
    background-color: #f1f5f9;
    border-right: 1px solid #cbd5e1;
}
</style>
""", unsafe_allow_html=True)

# 3. Estado de la sesión para la calculadora
if "calc_display" not in st.session_state:
    st.session_state.calc_display = ""
if "historial" not in st.session_state:
    st.session_state.historial = []

def agregar_caracter(val):
    st.session_state.calc_display += val

def limpiar_pantalla():
    st.session_state.calc_display = ""

def borrar_ultimo():
    st.session_state.calc_display = st.session_state.calc_display[:-1]

def calcular_resultado():
    expr_input = st.session_state.calc_display
    if not expr_input:
        return
    try:
        expr = expr_input.replace('asin', 'np.arcsin').replace('acos', 'np.arccos').replace('atan', 'np.arctan')
        expr = expr.replace('sin', 'np.sin').replace('cos', 'np.cos').replace('tan', 'np.tan')
        expr = expr.replace('ln', 'np.log').replace('log10', 'np.log10')
        expr = expr.replace('√', 'np.sqrt').replace('^', '**').replace('π', 'np.pi').replace('e', 'np.e')
        expr = expr.replace('x²', '**2').replace('%', '/100')
        
        if '!' in expr:
            import re
            expr = re.sub(r'(\d+)!', r'math.factorial(\1)', expr)

        res = eval(expr)
        res_str = f"{res:.8g}"
        st.session_state.historial.append(f"{expr_input} = {res_str}")
        st.session_state.calc_display = res_str
    except Exception:
        st.error("Expresión no válida")

# --- BARRA LATERAL: SELECTOR DINÁMICO DE MODELO ---
st.sidebar.title("🎛️ Panel de Control")
modelo_seleccionado = st.sidebar.radio(
    "Selecciona el Modelo de Calculadora:",
    [
        "📱 Modelo 1: Calculadora Científica",
        "📊 Modelo 2: Estadística Inferencial Profesional",
        "⚙️ Modelo 3: Simulación Monte Carlo"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Ciencia + Datos + Simulación = Grandes Decisiones")

# --- ENCABEZADO ---
st.title("SuperCalculadora & Analytics")

# ==========================================
# MODELO 1: CALCULADORA CIENTÍFICA
# ==========================================
if "Modelo 1" in modelo_seleccionado:
    st.subheader("📱 Calculadora Científica Avanzada")
    st.caption("Más que números, soluciones. Funciones avanzadas y notación científica.")

    col_calc, col_hist = st.columns([2, 1])

    with col_calc:
        st.text_input("Pantalla / Expresión:", key="calc_display")

        c_shift, c_alpha, c_mode, c_ac = st.columns(4)
        c_shift.button("Shift", use_container_width=True)
        c_alpha.button("Alpha", use_container_width=True)
        c_mode.button("MODE", use_container_width=True)
        c_ac.button("AC", on_click=limpiar_pantalla, use_container_width=True)

        botones = [
            [('x²', lambda: agregar_caracter('^2')), ('xⁿ', lambda: agregar_caracter('^')), ('√', lambda: agregar_caracter('√(')), ('log', lambda: agregar_caracter('log10(')), ('ln', lambda: agregar_caracter('ln('))],
            [('sin', lambda: agregar_caracter('sin(')), ('cos', lambda: agregar_caracter('cos(')), ('tan', lambda: agregar_caracter('tan(')), ('(', lambda: agregar_caracter('(')), (')', lambda: agregar_caracter(')'))],
            [('7', lambda: agregar_caracter('7')), ('8', lambda: agregar_caracter('8')), ('9', lambda: agregar_caracter('9')), ('DEL', borrar_ultimo), ('/', lambda: agregar_caracter('/'))],
            [('4', lambda: agregar_caracter('4')), ('5', lambda: agregar_caracter('5')), ('6', lambda: agregar_caracter('6')), ('*', lambda: agregar_caracter('*')), ('!', lambda: agregar_caracter('!'))],
            [('1', lambda: agregar_caracter('1')), ('2', lambda: agregar_caracter('2')), ('3', lambda: agregar_caracter('3')), ('-', lambda: agregar_caracter('-')), ('π', lambda: agregar_caracter('π'))],
            [('0', lambda: agregar_caracter('0')), ('.', lambda: agregar_caracter('.')), ('%', lambda: agregar_caracter('%')), ('+', lambda: agregar_caracter('+')), ('=', calcular_resultado)]
        ]

        for r_idx, row in enumerate(botones):
            cols = st.columns(5)
            for c_idx, (label, func) in enumerate(row):
                cols[c_idx].button(label, key=f"btn_{r_idx}_{c_idx}", on_click=func, use_container_width=True)

    with col_hist:
        st.subheader("📜 Historial Memoria")
        if st.session_state.historial:
            for item in reversed(st.session_state.historial[-8:]):
                st.code(item, language="text")
            if st.button("Limpiar Registro", use_container_width=True):
                st.session_state.historial = []
                st.rerun()
        else:
            st.info("Sin operaciones en memoria.")

# ==========================================
# MODELO 2: ESTADÍSTICA INFERENCIAL
# ==========================================
elif "Modelo 2" in modelo_seleccionado:
    st.subheader("📊 Estadística Inferencial Profesional")
    st.caption("Analiza. Decide. Con evidencia. Pruebas de hipótesis e intervalos de confianza.")

    col_in, col_plot = st.columns([1, 1.2])

    with col_in:
        tipo_prueba = st.selectbox("Análisis:", [
            "Descriptiva & Intervalo Z/t",
            "Prueba t de 1 Muestra",
            "Regresión Lineal Simple"
        ])

        raw_m1 = st.text_input("Muestra 1 / Var X (separados por coma):", "12, 15, 14, 10, 13, 16, 18, 11, 14")
        need_m2 = tipo_prueba == "Regresión Lineal Simple"
        raw_m2 = st.text_input("Muestra 2 / Var Y (separados por coma):", "8, 9, 11, 10, 7, 12, 10, 9, 11", disabled=not need_m2)

        conf = st.number_input("Nivel de Confianza:", value=0.95, min_value=0.50, max_value=0.99, step=0.01)
        mu0 = st.number_input("Media Hipotética (μ₀):", value=12.0)

        calc_btn = st.button("⚡ Calcular y Graficar", type="primary", use_container_width=True)

    with col_plot:
        try:
            data1 = np.array([float(x.strip()) for x in raw_m1.split(",") if x.strip() != ""])
            data2 = np.array([float(x.strip()) for x in raw_m2.split(",") if x.strip() != ""]) if need_m2 else None
        except ValueError:
            st.error("Ingresa solo números válidos separados por comas.")
            st.stop()

        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#f8fafc')

        if tipo_prueba == "Descriptiva & Intervalo Z/t":
            n, media, std = len(data1), np.mean(data1), np.std(data1, ddof=1)
            se = std / np.sqrt(n)
            ic_t = stats.t.interval(conf, df=n-1, loc=media, scale=se)

            st.success(f"**Media (x̄):** {media:.4f} | **s:** {std:.4f} | **SE:** {se:.4f}")
            st.info(f"**IC ({conf*100:.0f}%):** [{ic_t[0]:.4f}, {ic_t[1]:.4f}]")

            ax.boxplot(data1, patch_artist=True, boxprops=dict(facecolor="#38bdf8", color="#0284c7"))
            ax.errorbar(1, media, yerr=[[media - ic_t[0]], [ic_t[1] - media]], fmt='ro', capsize=6, label='Media e IC')
            ax.set_title("Diagrama de Caja e Intervalo de Confianza", color="#0f172a")
            ax.legend()

        elif tipo_prueba == "Prueba t de 1 Muestra":
            t_stat, p_val = stats.ttest_1samp(data1, mu0)
            st.metric("Estadístico t", f"{t_stat:.4f}")
            st.metric("p-valor", f"{p_val:.6f}")

            ax.hist(data1, bins=6, color="#0284c7", alpha=0.7, edgecolor="#0369a1")
            ax.axvline(np.mean(data1), color="#16a34a", linestyle="-", linewidth=2, label='Media Muestral')
            ax.axvline(mu0, color="#dc2626", linestyle="--", linewidth=2, label='μ₀ Hipotético')
            ax.set_title("Histograma vs Valor Hipotético", color="#0f172a")
            ax.legend()

        elif tipo_prueba == "Regresión Lineal Simple":
            slope, intercept, r_val, p_val, _ = stats.linregress(data1, data2)
            st.write(f"**Modelo:** $Y = {intercept:.2f} + {slope:.2f}X$ | **R²:** {r_val**2:.4f}")

            ax.scatter(data1, data2, color="#0284c7", label="Datos")
            ax.plot(data1, intercept + slope * data1, color="#dc2626", label="Regresión")
            ax.set_title("Ajuste Lineal", color="#0f172a")
            ax.legend()

        ax.tick_params(colors='#0f172a')
        ax.grid(True, linestyle=":", alpha=0.6)
        st.pyplot(fig)

# ==========================================
# MODELO 3: SIMULACIÓN MONTE CARLO
# ==========================================
else:
    st.subheader("⚙️ Simulación de Monte Carlo & Modelado")
    st.caption("Modela. Experimenta. Anticipa escenarios reales e hipotéticos.")

    col_sim_ctrl, col_sim_plot = st.columns([1, 1.2])

    with col_sim_ctrl:
        sim_tipo = st.selectbox("Distribución:", ["Normal", "Poisson", "Caminata Aleatoria"])
        n_sim = st.select_slider("Iteraciones (N):", options=[1000, 5000, 10000, 50000], value=10000)
        p1 = st.number_input("Parámetro 1 (Media / λ):", value=100.0)
        p2 = st.number_input("Parámetro 2 (Desv. Estándar σ):", value=15.0)

    with col_sim_plot:
        fig_sim, ax_sim = plt.subplots(figsize=(6, 4))
        fig_sim.patch.set_facecolor('#ffffff')
        ax_sim.set_facecolor('#f8fafc')

        if sim_tipo == "Normal":
            datos = np.random.normal(loc=p1, scale=p2, size=n_sim)
            ax_sim.hist(datos, bins=35, density=True, color="#16a34a", alpha=0.7, edgecolor="#15803d")
            ax_sim.set_title(f"Distribución Normal (N={n_sim})", color="#0f172a")
        elif sim_tipo == "Poisson":
            datos = np.random.poisson(lam=p1, size=n_sim)
            vals, counts = np.unique(datos, return_counts=True)
            ax_sim.bar(vals, counts/n_sim, color="#16a34a", alpha=0.8)
            ax_sim.set_title(f"Distribución Poisson (λ={p1})", color="#0f172a")
        else:
            pasos = np.random.choice([-1, 1], size=(n_sim, 100))
            trayectorias = np.cumsum(pasos, axis=1) + p1
            for i in range(min(n_sim, 40)):
                ax_sim.plot(trayectorias[i], alpha=0.3, linewidth=1)
            datos = trayectorias[:, -1]
            ax_sim.set_title(f"Trayectorias Estocásticas ({n_sim})", color="#0f172a")

        ax_sim.tick_params(colors='#0f172a')
        ax_sim.grid(True, linestyle=":", alpha=0.6)
        st.pyplot(fig_sim)

        st.metric("Media Simulada", f"{np.mean(datos):.2f}")
        st.metric("Desviación Estándar", f"{np.std(datos):.2f}")