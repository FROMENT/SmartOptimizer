#!/bin/bash
# Weekend Cleanup Example - Nettoyage rapide du weekend

echo "🧹 NETTOYAGE DE WEEKEND"
echo "======================"

# Répertoire de base
HOME_DIR="$HOME"
SMARTOPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1. Vérification sécurité obligatoire
echo "🔒 Étape 1: Vérification sécurité cloud"
"$SMARTOPT_DIR/scripts/quick_cloud_safety_check.sh"

if [ $? -ne 0 ]; then
    echo "❌ Vérification sécurité échouée - Arrêt du nettoyage"
    echo "   Attendez la stabilisation des services cloud"
    exit 1
fi

echo "✅ Sécurité cloud validée"
echo ""

# 2. Vue d'ensemble rapide
echo "🔍 Étape 2: Vue d'ensemble du répertoire home"
python3 "$SMARTOPT_DIR/src/analyzers/ultra_quick_overview.py" "$HOME_DIR"
echo ""

# 3. Nettoyage Downloads
echo "📥 Étape 3: Nettoyage du dossier Downloads"
if [ -d "$HOME_DIR/Downloads" ]; then
    python3 "$SMARTOPT_DIR/src/optimizers/quick_smart_optimizer.py" "$HOME_DIR/Downloads"
else
    echo "   📁 Dossier Downloads non trouvé"
fi
echo ""

# 4. Organisation Desktop
echo "🖥️  Étape 4: Organisation du Desktop"
if [ -d "$HOME_DIR/Desktop" ]; then
    python3 "$SMARTOPT_DIR/src/reorganizers/smart_reorganizer.py" "$HOME_DIR/Desktop"
else
    echo "   📁 Dossier Desktop non trouvé"
fi
echo ""

# 5. Nettoyage rapide des caches
echo "🗑️  Étape 5: Nettoyage des caches (optionnel)"
read -p "Nettoyer les caches système? (y/N): " clean_cache
if [[ $clean_cache =~ ^[Yy]$ ]]; then
    # Cache utilisateur (sécurisé)
    if [ -d "$HOME_DIR/.cache" ]; then
        echo "   🧹 Nettoyage cache utilisateur..."
        find "$HOME_DIR/.cache" -type f -atime +7 -delete 2>/dev/null || true
    fi
    
    # Cache npm (si présent)
    if [ -d "$HOME_DIR/.npm" ]; then
        echo "   📦 Nettoyage cache npm..."
        npm cache clean --force 2>/dev/null || true
    fi
    
    # Cache pip (si présent)  
    if [ -d "$HOME_DIR/.cache/pip" ]; then
        echo "   🐍 Nettoyage cache pip..."
        pip cache purge 2>/dev/null || true
    fi
fi

# 6. Résumé final
echo ""
echo "✅ NETTOYAGE DE WEEKEND TERMINÉ"
echo "==============================="
echo "📊 Actions effectuées:"
echo "   • Vérification sécurité cloud"
echo "   • Vue d'ensemble du home"
echo "   • Optimisation Downloads"
echo "   • Organisation Desktop"
if [[ $clean_cache =~ ^[Yy]$ ]]; then
    echo "   • Nettoyage des caches"
fi

echo ""
echo "📁 Vérifiez les sauvegardes dans:"
echo "   ~/SmartOptimizer_Backups/"
echo ""
echo "💡 Pour un nettoyage plus approfondi:"
echo "   ./examples/monthly_optimization.sh"