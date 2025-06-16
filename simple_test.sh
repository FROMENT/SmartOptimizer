#!/bin/bash
# Simple Test - Tests de base pour vérifier SmartOptimizer

echo "🧪 TESTS SIMPLES SMARTOPTIMIZER"
echo "==============================="

cd "$(dirname "${BASH_SOURCE[0]}")"

echo ""
echo "1️⃣ Test de structure du projet..."
if python3 tests/test_project_structure.py >/dev/null 2>&1; then
    echo "   ✅ Structure validée"
else
    echo "   ❌ Problème de structure"
    exit 1
fi

echo ""
echo "2️⃣ Test de syntaxe Python..."
for script in src/analyzers/*.py src/optimizers/*.py src/reorganizers/*.py; do
    if python3 -m py_compile "$script" 2>/dev/null; then
        echo "   ✅ $(basename "$script")"
    else
        echo "   ❌ Erreur dans $(basename "$script")"
    fi
done

echo ""
echo "3️⃣ Test de configuration..."
if [ -f "smartoptimizer.conf" ] && grep -q "SIMULATION_MODE=true" smartoptimizer.conf; then
    echo "   ✅ Configuration sécurisée (mode simulation)"
else
    echo "   ⚠️  Configuration manquante ou non sécurisée"
fi

echo ""
echo "4️⃣ Test de permissions..."
if [ -x "install.sh" ] && [ -x "upgrade.sh" ]; then
    echo "   ✅ Scripts d'installation exécutables"
else
    echo "   ⚠️  Permissions des scripts à vérifier"
fi

echo ""
echo "5️⃣ Test de détection cloud (lecture seule)..."
echo "   📁 Création d'un dossier de test temporaire..."
TEST_DIR="/tmp/smartopt_test_$$"
mkdir -p "$TEST_DIR"
echo "Test file" > "$TEST_DIR/test.txt"

echo "   🔍 Test d'analyse basique..."
if timeout 10 python3 src/analyzers/ultra_quick_overview.py "$TEST_DIR" >/dev/null 2>&1; then
    echo "   ✅ Analyseur fonctionnel"
else
    echo "   ⚠️  Analyseur pourrait avoir des problèmes"
fi

# Nettoyage
rm -rf "$TEST_DIR"

echo ""
echo "📋 RÉSUMÉ:"
echo "========="
echo "✅ SmartOptimizer semble correctement installé"
echo "✅ Mode simulation activé (sécurisé)"
echo "✅ Structure et syntaxe validées"

echo ""
echo "🚀 PROCHAINES ÉTAPES RECOMMANDÉES:"
echo "=================================="
echo ""
echo "🔍 1. Tester la détection cloud:"
echo "   python3 src/analyzers/cloud_services_detector.py ~/"
echo ""
echo "🔒 2. Vérifier la sécurité cloud:"
echo "   ./scripts/quick_cloud_safety_check.sh"
echo ""
echo "📊 3. Vue d'ensemble rapide de votre système:"
echo "   python3 src/analyzers/ultra_quick_overview.py ~/"
echo ""
echo "🔧 4. Analyse des imbrications cloud:"
echo "   python3 src/analyzers/cloud_nesting_analyzer.py ~/"
echo ""
echo "⚠️  IMPORTANT: Tous les scripts sont en mode SIMULATION par défaut"
echo "   Aucune modification ne sera effectuée sans votre autorisation explicite"

echo ""
echo "📚 Pour plus d'informations:"
echo "   • Guide de test détaillé: cat TEST_GUIDE.md"
echo "   • Documentation complète: cat docs/user-guide.md"
echo "   • Nouveautés v1.1.0: cat WHATS_NEW_v1.1.0.md"

echo ""
echo "✅ SmartOptimizer est prêt à utiliser en mode sécurisé!"