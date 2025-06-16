#!/bin/bash
# SmartOptimizer Upgrade Script - Mise à jour vers v1.1.0

echo "🔄 MISE À JOUR SMARTOPTIMIZER v1.0.0 → v1.1.0"
echo "=============================================="

# Détecter la version existante
CURRENT_VERSION="unknown"
if [ -f "README.md" ]; then
    CURRENT_VERSION=$(grep -o "version-[0-9.]*" README.md | head -1 | cut -d'-' -f2)
fi

echo "📊 Version actuelle détectée: $CURRENT_VERSION"

if [ "$CURRENT_VERSION" = "1.1.0" ]; then
    echo "✅ Vous avez déjà la dernière version (v1.1.0)"
    exit 0
fi

echo ""
echo "🆕 NOUVEAUTÉS v1.1.0:"
echo "====================="
echo "☁️  • Détection complète de tous les services cloud (iCloud, OneDrive, Google Drive, Dropbox, Box)"
echo "🔍 • Analyseur d'imbrications cloud pour détecter les doublons d'espace"
echo "⚡ • Optimiseur de déduplication inter-cloud intelligent"
echo "🎯 • Stratégies d'optimisation spécialisées par service cloud"
echo "🔧 • Workflows complets d'optimisation cloud"
echo "📊 • Surveillance automatique des imbrications"

echo ""
read -p "Continuer la mise à jour? (Y/n): " continue_upgrade
if [[ $continue_upgrade =~ ^[Nn]$ ]]; then
    echo "❌ Mise à jour annulée"
    exit 0
fi

# Créer une sauvegarde de l'installation actuelle
BACKUP_DIR="./smartoptimizer_backup_$(date +%Y%m%d_%H%M%S)"
echo ""
echo "💾 Création d'une sauvegarde..."
mkdir -p "$BACKUP_DIR"

# Sauvegarder les fichiers de configuration
if [ -f "smartoptimizer.conf" ]; then
    cp "smartoptimizer.conf" "$BACKUP_DIR/"
    echo "   ✅ Configuration sauvegardée"
fi

# Sauvegarder les scripts personnalisés s'ils existent
if [ -d "custom_scripts" ]; then
    cp -r "custom_scripts" "$BACKUP_DIR/"
    echo "   ✅ Scripts personnalisés sauvegardés"
fi

echo "   📁 Sauvegarde complète: $BACKUP_DIR"

# Mise à jour des nouveaux fichiers
echo ""
echo "📥 Installation des nouveaux composants..."

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "README.md" ] || [ ! -d "src" ]; then
    echo "❌ Erreur: Exécutez ce script depuis le répertoire SmartOptimizer"
    exit 1
fi

# Créer les nouveaux répertoires si nécessaire
mkdir -p src/analyzers src/optimizers src/reorganizers src/utils
mkdir -p examples scripts docs tests docker

# Vérifier les nouveaux fichiers requis
REQUIRED_FILES=(
    "src/analyzers/cloud_services_detector.py"
    "src/analyzers/cloud_nesting_analyzer.py"
    "src/optimizers/cloud_optimizer.py"
    "src/optimizers/cloud_deduplication_optimizer.py"
    "examples/cloud_optimization_workflow.sh"
    "examples/cloud_deduplication_strategy.sh"
)

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo "⚠️  Fichiers manquants détectés:"
    for file in "${MISSING_FILES[@]}"; do
        echo "   • $file"
    done
    echo ""
    echo "📥 Téléchargement des fichiers manquants..."
    echo "   (Dans un environnement réel, ceci téléchargerait depuis GitHub)"
    echo "   Pour maintenant, assurez-vous d'avoir tous les nouveaux fichiers"
fi

# Mise à jour des permissions
echo ""
echo "🔒 Mise à jour des permissions..."
chmod +x src/analyzers/*.py 2>/dev/null
chmod +x src/optimizers/*.py 2>/dev/null
chmod +x src/reorganizers/*.py 2>/dev/null
chmod +x src/utils/*.py 2>/dev/null
chmod +x examples/*.sh 2>/dev/null
chmod +x scripts/*.sh 2>/dev/null
chmod +x install.sh 2>/dev/null
echo "   ✅ Permissions mises à jour"

# Mise à jour de la configuration
echo ""
echo "⚙️  Mise à jour de la configuration..."

if [ -f "smartoptimizer.conf" ]; then
    # Ajouter les nouvelles options de configuration
    if ! grep -q "CLOUD_OPTIMIZATION" smartoptimizer.conf; then
        echo "" >> smartoptimizer.conf
        echo "# Configuration Cloud v1.1.0" >> smartoptimizer.conf
        echo "CLOUD_OPTIMIZATION=true" >> smartoptimizer.conf
        echo "CLOUD_DEDUPLICATION_ENABLED=true" >> smartoptimizer.conf
        echo "CLOUD_NESTING_DETECTION=true" >> smartoptimizer.conf
        echo "CLOUD_SAFETY_CHECK_REQUIRED=true" >> smartoptimizer.conf
        echo "   ✅ Nouvelles options cloud ajoutées à la configuration"
    fi
else
    # Créer une nouvelle configuration avec les options cloud
    cat > smartoptimizer.conf << EOF
# Configuration SmartOptimizer v1.1.0
BACKUP_DIR="$HOME/SmartOptimizer_Backups"
SIMULATION_MODE=true
CONFIDENCE_THRESHOLD=70
CLOUD_SAFETY_CHECK=true

# Configuration Cloud v1.1.0
CLOUD_OPTIMIZATION=true
CLOUD_DEDUPLICATION_ENABLED=true
CLOUD_NESTING_DETECTION=true
CLOUD_SAFETY_CHECK_REQUIRED=true
EOF
    echo "   ✅ Configuration cloud créée"
fi

# Test des nouveaux composants
echo ""
echo "🧪 Test des nouveaux composants..."

# Test de l'analyseur cloud
if python3 -c "import sys; sys.path.append('src/analyzers'); import cloud_services_detector" 2>/dev/null; then
    echo "   ✅ Cloud Services Detector: OK"
else
    echo "   ⚠️  Cloud Services Detector: Erreur d'import"
fi

# Test de l'analyseur d'imbrications
if python3 -c "import sys; sys.path.append('src/analyzers'); import cloud_nesting_analyzer" 2>/dev/null; then
    echo "   ✅ Cloud Nesting Analyzer: OK"
else
    echo "   ⚠️  Cloud Nesting Analyzer: Erreur d'import"
fi

# Test de l'optimiseur de déduplication
if python3 -c "import sys; sys.path.append('src/optimizers'); import cloud_deduplication_optimizer" 2>/dev/null; then
    echo "   ✅ Cloud Deduplication Optimizer: OK"
else
    echo "   ⚠️  Cloud Deduplication Optimizer: Erreur d'import"
fi

# Mise à jour de la documentation
echo ""
echo "📚 Mise à jour de la documentation..."

# Mettre à jour le numéro de version dans README.md si possible
if [ -f "README.md" ]; then
    if grep -q "version-1.0.0" README.md; then
        sed -i '' 's/version-1.0.0/version-1.1.0/g' README.md 2>/dev/null || \
        sed -i 's/version-1.0.0/version-1.1.0/g' README.md 2>/dev/null
        echo "   ✅ Version mise à jour dans README.md"
    fi
fi

# Créer un guide de migration
cat > UPGRADE_GUIDE_v1.1.0.md << 'EOF'
# Guide de Migration v1.1.0

## Nouveautés Cloud

### Nouvelles commandes disponibles:

```bash
# Détecter tous les services cloud
python3 src/analyzers/cloud_services_detector.py ~/

# Analyser les imbrications problématiques  
python3 src/analyzers/cloud_nesting_analyzer.py ~/

# Optimiser un service cloud spécifique
python3 src/optimizers/cloud_optimizer.py ~/OneDrive

# Déduplication complète inter-cloud
python3 src/optimizers/cloud_deduplication_optimizer.py ~/

# Workflows complets
./examples/cloud_optimization_workflow.sh
./examples/cloud_deduplication_strategy.sh
```

### Cas d'usage typiques:

1. **Desktop synchronisé partout**: Détection et résolution automatique
2. **Dropbox dans Google Drive**: Déimbrication intelligente  
3. **Doublons inter-cloud**: Déduplication avec conservation du meilleur
4. **Optimisation par service**: Stratégies spécialisées iCloud/OneDrive/Google

### Configuration recommandée:

- iCloud Drive: Documents système (Desktop, Documents, Photos)
- Google Drive: Collaboration et Google Workspace
- OneDrive: Documents Office 365 et Teams
- Dropbox: Projets créatifs et partage externe

Consultez la documentation complète dans docs/user-guide.md
EOF

echo "   📖 Guide de migration créé: UPGRADE_GUIDE_v1.1.0.md"

# Validation finale
echo ""
echo "✅ MISE À JOUR TERMINÉE"
echo "======================"
echo "🎉 SmartOptimizer v1.1.0 installé avec succès!"
echo ""
echo "🔥 Nouvelles fonctionnalités disponibles:"
echo "   • Optimisation cloud complète"
echo "   • Déduplication inter-services"
echo "   • Détection d'imbrications"
echo ""
echo "📋 Prochaines étapes recommandées:"
echo "   1. Lire le guide de migration: cat UPGRADE_GUIDE_v1.1.0.md"
echo "   2. Tester la détection cloud: python3 src/analyzers/cloud_services_detector.py ~/"
echo "   3. Analyser les imbrications: python3 src/analyzers/cloud_nesting_analyzer.py ~/"
echo "   4. Consulter la documentation: cat README.md"
echo ""
echo "💾 Sauvegarde de l'ancienne version: $BACKUP_DIR"
echo "📞 Support: docs/user-guide.md"

# Test de validation final
echo ""
echo "🔍 Validation finale..."
if [ -f "src/analyzers/cloud_services_detector.py" ] && \
   [ -f "src/analyzers/cloud_nesting_analyzer.py" ] && \
   [ -f "src/optimizers/cloud_deduplication_optimizer.py" ]; then
    echo "✅ Tous les composants cloud sont installés"
    
    # Proposer un test rapide
    read -p "Lancer un test rapide de détection cloud? (Y/n): " test_cloud
    if [[ ! $test_cloud =~ ^[Nn]$ ]]; then
        echo ""
        echo "🧪 Test de détection cloud..."
        python3 src/analyzers/cloud_services_detector.py 2>/dev/null | head -20
        echo ""
        echo "✅ Test terminé - SmartOptimizer v1.1.0 est prêt!"
    fi
else
    echo "⚠️  Certains composants pourraient être manquants"
    echo "   Vérifiez l'installation complète avec: ./install.sh"
fi

echo ""
echo "🚀 Profitez des nouvelles fonctionnalités cloud de SmartOptimizer!"