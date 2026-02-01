# 🚀 Déployer votre application sur Streamlit Cloud

## 📋 Prérequis

Votre application fonctionne en local avec `streamlit run app.py`. Pour la déployer sur Streamlit Cloud :

## ✅ Étape 1 : Vérifier les fichiers

Assurez-vous que ces fichiers sont présents dans le dossier `sn` :
- ✅ `app.py` (votre application)
- ✅ `requirements.txt` (dépendances)
- ✅ `modele_naive_bayes_credit.pkl` (modèle entraîné)
- ✅ `.streamlit/config.toml` (configuration - optionnel)

## 📤 Étape 2 : Mettre sur GitHub

### 2.1 Initialiser Git (si pas déjà fait)

```bash
cd C:\Users\rickk\OneDrive\Bureau\ing-5\ML&BIGDATA\MACHINE-LEARNing\pratique\MACHINE_LEARNING\sn
git init
```

### 2.2 Ajouter tous les fichiers

```bash
git add app.py
git add requirements.txt
git add modele_naive_bayes_credit.pkl
git add .streamlit/config.toml
```

**⚠️ IMPORTANT** : Le fichier `modele_naive_bayes_credit.pkl` DOIT être ajouté à Git !

### 2.3 Créer un commit

```bash
git commit -m "Application de prédiction de crédit"
```

### 2.4 Créer un repository sur GitHub

1. Allez sur https://github.com
2. Cliquez sur "New repository"
3. Donnez un nom (ex: `prediction-credit`)
4. **Ne cochez PAS** "Add README" (vous avez déjà des fichiers)
5. Cliquez sur "Create repository"

### 2.5 Lier et pousser vers GitHub

```bash
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
git push -u origin main
```

**Remplacez** `VOTRE_USERNAME` et `VOTRE_REPO` par vos valeurs.

## 🌐 Étape 3 : Déployer sur Streamlit Cloud

### 3.1 Se connecter à Streamlit Cloud

1. Allez sur https://streamlit.io/cloud
2. Cliquez sur "Sign up" ou "Log in"
3. Connectez-vous avec votre compte **GitHub**

### 3.2 Créer une nouvelle application

1. Cliquez sur **"New app"**
2. Remplissez le formulaire :
   - **Repository** : Sélectionnez votre repository GitHub
   - **Branch** : `main` (ou `master`)
   - **Main file path** : `app.py` ⚠️ IMPORTANT
   - **App URL** : Choisissez un nom unique (ex: `prediction-credit`)
3. Cliquez sur **"Deploy"**

### 3.3 Attendre le déploiement

- Le build prend 2-5 minutes
- Vous verrez les logs en temps réel
- Une fois terminé, votre app sera accessible sur : `https://prediction-credit.streamlit.app`

## ❌ Problèmes courants

### Erreur : "FileNotFoundError: modele_naive_bayes_credit.pkl"

**Cause** : Le fichier modèle n'est pas sur GitHub

**Solution** :
```bash
git add modele_naive_bayes_credit.pkl
git commit -m "Add model file"
git push
```
Puis redéployez dans Streamlit Cloud (cliquez sur "Reboot app")

### Erreur : "ModuleNotFoundError"

**Cause** : Dépendances manquantes

**Solution** : Vérifiez que `requirements.txt` contient toutes les dépendances nécessaires

### L'application ne se charge pas

**Solution** :
1. Vérifiez les **logs** dans Streamlit Cloud (menu ⋮ > Logs)
2. Testez localement : `streamlit run app.py`
3. Vérifiez que le repository est **public** (ou vous avez Streamlit Pro)

## ✅ Checklist finale

- [ ] Tous les fichiers sont commités sur GitHub
- [ ] `modele_naive_bayes_credit.pkl` est bien dans le repository
- [ ] Le repository est public (ou vous avez Streamlit Pro)
- [ ] L'application fonctionne en local
- [ ] Le "Main file path" dans Streamlit Cloud est `app.py`

## 🎯 Votre application sera accessible sur :

`https://<votre-nom-app>.streamlit.app`
