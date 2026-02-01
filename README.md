# 💳 Application de Prédiction de Crédit

Application Streamlit utilisant le modèle Naïve Bayes pour la prédiction d'acceptation de crédit.

## 🚀 Déploiement sur Streamlit Cloud

### Guide rapide

1. **Mettre le code sur GitHub**
2. **Aller sur** https://streamlit.io/cloud
3. **Se connecter** avec GitHub
4. **Créer une nouvelle app** :
   - Repository : Votre repo GitHub
   - Branch : `main`
   - Main file path : `app.py`
5. **Déployer** !


## 📋 Fichiers requis

- `app.py` - Application principale
- `requirements.txt` - Dépendances
- `modele_naive_bayes_credit.pkl` - Modèle entraîné
- `.streamlit/config.toml` - Configuration

## 🔧 Utilisation locale

```bash
streamlit run app.py
```

## ⚠️ Important pour le déploiement

Le fichier `modele_naive_bayes_credit.pkl` **DOIT** être commité sur GitHub pour que Streamlit Cloud puisse le charger.
