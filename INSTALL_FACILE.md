# 🚀 Installation Facile SmartOptimizer

## ⚡ Sur votre Mac - 3 Étapes

### 1️⃣ Ouvrir le Terminal
```bash
# Applications > Utilitaires > Terminal
# Ou Cmd+Espace puis taper "Terminal"
```

### 2️⃣ Aller dans le dossier SmartOptimizer
```bash
cd SmartOptimizer
```

### 3️⃣ Lancer SmartOptimizer
```bash
python3 smart.py --detect
```

## 🎯 Commandes Rapides

### 📊 Voir mes services cloud
```bash
python3 smart.py --detect
```
**→ Montre iCloud, Google Drive, OneDrive, Dropbox avec leurs tailles**

### 🏢 Analyser OneDrive Entreprise
```bash
python3 smart.py --business
```
**→ Détecte les tenants OneDrive Business/Enterprise**

### 🔍 Vue d'ensemble de mon Mac
```bash
python3 smart.py --overview
```
**→ Montre les plus gros dossiers de votre Mac**

### ⚙️ Configuration automatique
```bash
python3 smart.py --install
```
**→ Configure SmartOptimizer pour votre Mac**

## 🌟 Interface Menu (Optionnel)

Pour une interface avec menu interactif :
```bash
python3 smart.py
```

Puis choisir les options par numéro (1, 2, 3, etc.)

## ✅ Test Rapide - Fonctionne ?

Copiez-collez cette commande :
```bash
cd SmartOptimizer && python3 smart.py --detect
```

**Si ça marche :** Vous voyez vos services cloud détectés ! 🎉

**Si erreur :** Vérifiez que vous êtes dans le bon dossier :
```bash
pwd
ls smart.py
```

## 🆘 Problèmes Courants

### "No such file or directory"
```bash
# Vérifier où vous êtes
pwd

# Chercher le dossier SmartOptimizer
ls -la | grep Smart

# Si trouvé, aller dedans
cd SmartOptimizer
```

### "Python not found"
```bash
# Essayer python au lieu de python3
python smart.py --detect

# Ou installer Python avec Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
```

## 🎉 Prêt à Utiliser !

Une fois que `python3 smart.py --detect` fonctionne, vous pouvez :

✅ **Détecter** tous vos services cloud  
✅ **Analyser** OneDrive Entreprise  
✅ **Voir** l'espace utilisé sur votre Mac  
✅ **Simuler** des optimisations en sécurité  

**SmartOptimizer est maintenant opérationnel ! 🚀**