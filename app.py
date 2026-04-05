import streamlit as st
import joblib
import matplotlib.pyplot as plt
import pandas as pd

# ── CHARGER LES MODÈLES
model_rf = joblib.load('random_forest_model.pkl')
rules = joblib.load('apriori_rules.pkl')
roi_df = joblib.load('roi_df.pkl')
feature_columns = joblib.load('feature_columns.pkl')
skills_cols = roi_df['skill'].tolist()

# ── TITRE
st.title('🎯 Skill ROI Forecaster')
st.subheader('Quelles competences apprendre pour trouver un emploi plus vite ?')

# ── SIDEBAR
st.sidebar.header('Ton profil')
mes_skills = st.sidebar.multiselect(
    'Choisis tes skills actuels :',
    options=skills_cols,
    default=['python', 'sql']
)
top_n = st.sidebar.slider('Nombre de recommandations :', 3, 10, 5)

# ── SECTION 1 : ROI SCORE
st.header('🏆 Tes recommandations personnalisées')
skills_manquants = roi_df[~roi_df['skill'].isin(mes_skills)]
recommandations = skills_manquants.head(top_n)
st.dataframe(recommandations[['skill', 'avg_salary', 'roi_score']])

fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(recommandations['skill'][::-1], recommandations['roi_score'][::-1], color='#e84e1b')
ax.set_title('Skills recommandes pour toi')
ax.set_xlabel('ROI Score')
st.pyplot(fig)

# ── SECTION 2 : PRÉDICTION SALAIRE
st.header('💰 Prediction de ton Salaire')

if mes_skills:
    input_data = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
    
    for skill in mes_skills:
        if skill in feature_columns:
            input_data[skill] = 1
    
    input_data['seniority_encoded'] = 2
    input_data['job_category_software engineer'] = 1

    salaire_predit = model_rf.predict(input_data)[0]
    st.metric('Salaire estime', f'${salaire_predit:,.0f}')
else:
    st.warning('Choisis au moins un skill dans ton profil !')
# ── SECTION 3 : COMBINAISONS SKILLS
st.header('🔗 Combinaisons de Skills')

if mes_skills:
    suggestions = rules[rules['antecedents'].apply(
        lambda x: any(skill in x for skill in mes_skills)
    )]
    
    if len(suggestions) > 0:
        st.write('Les skills qui vont souvent avec les tiens :')
        top_suggestions = suggestions.nlargest(5, 'confidence').copy()
        
        # Convertir frozenset en texte
        top_suggestions['antecedents'] = top_suggestions['antecedents'].apply(lambda x: ', '.join(x))
        top_suggestions['consequents'] = top_suggestions['consequents'].apply(lambda x: ', '.join(x))
        
        st.dataframe(top_suggestions[['antecedents', 'consequents', 'confidence']])
    else:
        st.info('Pas de combinaisons trouvees pour tes skills !')
else:
    st.warning('Choisis au moins un skill dans ton profil !')