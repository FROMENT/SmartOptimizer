#!/bin/bash
# SmartOptimizer Installation Script

echo "🚀 INSTALLATION DE SMARTOPTIMIZER v1.1.0"
echo "========================================="
echo "🆕 Nouveautés v1.1.0:"
echo "   • Détection et optimisation de tous les services cloud"
echo "   • Analyse des imbrications cloud (iCloud, OneDrive, Google Drive, etc.)"
echo "   • Déduplication intelligente inter-cloud"
echo "   • Stratégies d'optimisation spécialisées par service"
echo ""

# Vérifier Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 requis mais non trouvé"
    echo "   Installer Python 3.8+ avant de continuer"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION détecté"

# Créer l'environnement virtuel (optionnel)
read -p "🤔 Créer un environnement virtuel? (y/N): " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv smartoptimizer_env
    source smartoptimizer_env/bin/activate
    echo "✅ Environnement virtuel activé"
    
    # Installer les dépendances optionnelles
    echo "📥 Installation des dépendances..."
    pip install --upgrade pip
    pip install Pillow moviepy mutagen 2>/dev/null || echo "⚠️  Dépendances optionnelles non installées (mode simple disponible)"
fi

# Rendre les scripts exécutables
echo "🔧 Configuration des permissions..."
chmod +x scripts/*.sh
chmod +x src/analyzers/*.py
chmod +x src/optimizers/*.py
chmod +x src/reorganizers/*.py
chmod +x src/utils/*.py

# Créer les liens symboliques (optionnel)
read -p "🔗 Créer des liens symboliques dans /usr/local/bin? (y/N): " create_links
if [[ $create_links =~ ^[Yy]$ ]]; then
    if [ "$EUID" -eq 0 ]; then
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
        ln -sf "$SCRIPT_DIR/src/analyzers/ultra_quick_overview.py" /usr/local/bin/smartopt-overview
        ln -sf "$SCRIPT_DIR/src/optimizers/quick_smart_optimizer.py" /usr/local/bin/smartopt-quick
        ln -sf "$SCRIPT_DIR/scripts/quick_cloud_safety_check.sh" /usr/local/bin/smartopt-safety
        echo "✅ Liens symboliques créés"
    else
        echo "⚠️  Permissions admin requises pour les liens symboliques"
        echo "   Réexécuter avec sudo si désiré"
    fi
fi

# Vérifier les dépendances système
echo ""
echo "🔍 Vérification des dépendances système:"

# Vérifier 'du' command
if command -v du &> /dev/null; then
    echo "  ✅ du (analyse de taille)"
else
    echo "  ❌ du manquant"
fi

# Vérifier 'find' command  
if command -v find &> /dev/null; then
    echo "  ✅ find (recherche de fichiers)"
else
    echo "  ❌ find manquant"
fi

# Vérifier Git (optionnel)
if command -v git &> /dev/null; then
    echo "  ✅ git (détection de repos)"
else
    echo "  ⚠️  git absent (détection de repos désactivée)"
fi

# Test rapide
echo ""
echo "🧪 Test d'installation..."
if python3 -c "import sys; print('Python OK')" 2>/dev/null; then
    echo "✅ Installation réussie!"
else
    echo "❌ Problème d'installation détecté"
    exit 1
fi

# Afficher les commandes disponibles
echo ""
echo "🎯 COMMANDES DISPONIBLES:"
echo "========================"
echo "📊 Vue d'ensemble rapide:"
echo "   python3 src/analyzers/ultra_quick_overview.py ~/"
echo ""
echo "🔒 Vérification sécurité:"
echo "   ./scripts/quick_cloud_safety_check.sh"
echo ""
echo "☁️  Optimisation cloud (NOUVEAU):"
echo "   python3 src/analyzers/cloud_services_detector.py ~/"
echo "   python3 src/analyzers/cloud_nesting_analyzer.py ~/"
echo "   ./examples/cloud_deduplication_strategy.sh"
echo ""
echo "🧹 Optimisation rapide:"
echo "   python3 src/optimizers/quick_smart_optimizer.py ~/Downloads"
echo ""
echo "🗂️  Réorganisation:"
echo "   python3 src/reorganizers/smart_reorganizer.py ~/Desktop"
echo ""
echo "📚 Documentation complète:"
echo "   cat README.md"

echo ""
echo "🎉 SmartOptimizer installé avec succès!"
echo "   Consulter README.md pour la documentation complète"

# Créer un fichier de configuration utilisateur
cat > smartoptimizer.conf << EOF
# Configuration SmartOptimizer
BACKUP_DIR="$HOME/SmartOptimizer_Backups"
SIMULATION_MODE=true
CONFIDENCE_THRESHOLD=70
CLOUD_SAFETY_CHECK=true
EOF

echo "⚙️  Configuration créée: smartoptimizer.conf"