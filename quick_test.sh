#!/bin/bash
# Quick Test Script - Tests rapides et sécurisés de SmartOptimizer

echo "🧪 TESTS RAPIDES SMARTOPTIMIZER v1.1.0"
echo "======================================"

SMARTOPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$HOME/SmartOptimizer_QuickTest"
PASSED=0
TOTAL=0

# Fonction de test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_exit_code="${3:-0}"
    
    echo ""
    echo "🔍 Test: $test_name"
    echo "   Commande: $test_command"
    
    TOTAL=$((TOTAL + 1))
    
    if eval "$test_command" >/dev/null 2>&1; then
        if [ $? -eq $expected_exit_code ]; then
            echo "   ✅ RÉUSSI"
            PASSED=$((PASSED + 1))
        else
            echo "   ❌ ÉCHEC (code de sortie inattendu)"
        fi
    else
        echo "   ❌ ÉCHEC"
    fi
}

# Préparation
echo "📋 Préparation de l'environnement de test..."
cd "$SMARTOPT_DIR"

# Nettoyer les anciens tests
rm -rf "$TEST_DIR" 2>/dev/null
mkdir -p "$TEST_DIR"

echo "   📁 Répertoire de test: $TEST_DIR"

# ===== TESTS DE BASE =====
echo ""
echo "🟢 === TESTS DE BASE (Aucun Risque) ==="

run_test "Structure du projet" "python3 tests/test_project_structure.py"

run_test "Syntaxe Python - Ultra Quick Overview" "python3 -m py_compile src/analyzers/ultra_quick_overview.py"

run_test "Syntaxe Python - Cloud Services Detector" "python3 -m py_compile src/analyzers/cloud_services_detector.py"

run_test "Syntaxe Python - Cloud Nesting Analyzer" "python3 -m py_compile src/analyzers/cloud_nesting_analyzer.py"

run_test "Syntaxe Python - Cloud Optimizer" "python3 -m py_compile src/optimizers/cloud_optimizer.py"

run_test "Syntaxe Python - Cloud Deduplication Optimizer" "python3 -m py_compile src/optimizers/cloud_deduplication_optimizer.py"

run_test "Permissions install.sh" "test -x install.sh"

run_test "Permissions upgrade.sh" "test -x upgrade.sh"

run_test "Configuration par défaut" "grep -q 'SIMULATION_MODE=true' smartoptimizer.conf"

# ===== TESTS DE DÉTECTION =====
echo ""
echo "🔍 === TESTS DE DÉTECTION (Lecture Seule) ==="

# Créer des fichiers de test
echo "Creating test files..."
echo "Test content 1" > "$TEST_DIR/test1.txt"
echo "Test content 1" > "$TEST_DIR/test1_copy.txt"  # Doublon
echo "Different content" > "$TEST_DIR/test2.txt"
mkdir -p "$TEST_DIR/subdir"
echo "Nested file" > "$TEST_DIR/subdir/nested.txt"

run_test "Ultra Quick Overview sur dossier de test" "timeout 30 python3 src/analyzers/ultra_quick_overview.py '$TEST_DIR'"

# Test de détection cloud sur le home (si pas trop volumineux)
run_test "Détection cloud services (timeout 60s)" "timeout 60 python3 src/analyzers/cloud_services_detector.py '$HOME'"

# ===== TESTS DE SIMULATION =====
echo ""
echo "🟡 === TESTS DE SIMULATION (Mode Sécurisé) ==="

run_test "Quick Optimizer en simulation" "timeout 30 python3 src/optimizers/quick_smart_optimizer.py '$TEST_DIR'"

run_test "Smart Reorganizer en simulation" "timeout 30 python3 src/reorganizers/smart_reorganizer.py '$TEST_DIR'"

# ===== TESTS DE SÉCURITÉ =====
echo ""
echo "🔒 === TESTS DE SÉCURITÉ ==="

run_test "Vérification sécurité cloud" "timeout 30 scripts/quick_cloud_safety_check.sh"

run_test "Check cloud sync status" "timeout 30 python3 src/utils/check_cloud_sync_status.py"

# ===== TESTS DOCKER (Optionnel) =====
echo ""
echo "🐳 === TESTS DOCKER (Optionnel) ==="

if command -v docker >/dev/null 2>&1; then
    run_test "Docker build" "cd docker && timeout 300 docker build -t smartoptimizer-test . >/dev/null 2>&1"
    
    if [ $? -eq 0 ]; then
        run_test "Docker run test" "timeout 60 docker run --rm -v '$TEST_DIR:/home/optimizer/data' smartoptimizer-test overview >/dev/null 2>&1"
    fi
else
    echo "   ⚠️  Docker non disponible - Tests Docker ignorés"
fi

# ===== TESTS DE PERFORMANCE =====
echo ""
echo "⚡ === TESTS DE PERFORMANCE ==="

# Test de rapidité sur petit dataset
START_TIME=$(date +%s)
python3 src/analyzers/ultra_quick_overview.py "$TEST_DIR" >/dev/null 2>&1
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ $DURATION -lt 10 ]; then
    echo "   ✅ Performance Ultra Quick Overview: ${DURATION}s (< 10s)"
    PASSED=$((PASSED + 1))
else
    echo "   ⚠️  Performance Ultra Quick Overview: ${DURATION}s (> 10s attendu)"
fi
TOTAL=$((TOTAL + 1))

# ===== TESTS D'INTÉGRATION =====
echo ""
echo "🔗 === TESTS D'INTÉGRATION ==="

# Test du workflow weekend (en mode simulation forcée)
export SMARTOPT_SIMULATION=true
run_test "Weekend cleanup workflow (simulation)" "timeout 120 bash -c 'yes n | examples/weekend_cleanup.sh' >/dev/null 2>&1"

# ===== RÉSULTATS =====
echo ""
echo "📊 === RÉSULTATS DES TESTS ==="
echo "=========================="

SUCCESS_RATE=$((PASSED * 100 / TOTAL))

echo "✅ Tests réussis: $PASSED"
echo "❌ Tests échoués: $((TOTAL - PASSED))"
echo "📊 Total: $TOTAL"
echo "🎯 Taux de réussite: $SUCCESS_RATE%"

if [ $SUCCESS_RATE -ge 90 ]; then
    echo ""
    echo "🎉 EXCELLENT! SmartOptimizer est prêt à l'emploi"
    echo "   Vous pouvez utiliser le projet en toute confiance"
    
    echo ""
    echo "🚀 Prochaines étapes recommandées:"
    echo "   1. Lire le guide de test complet: cat TEST_GUIDE.md"
    echo "   2. Tester la détection cloud: python3 src/analyzers/cloud_services_detector.py ~/"
    echo "   3. Analyser les imbrications: python3 src/analyzers/cloud_nesting_analyzer.py ~/"
    echo "   4. Workflow complet: ./examples/cloud_optimization_workflow.sh"
    
elif [ $SUCCESS_RATE -ge 70 ]; then
    echo ""
    echo "🟡 ACCEPTABLE - Quelques problèmes mineurs détectés"
    echo "   Le projet est utilisable mais vérifiez les erreurs"
    echo "   Consultez TEST_GUIDE.md pour des tests plus détaillés"
    
else
    echo ""
    echo "❌ PROBLÈMES DÉTECTÉS - Révision nécessaire"
    echo "   Vérifiez l'installation et les dépendances"
    echo "   Consultez TEST_GUIDE.md pour le débogage"
fi

# Nettoyage
echo ""
echo "🧹 Nettoyage..."
rm -rf "$TEST_DIR"

echo ""
echo "📞 Support:"
echo "   • Guide détaillé: cat TEST_GUIDE.md"
echo "   • Documentation: cat docs/user-guide.md"
echo "   • Configuration: cat smartoptimizer.conf"

echo ""
echo "🕒 Test terminé: $(date)"

# Code de sortie
if [ $SUCCESS_RATE -ge 70 ]; then
    exit 0
else
    exit 1
fi