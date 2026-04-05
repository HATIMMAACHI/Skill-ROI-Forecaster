import streamlit as st
import joblib
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from streamlit_lottie import st_lottie
import requests

# ── CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title='Skill ROI Forecaster',
    page_icon='🎯',
    layout='wide',
    initial_sidebar_state="expanded"
)

# ── CHARGEMENT DES ASSETS (Lottie)
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")

# ── STYLE CSS AVANCÉ (Glassmorphism & Custom Fonts)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Poppins:wght@800&display=swap');

    /* Global */
    .main { background-color: #0E1117; font-family: 'Inter', sans-serif; }
    
    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: rgba(26, 28, 35, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(232, 78, 27, 0.2);
    }

    /* Headings */
    h1 { font-family: 'Poppins', sans-serif; letter-spacing: -1px; background: -webkit-linear-gradient(#ff8c00, #e84e1b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    h2 { color: #ffffff !important; font-weight: 700; border-left: 5px solid #e84e1b; padding-left: 15px; margin-top: 2rem; }

    /* Custom Cards for Metrics */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #e84e1b;
        background: rgba(232, 78, 27, 0.05);
    }
    .metric-value { color: #e84e1b; font-size: 2rem; font-weight: bold; }
    .metric-label { color: #888; font-size: 0.9rem; text-transform: uppercase; }

    /* Buttons & Inputs */
    .stMultiSelect div[role="listbox"] { background-color: #1A1C23; }
    .stSlider > div > div > div > div { background-color: #e84e1b; }
</style>
""", unsafe_allow_html=True)

# ── LOGIQUE DE DONNÉES (Cache)
@st.cache_resource
def load_models():
    # Simulation des chargements (Remplace par tes vrais fichiers)
    model_rf = joblib.load('random_forest_model.pkl')
    rules = joblib.load('apriori_rules.pkl')
    roi_df = joblib.load('roi_df.pkl')
    feature_columns = joblib.load('feature_columns.pkl')
    return model_rf, rules, roi_df, feature_columns

model_rf, rules, roi_df, feature_columns = load_models()
skills_cols = roi_df['skill'].tolist()

# ── SIDEBAR PRO
with st.sidebar:
    st_lottie(lottie_coding, height=150, key="coding")
    st.markdown("## 👤 Ton Profil")
    
    mes_skills = st.multiselect(
        '🛠️ Skills actuels',
        options=skills_cols,
        default=['python', 'sql']
    )

    niveau = st.select_slider(
        '📈 Niveau d\'expérience',
        options=['Junior', 'Mid Level', 'Senior', 'Lead']
    )

    top_n = st.slider('📊 Recommandations', 3, 10, 5)
    
    st.markdown("---")
    st.info("💡 Astuce : Ajoute SQL et Cloud pour voir le ROI s'envoler !")

# ── HEADER SECTION
header_col1, header_col2 = st.columns([2, 1])
with header_col1:
    st.markdown("# 🎯 Skill ROI Forecaster")
    st.markdown("### Optimise ton apprentissage. Maximise ton salaire.")
with header_col2:
    st.empty() # Espace pour alignement

if not mes_skills:
    st.warning("👈 Sélectionne tes compétences dans la barre latérale pour commencer.")
    st.stop()

# ── CALCULS & LOGIQUE
niveau_map = {'Junior': 2, 'Mid Level': 4, 'Lead': 3, 'Senior': 5}
input_data = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
for skill in mes_skills:
    if skill in feature_columns: input_data[skill] = 1
input_data['seniority_encoded'] = niveau_map[niveau]
input_data['job_category_software engineer'] = 1

salaire_predit = model_rf.predict(input_data)[0]
skills_manquants = roi_df[~roi_df['skill'].isin(mes_skills)]
meilleur_skill = skills_manquants.iloc[0]

# ── MÉTRIQUES INTERACTIVES
st.markdown("<br>", unsafe_allow_html=True)
m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Salaire Estimé</div>
        <div class="metric-value">${salaire_predit:,.0f}</div>
        <div style='color:#00ff00; font-size:0.8rem;'>▲ Basé sur votre profil</div>
    </div>""", unsafe_allow_html=True)

with m_col2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Priorité d'Apprentissage</div>
        <div class="metric-value">{meilleur_skill['skill'].upper()}</div>
        <div style='color:#e84e1b; font-size:0.8rem;'>ROI Score: {meilleur_skill['roi_score']:.2f}</div>
    </div>""", unsafe_allow_html=True)

with m_col3:
    progress = (len(mes_skills) / len(skills_cols)) * 100
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Maîtrise du Marché</div>
        <div class="metric-value">{len(mes_skills)} / {len(skills_cols)}</div>
        <div style='color:#888; font-size:0.8rem;'>{progress:.1f}% des skills demandés</div>
    </div>""", unsafe_allow_html=True)

# ── GRAPHIQUE 1 : ROI RECOMMANDATIONS (PLOTLY)
st.markdown("## 🏆 Top Skills à acquérir")
recommandations = skills_manquants.head(top_n).sort_values('roi_score', ascending=True)

fig_roi = px.bar(
    recommandations, 
    x='roi_score', 
    y='skill', 
    orientation='h',
    color='roi_score',
    color_continuous_scale=['#333333', '#e84e1b'],
    template='plotly_dark'
)
fig_roi.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis_title="Score de Retour sur Investissement",
    yaxis_title=None,
    coloraxis_showscale=False
)
st.plotly_chart(fig_roi, use_container_width=True)

# ── GRAPHIQUE 2 : PROJECTION DE CARRIÈRE (PLOTLY)
col_a, col_b = st.columns([1, 1])

with col_a:
    st.markdown("## 📈 Évolution Salariale")
    niveaux_list = ['Junior', 'Mid Level', 'Senior', 'Lead']
    sals = []
    for n in niveaux_list:
        temp_inp = input_data.copy()
        temp_inp['seniority_encoded'] = niveau_map[n]
        sals.append(model_rf.predict(temp_inp)[0])
    
    fig_evol = go.Figure()
    fig_evol.add_trace(go.Scatter(
        x=niveaux_list, y=sals,
        mode='lines+markers',
        line=dict(color='#e84e1b', width=4),
        marker=dict(size=10, color='white', line=dict(color='#e84e1b', width=2)),
        fill='tozeroy',
        fillcolor='rgba(232, 78, 27, 0.1)'
    ))
    fig_evol.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350)
    st.plotly_chart(fig_evol, use_container_width=True)

with col_b:
    st.markdown("## 🔗 Synergies de Compétences")
    # Filtrage des règles
    suggestions = rules[rules['antecedents'].apply(lambda x: any(s in x for s in mes_skills))]
    if not suggestions.empty:
        top_sug = suggestions.nlargest(5, 'confidence')
        for _, row in top_sug.iterrows():
            with st.expander(f"💡 Carrière : {list(row['consequents'])[0].upper()}"):
                st.write(f"Les recruteurs qui cherchent **{list(row['antecedents'])[0]}** demandent aussi cet outil dans **{row['confidence']*100:.0f}%** des cas.")
    else:
        st.info("Ajoutez plus de skills pour voir les corrélations.")

# ── FOOTER
st.markdown("<br><hr><center>Maachi Hatim © 2026 | Built with Python & 🔥</center>", unsafe_allow_html=True)