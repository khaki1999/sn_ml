"""
Application Streamlit améliorée pour la prédiction de crédit
Version avec interface enrichie, visualisations et fonctionnalités avancées
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# Configuration de la page
st.set_page_config(
    page_title="Prédicteur de Crédit - Naïve Bayes",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Chargement du modèle
@st.cache_resource
def load_model():
    """Charge le modèle avec cache"""
    try:
        return joblib.load('modele_naive_bayes_credit.pkl')
    except FileNotFoundError:
        st.error("❌ Modèle non trouvé! Le fichier 'modele_naive_bayes_credit.pkl' est manquant.")
        st.stop()
        return None

# Chargement des données 
@st.cache_data
def load_data():
    """Charge les données d'entraînement si disponibles"""
    try:
        return pd.read_csv('AER_credit_card_data.csv')
    except FileNotFoundError:
        return None

# Initialisation
model = load_model()
df_data = load_data()

# Navigation
st.sidebar.title("📋 Navigation")
menu = st.sidebar.radio(
    "Choisir une section",
    ["🏠 Accueil", "🤖 Prédiction", "📊 Analyse des données", "📁 Prédictions multiples"]
)

# ==================== PAGE ACCUEIL ====================
if menu == "🏠 Accueil":
    st.markdown('<h1 class="main-header">💳 Système d\'Aide à la Décision : Carte de Crédit</h1>', unsafe_allow_html=True)
    st.markdown("### Application de Machine Learning utilisant le modèle **Naïve Bayes**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎯 Modèle", "Naïve Bayes", "Gaussian")
    
    with col2:
        if df_data is not None:
            st.metric("📊 Données", f"{len(df_data):,} lignes", "AER Credit Data")
        else:
            st.metric("📊 Données", "Non disponibles", "")
    
    with col3:
        st.metric("⚡ Précision", "~84%", "Test set")
    
    st.markdown("---")
    
    st.subheader("📖 À propos de l'application")
    
    st.info("""
    Cette application permet de prédire l'acceptation d'une demande de carte de crédit en utilisant 
    un modèle de Machine Learning (Naïve Bayes). 
    
    **Fonctionnalités :**
    - ✅ Prédiction individuelle avec visualisations
    - ✅ Prédictions multiples via fichier CSV
    - ✅ Analyse exploratoire des données
    - ✅ Export des résultats
    """)
    
    st.subheader("🔧 Comment utiliser")
    
    tab1, tab2, tab3 = st.tabs(["Prédiction individuelle", "Prédictions multiples", "Analyse"])
    
    with tab1:
        st.write("""
        1. Allez dans la section **"🤖 Prédiction"**
        2. Remplissez les informations du demandeur dans les champs
        3. Cliquez sur **"Analyser le dossier"**
        4. Consultez les résultats avec les graphiques de probabilités
        """)
    
    with tab2:
        st.write("""
        1. Allez dans la section **"📁 Prédictions multiples"**
        2. Téléchargez un fichier CSV avec les colonnes requises
        3. L'application effectuera les prédictions pour toutes les lignes
        4. Téléchargez les résultats en CSV
        """)
    
    with tab3:
        st.write("""
        1. Allez dans la section **"📊 Analyse des données"**
        2. Explorez les statistiques et visualisations
        3. Analysez les corrélations entre les variables
        """)

# ==================== PAGE PRÉDICTION ====================
elif menu == "🤖 Prédiction":
    st.markdown('<h1 class="main-header">🤖 Prédiction de Crédit</h1>', unsafe_allow_html=True)
    
    st.info("💡 Remplissez tous les champs ci-dessous pour obtenir une prédiction")
    
    # Formulaire en colonnes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Informations financières")
        reports = st.number_input(
            "Nombre d'incidents de paiement",
            min_value=0,
            max_value=20,
            value=0,
            help="Nombre de rapports de crédit défavorables"
        )
        income = st.number_input(
            "Revenu annuel (x10 000 $)",
            min_value=0.0,
            value=3.5,
            step=0.1,
            format="%.2f",
            help="Revenu annuel en dizaines de milliers de dollars"
        )
    
    with col2:
        st.markdown("### 🏠 Informations personnelles")
        age = st.slider("Âge", 18, 100, 30)
        owner = st.selectbox(
            "Propriétaire de son logement ?",
            ("Oui", "Non"),
            help="Le demandeur est-il propriétaire ?"
        )
        selfemp = st.selectbox(
            "Travailleur indépendant ?",
            ("Oui", "Non"),
            help="Le demandeur travaille-t-il à son compte ?"
        )
        dependents = st.number_input(
            "Nombre de personnes à charge",
            min_value=0,
            max_value=10,
            value=0
        )
    
    with col3:
        st.markdown("### 💳 Informations bancaires")
        months = st.number_input(
            "Mois à l'adresse actuelle",
            min_value=0,
            value=12,
            help="Ancienneté à l'adresse actuelle"
        )
        majorcards = st.selectbox(
            "Possède d'autres cartes majeures ?",
            (1, 0),
            format_func=lambda x: "Oui" if x == 1 else "Non"
        )
        active = st.number_input(
            "Nombre de comptes de crédit actifs",
            min_value=0,
            value=5
        )
    
    # Conversion des valeurs
    owner_val = 1 if owner == "Oui" else 0
    selfemp_val = 1 if selfemp == "Oui" else 0
    
    # Création du DataFrame
    input_data = {
        'reports': [reports],
        'age': [age],
        'income': [income],
        'owner': [owner_val],
        'selfemp': [selfemp_val],
        'dependents': [dependents],
        'months': [months],
        'majorcards': [majorcards],
        'active': [active]
    }
    input_df = pd.DataFrame(input_data)
    
    # Affichage du résumé
    st.markdown("---")
    col_summary1, col_summary2 = st.columns([1, 2])
    
    with col_summary1:
        st.subheader("📋 Résumé du profil")
        summary_df = input_df.T.rename(columns={0: 'Valeur'})
        summary_df.index.name = 'Caractéristique'
        st.dataframe(summary_df, use_container_width=True)
    
    with col_summary2:
        st.subheader("🎯 Résultat de l'analyse")
        
        if st.button('🔮 Analyser le dossier', type="primary", use_container_width=True):
            try:
                # Vérification de l'ordre des colonnes
                expected_cols = ['reports', 'age', 'income', 'owner', 'selfemp', 
                               'dependents', 'months', 'majorcards', 'active']
                input_df_ordered = input_df[expected_cols]
                
                # Prédiction
                prediction = model.predict(input_df_ordered)[0]
                prediction_proba = model.predict_proba(input_df_ordered)[0]
                
                # Affichage du résultat
                col_result1, col_result2, col_result3 = st.columns(3)
                
                with col_result1:
                    if prediction == 1:
                        st.success("✅ **DEMANDE APPROUVÉE**")
                        st.balloons()
                    else:
                        st.error("❌ **DEMANDE REFUSÉE**")
                
                with col_result2:
                    confidence = max(prediction_proba) * 100
                    st.metric("Confiance", f"{confidence:.2f}%")
                
                with col_result3:
                    proba_accept = prediction_proba[1] if len(prediction_proba) > 1 else prediction_proba[0]
                    st.metric("Probabilité d'acceptation", f"{proba_accept * 100:.2f}%")
                
                # Graphique des probabilités
                st.markdown("### 📊 Probabilités détaillées")
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
                
                # Graphique en barres
                classes = ['Refusé', 'Accepté']
                colors = ['#ff6b6b', '#51cf66']
                bars = ax1.bar(classes, prediction_proba * 100, color=colors, alpha=0.8, edgecolor='black')
                ax1.set_ylabel('Probabilité (%)', fontsize=12)
                ax1.set_title('Probabilités de Prédiction', fontsize=14, fontweight='bold')
                ax1.set_ylim([0, 100])
                ax1.grid(axis='y', alpha=0.3)
                
                # Ajouter les valeurs sur les barres
                for i, (bar, prob) in enumerate(zip(bars, prediction_proba)):
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{prob*100:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
                
                # Graphique circulaire
                ax2.pie(prediction_proba * 100, labels=classes, colors=colors, autopct='%1.1f%%',
                       startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
                ax2.set_title('Répartition des Probabilités', fontsize=14, fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig)
                
                # Conseils métier
                score = prediction_proba[1] if len(prediction_proba) > 1 else prediction_proba[0]
                st.markdown("### 💡 Analyse du profil")
                
                if score > 0.8:
                    st.success("💡 **Profil excellent** : Risque très faible. Demande recommandée.")
                elif score > 0.5:
                    st.warning("⚠️ **Profil intermédiaire** : Vérification manuelle conseillée. Analyse approfondie recommandée.")
                else:
                    st.error("🚨 **Profil à risque** : Antécédents ou revenus insuffisants. Demande non recommandée.")
                
                # Barre de progression
                st.progress(score)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la prédiction: {str(e)}")
                st.info("💡 Vérifiez que toutes les valeurs sont correctement saisies.")

# ==================== PAGE ANALYSE DES DONNÉES ====================
elif menu == "📊 Analyse des données":
    st.markdown('<h1 class="main-header">📊 Analyse Exploratoire des Données</h1>', unsafe_allow_html=True)
    
    if df_data is None:
        st.warning("⚠️ Les données d'entraînement ne sont pas disponibles. Le fichier 'AER_credit_card_data.csv' est manquant.")
    else:
        tab1, tab2, tab3 = st.tabs(["📋 Vue d'ensemble", "📈 Statistiques", "🔗 Corrélations"])
        
        with tab1:
            st.subheader("Données complètes")
            st.dataframe(df_data.head(20), use_container_width=True)
            
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.write("**Informations sur le dataset:**")
                st.write(f"- Nombre de lignes: {len(df_data):,}")
                st.write(f"- Nombre de colonnes: {len(df_data.columns)}")
                st.write(f"- Mémoire utilisée: {df_data.memory_usage(deep=True).sum() / 1024:.2f} KB")
            
            with col_info2:
                st.write("**Types de données:**")
                st.write(df_data.dtypes)
        
        with tab2:
            st.subheader("Statistiques descriptives")
            st.dataframe(df_data.describe(), use_container_width=True)
            
            # Distribution d'une variable
            st.subheader("Distribution des variables")
            numeric_cols = df_data.select_dtypes(include=[np.number]).columns.tolist()
            if 'card' in numeric_cols:
                numeric_cols.remove('card')
            
            selected_col = st.selectbox("Sélectionner une variable", numeric_cols)
            
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            
            # Histogramme
            axes[0].hist(df_data[selected_col].dropna(), bins=30, edgecolor='black', alpha=0.7, color='#1f77b4')
            axes[0].set_title(f'Distribution de {selected_col}', fontsize=12, fontweight='bold')
            axes[0].set_xlabel(selected_col)
            axes[0].set_ylabel('Fréquence')
            axes[0].grid(alpha=0.3)
            
            # Box plot
            axes[1].boxplot(df_data[selected_col].dropna())
            axes[1].set_title(f'Box Plot de {selected_col}', fontsize=12, fontweight='bold')
            axes[1].set_ylabel(selected_col)
            axes[1].grid(alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
        
        with tab3:
            st.subheader("Matrice de corrélation")
            
            numeric_df = df_data.select_dtypes(include=[np.number])
            if len(numeric_df.columns) > 0:
                corr_matrix = numeric_df.corr()
                
                fig, ax = plt.subplots(figsize=(12, 10))
                sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                           center=0, square=True, linewidths=1, ax=ax, cbar_kws={"shrink": 0.8})
                plt.title('Matrice de Corrélation', fontsize=14, fontweight='bold')
                st.pyplot(fig)
            else:
                st.info("Aucune variable numérique pour la corrélation")

# ==================== PAGE PRÉDICTIONS MULTIPLES ====================
elif menu == "📁 Prédictions multiples":
    st.markdown('<h1 class="main-header">📁 Prédictions Multiples</h1>', unsafe_allow_html=True)
    
    st.info("""
    💡 Téléchargez un fichier CSV contenant les informations des demandeurs de crédit.
    Le fichier doit contenir les colonnes suivantes :
    - `reports` : Nombre d'incidents de paiement
    - `age` : Âge
    - `income` : Revenu annuel (x10 000 $)
    - `owner` : Propriétaire (1=Oui, 0=Non)
    - `selfemp` : Travailleur indépendant (1=Oui, 0=Non)
    - `dependents` : Nombre de personnes à charge
    - `months` : Mois à l'adresse actuelle
    - `majorcards` : Autres cartes majeures (1=Oui, 0=Non)
    - `active` : Nombre de comptes de crédit actifs
    """)
    
    uploaded_file = st.file_uploader("Choisir un fichier CSV", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            
            st.success(f"✅ Fichier chargé avec succès! {len(df_upload)} lignes trouvées.")
            
            # Aperçu
            st.subheader("📋 Aperçu des données")
            st.dataframe(df_upload.head(10), use_container_width=True)
            
            # Vérification des colonnes requises
            required_cols = ['reports', 'age', 'income', 'owner', 'selfemp', 
                           'dependents', 'months', 'majorcards', 'active']
            missing_cols = [col for col in required_cols if col not in df_upload.columns]
            
            if missing_cols:
                st.error(f"❌ Colonnes manquantes: {', '.join(missing_cols)}")
            else:
                if st.button("🔮 Effectuer les prédictions", type="primary"):
                    with st.spinner("⏳ Traitement en cours..."):
                        try:
                            # Sélection des colonnes dans le bon ordre
                            df_processed = df_upload[required_cols].copy()
                            
                            # Prédictions
                            predictions = model.predict(df_processed)
                            predictions_proba = model.predict_proba(df_processed)
                            
                            # Ajout des résultats
                            df_results = df_upload.copy()
                            df_results['Prédiction'] = ['Accepté' if p == 1 else 'Refusé' for p in predictions]
                            df_results['Confiance (%)'] = [max(proba) * 100 for proba in predictions_proba]
                            df_results['Probabilité Accepté (%)'] = [proba[1] * 100 if len(proba) > 1 else proba[0] * 100 for proba in predictions_proba]
                            df_results['Probabilité Refusé (%)'] = [proba[0] * 100 for proba in predictions_proba]
                            
                            st.success(f"✅ {len(df_results)} prédictions effectuées avec succès!")
                            
                            # Statistiques
                            col_stat1, col_stat2, col_stat3 = st.columns(3)
                            
                            with col_stat1:
                                acceptes = (df_results['Prédiction'] == 'Accepté').sum()
                                st.metric("✅ Acceptés", acceptes)
                            
                            with col_stat2:
                                refuses = (df_results['Prédiction'] == 'Refusé').sum()
                                st.metric("❌ Refusés", refuses)
                            
                            with col_stat3:
                                taux = (acceptes / len(df_results)) * 100
                                st.metric("📊 Taux d'acceptation", f"{taux:.1f}%")
                            
                            # Affichage des résultats
                            st.subheader("📊 Résultats détaillés")
                            st.dataframe(df_results, use_container_width=True, height=400)
                            
                            # Graphique des résultats
                            fig, ax = plt.subplots(figsize=(10, 6))
                            counts = df_results['Prédiction'].value_counts()
                            colors = ['#51cf66' if idx == 'Accepté' else '#ff6b6b' for idx in counts.index]
                            bars = ax.bar(counts.index, counts.values, color=colors, alpha=0.8, edgecolor='black')
                            ax.set_ylabel('Nombre de demandes', fontsize=12)
                            ax.set_title('Répartition des Prédictions', fontsize=14, fontweight='bold')
                            ax.grid(axis='y', alpha=0.3)
                            
                            # Ajouter les valeurs sur les barres
                            for bar in bars:
                                height = bar.get_height()
                                ax.text(bar.get_x() + bar.get_width()/2., height,
                                       f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')
                            
                            plt.tight_layout()
                            st.pyplot(fig)
                            
                            # Export CSV
                            csv = df_results.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="📥 Télécharger les résultats (CSV)",
                                data=csv,
                                file_name="predictions_credit.csv",
                                mime="text/csv"
                            )
                            
                        except Exception as e:
                            st.error(f"❌ Erreur lors des prédictions: {str(e)}")
                            st.info("💡 Vérifiez que les données sont au bon format et contiennent les colonnes requises.")
        
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement du fichier: {str(e)}")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Modèle : Naïve Bayes (Gaussian) | Source : AER Credit Data")
