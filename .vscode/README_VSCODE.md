# 🛠️ Configuration VS Code - SmartOptimizer

## 📋 Fonctionnalités Configurées

### ⚡ **Raccourcis Clavier Utiles**
- `Cmd+Shift+P` → Palette de commandes
- `Cmd+Shift+T` → Tâches (Tasks)
- `F5` → Debug SmartOptimizer
- `Cmd+Shift+F5` → Restart Debug
- `Cmd+K Cmd+S` → Raccourcis clavier

### 🎯 **Tâches Disponibles (Cmd+Shift+P → "Tasks")**
1. **SmartOptimizer: Lancer Interface** → Lance `python3 smart.py`
2. **SmartOptimizer: Vérifier Projet** → Lance `python3 verify_project.py`
3. **SmartOptimizer: Installation** → Lance `python3 install_universal.py`
4. **SmartOptimizer: Tests Rapides** → Lance `./quick_test.sh`
5. **SmartOptimizer: Revue Code** → Lance `python3 code_review.py`
6. **Git: Status et Log** → Affiche l'état Git
7. **Python: Format All Files** → Formate tout le code avec Black
8. **Python: Lint All Files** → Vérifie le code avec Flake8

### 🐛 **Configurations Debug (F5)**
- **Interface Principale** → Debug smart.py
- **Vérification Projet** → Debug verify_project.py
- **Installation** → Debug install_universal.py
- **Dédoublonnage** → Debug dedoublons_rapide.py
- **Modules** → Debug modules src/

### 📝 **Snippets de Code (Tapez le préfixe + Tab)**
- `soclass` → Template classe SmartOptimizer complète
- `sofunc` → Function avec docstring
- `soplatform` → Détection multi-platform
- `soerror` → Gestion d'erreur
- `sosim` → Vérification mode simulation

### 🔧 **Extensions Installées Automatiquement**
- **Python** → Support Python complet
- **Pylint + Flake8** → Analyse de code
- **Black Formatter** → Formatage automatique
- **Jupyter** → Support notebooks
- **Markdown** → Édition documentation
- **GitLens** → Git amélioré
- **Code Runner** → Exécution rapide
- **Spell Checker** → Vérification orthographe

## 🚀 **Utilisation Rapide**

### 1️⃣ **Ouvrir le Projet**
```bash
cd SmartOptimizer
code .
```

### 2️⃣ **Lancer SmartOptimizer**
- **Option 1** : Appuyer sur `F5` → Sélectionner "Interface Principale"
- **Option 2** : `Cmd+Shift+P` → "Tasks" → "SmartOptimizer: Lancer Interface"
- **Option 3** : Terminal intégré → `python3 smart.py`

### 3️⃣ **Développer et Déboguer**
- **Format automatique** : Sauvegarde = formatage automatique
- **Linting en temps réel** : Erreurs soulignées automatiquement
- **Debug points** : Cliquer à gauche du numéro de ligne
- **Terminal intégré** : `Ctrl+\`` (backtick)

### 4️⃣ **Git Integration**
- **Source Control** : Icône dans la barre latérale
- **GitLens** : Informations Git directement dans le code
- **Diff visual** : Comparaison des changements

## 💡 **Conseils Pro**

### 🔥 **Workflow Efficace**
1. `F5` → Lancer en debug pour tester rapidement
2. `Cmd+Shift+T` → Lancer les tâches de vérification
3. Modification du code → Sauvegarde = formatage automatique
4. `Cmd+Shift+G` → Git pour commit rapide

### 📊 **Productivité**
- **Multi-curseur** : `Alt+Click` pour éditer plusieurs lignes
- **Recherche globale** : `Cmd+Shift+F`
- **Palette commandes** : `Cmd+Shift+P` pour tout faire
- **Terminal multiple** : `Cmd+Shift+\`` pour nouveau terminal

### 🎯 **Spécial SmartOptimizer**
- Mots SmartOptimizer ajoutés au spell checker
- Formatage selon standards du projet (Black, 88 chars)
- Tâches personnalisées pour tous les scripts
- Debug configuré pour chaque module

## 🔧 **Personnalisation**

### Modifier les Tâches
Éditer `.vscode/tasks.json` pour ajouter vos propres tâches.

### Ajouter des Snippets
Éditer `.vscode/python.code-snippets` pour vos templates.

### Changer les Paramètres
Éditer `.vscode/settings.json` pour personnaliser VS Code.

---

**VS Code configuré pour SmartOptimizer ! 🚀**

*Développement professionnel avec debug, formatage, et intégration Git complète.*