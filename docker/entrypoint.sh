#!/bin/bash
# SmartOptimizer Docker Entrypoint

set -e

echo "🐳 SMARTOPTIMIZER DOCKER"
echo "======================="

# Fonction d'aide
show_help() {
    echo "Commandes disponibles:"
    echo "  overview [path]    - Vue d'ensemble rapide (défaut: /home/optimizer/data)"
    echo "  analyze [path]     - Analyse complète"
    echo "  optimize [path]    - Optimisation intelligente"
    echo "  reorganize [path]  - Réorganisation des fichiers"
    echo "  safety-check       - Vérification sécurité cloud"
    echo "  shell             - Shell interactif"
    echo ""
    echo "Variables d'environnement:"
    echo "  SMARTOPT_MODE     - Mode d'opération (safe|normal|aggressive)"
    echo "  SMARTOPT_BACKUP   - Répertoire de sauvegarde"
    echo "  SMARTOPT_CONFIDENCE - Seuil de confiance (0-100)"
}

# Configuration par défaut
DEFAULT_PATH="/home/optimizer/data"
SMARTOPT_MODE=${SMARTOPT_MODE:-safe}
SMARTOPT_BACKUP=${SMARTOPT_BACKUP:-/home/optimizer/backups}
SMARTOPT_CONFIDENCE=${SMARTOPT_CONFIDENCE:-70}

# Créer les répertoires nécessaires
mkdir -p "$SMARTOPT_BACKUP"
mkdir -p "$DEFAULT_PATH"

echo "📊 Configuration:"
echo "  Mode: $SMARTOPT_MODE"
echo "  Backup: $SMARTOPT_BACKUP"
echo "  Confiance: $SMARTOPT_CONFIDENCE%"
echo ""

# Fonction principale
case "${1:-overview}" in
    "overview")
        TARGET_PATH="${2:-$DEFAULT_PATH}"
        echo "🔍 Vue d'ensemble de: $TARGET_PATH"
        python3 src/analyzers/ultra_quick_overview.py "$TARGET_PATH"
        ;;
        
    "analyze")
        TARGET_PATH="${2:-$DEFAULT_PATH}"
        echo "📊 Analyse complète de: $TARGET_PATH"
        python3 src/analyzers/comprehensive_analyzer.py "$TARGET_PATH"
        ;;
        
    "optimize")
        TARGET_PATH="${2:-$DEFAULT_PATH}"
        echo "⚡ Optimisation de: $TARGET_PATH"
        if [ "$SMARTOPT_MODE" = "safe" ]; then
            echo "🔒 Mode sécurisé - Simulation uniquement"
            python3 src/optimizers/quick_smart_optimizer.py "$TARGET_PATH"
        else
            echo "🚀 Mode actif - Optimisation réelle"
            python3 src/optimizers/complete_optimizer.py "$TARGET_PATH"
        fi
        ;;
        
    "reorganize")
        TARGET_PATH="${2:-$DEFAULT_PATH}"
        echo "🗂️  Réorganisation de: $TARGET_PATH"
        python3 src/reorganizers/smart_reorganizer.py "$TARGET_PATH"
        ;;
        
    "safety-check")
        echo "🔒 Vérification sécurité cloud"
        if command -v bash >/dev/null 2>&1; then
            bash scripts/quick_cloud_safety_check.sh
        else
            python3 src/utils/check_cloud_sync_status.py
        fi
        ;;
        
    "shell")
        echo "🐚 Shell interactif"
        exec /bin/bash
        ;;
        
    "help"|"--help"|"-h")
        show_help
        ;;
        
    *)
        echo "❌ Commande inconnue: $1"
        echo ""
        show_help
        exit 1
        ;;
esac

echo ""
echo "✅ Opération terminée"
echo "📁 Données: $DEFAULT_PATH"
echo "🔒 Backups: $SMARTOPT_BACKUP"