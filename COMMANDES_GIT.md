# 📝 Commandes Git pour le déploiement

## 🚀 Commandes à exécuter dans PowerShell

Ouvrez PowerShell dans le dossier `sn` et exécutez ces commandes :

### 1. Vérifier l'état Git

```powershell
cd "C:\Users\rickk\OneDrive\Bureau\ing-5\ML&BIGDATA\MACHINE-LEARNing\pratique\MACHINE_LEARNING\sn"
git status
```

### 2. Ajouter les fichiers (si pas déjà fait)

```powershell
git add app.py
git add requirements.txt
git add modele_naive_bayes_credit.pkl
git add .streamlit/config.toml
git add .gitignore
```

### 3. Créer un commit

```powershell
git commit -m "Application de prediction de credit - Pret pour Streamlit Cloud"
```

### 4. Vérifier que le modèle est bien inclus

```powershell
git ls-files | Select-String "modele_naive_bayes_credit.pkl"
```

Si cette commande ne retourne rien, le fichier n'est pas suivi par Git. Ajoutez-le :
```powershell
git add modele_naive_bayes_credit.pkl
git commit -m "Add model file"
```

### 5. Lier à GitHub (première fois seulement)

```powershell
git remote add origin https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
```

**Remplacez** :
- `VOTRE_USERNAME` par votre nom d'utilisateur GitHub
- `VOTRE_REPO` par le nom de votre repository

### 6. Pousser vers GitHub

```powershell
git branch -M main
git push -u origin main
```

## ⚠️ Si le repository existe déjà

Si vous avez déjà un repository GitHub :

```powershell
git remote set-url origin https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
git push -u origin main
```

## 🔍 Vérifications importantes

### Vérifier que tous les fichiers sont commités

```powershell
git ls-files
```

Vous devriez voir :
- `app.py`
- `requirements.txt`
- `modele_naive_bayes_credit.pkl` ⚠️ CRITIQUE
- `.streamlit/config.toml`

### Vérifier que le modèle est bien là

```powershell
Test-Path "modele_naive_bayes_credit.pkl"
```

Doit retourner `True`
