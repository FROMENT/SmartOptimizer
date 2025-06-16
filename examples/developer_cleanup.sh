#!/bin/bash
# Developer Cleanup Example - Nettoyage spécialisé développeur

echo "💻 NETTOYAGE DÉVELOPPEUR"
echo "======================="

HOME_DIR="$HOME"
SMARTOPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1. Vérification sécurité
echo "🔒 Vérification sécurité cloud et Git..."
"$SMARTOPT_DIR/scripts/quick_cloud_safety_check.sh"

if [ $? -ne 0 ]; then
    echo "❌ Arrêt pour cause de synchronisation active"
    exit 1
fi

# Vérifier les repos Git non commités
echo "📋 Vérification des repos Git non commités..."
UNCOMMITTED_REPOS=$(find "$HOME_DIR" -name ".git" -type d -exec dirname {} \; 2>/dev/null | while read repo; do
    cd "$repo" 2>/dev/null || continue
    if ! git diff --quiet 2>/dev/null || ! git diff --staged --quiet 2>/dev/null; then
        echo "$repo"
    fi
done)

if [ -n "$UNCOMMITTED_REPOS" ]; then
    echo "⚠️  Repos avec modifications non commitées:"
    echo "$UNCOMMITTED_REPOS"
    echo ""
    read -p "Continuer malgré les modifications non commitées? (y/N): " continue_anyway
    if [[ ! $continue_anyway =~ ^[Yy]$ ]]; then
        echo "❌ Nettoyage annulé - Commitez vos changements d'abord"
        exit 1
    fi
fi

echo ""

# 2. Analyse des projets de développement
echo "📊 Analyse des projets de développement..."
PROJECTS_DIRS=("$HOME_DIR/Projects" "$HOME_DIR/Documents/Projects" "$HOME_DIR/Code" "$HOME_DIR/Dev")

for projects_dir in "${PROJECTS_DIRS[@]}"; do
    if [ -d "$projects_dir" ]; then
        echo "   🔍 Analyse de $projects_dir"
        python3 "$SMARTOPT_DIR/src/analyzers/comprehensive_analyzer.py" "$projects_dir"
        echo ""
    fi
done

# 3. Nettoyage des environnements virtuels volumineux
echo "🐍 Recherche des environnements virtuels volumineux..."
LARGE_VENVS=$(find "$HOME_DIR" -name "venv" -o -name ".venv" -o -name "env" -o -name "virtualenv" | while read venv_dir; do
    if [ -d "$venv_dir" ]; then
        size=$(du -sm "$venv_dir" 2>/dev/null | cut -f1)
        if [ "$size" -gt 500 ]; then  # Plus de 500MB
            echo "$venv_dir ($size MB)"
        fi
    fi
done)

if [ -n "$LARGE_VENVS" ]; then
    echo "📦 Environnements virtuels volumineux trouvés:"
    echo "$LARGE_VENVS"
    echo ""
    read -p "Analyser ces environnements en détail? (Y/n): " analyze_venvs
    if [[ ! $analyze_venvs =~ ^[Nn]$ ]]; then
        echo "$LARGE_VENVS" | while read venv_info; do
            venv_path=$(echo "$venv_info" | cut -d' ' -f1)
            echo "   🔍 Analyse de $venv_path"
            python3 "$SMARTOPT_DIR/src/optimizers/quick_smart_optimizer.py" "$venv_path"
        done
    fi
fi

# 4. Nettoyage des caches de développement
echo ""
echo "🗑️  Nettoyage des caches de développement..."

# Cache Node.js
if [ -d "$HOME_DIR/.npm" ]; then
    npm_size=$(du -sm "$HOME_DIR/.npm" 2>/dev/null | cut -f1)
    echo "   📦 Cache npm: ${npm_size}MB"
    if [ "$npm_size" -gt 1000 ]; then
        read -p "   Nettoyer le cache npm (${npm_size}MB)? (Y/n): " clean_npm
        if [[ ! $clean_npm =~ ^[Nn]$ ]]; then
            npm cache clean --force
            echo "   ✅ Cache npm nettoyé"
        fi
    fi
fi

# Cache Yarn
if [ -d "$HOME_DIR/.yarn/cache" ]; then
    yarn_size=$(du -sm "$HOME_DIR/.yarn/cache" 2>/dev/null | cut -f1)
    echo "   📦 Cache Yarn: ${yarn_size}MB"
    if [ "$yarn_size" -gt 500 ]; then
        read -p "   Nettoyer le cache Yarn (${yarn_size}MB)? (Y/n): " clean_yarn
        if [[ ! $clean_yarn =~ ^[Nn]$ ]]; then
            yarn cache clean
            echo "   ✅ Cache Yarn nettoyé"
        fi
    fi
fi

# Cache Pip
if [ -d "$HOME_DIR/.cache/pip" ]; then
    pip_size=$(du -sm "$HOME_DIR/.cache/pip" 2>/dev/null | cut -f1)
    echo "   🐍 Cache pip: ${pip_size}MB"
    if [ "$pip_size" -gt 500 ]; then
        read -p "   Nettoyer le cache pip (${pip_size}MB)? (Y/n): " clean_pip
        if [[ ! $clean_pip =~ ^[Nn]$ ]]; then
            pip cache purge
            echo "   ✅ Cache pip nettoyé"
        fi
    fi
fi

# Cache Gradle
if [ -d "$HOME_DIR/.gradle/caches" ]; then
    gradle_size=$(du -sm "$HOME_DIR/.gradle/caches" 2>/dev/null | cut -f1)
    echo "   ☕ Cache Gradle: ${gradle_size}MB"
    if [ "$gradle_size" -gt 1000 ]; then
        read -p "   Nettoyer le cache Gradle (${gradle_size}MB)? (Y/n): " clean_gradle
        if [[ ! $clean_gradle =~ ^[Nn]$ ]]; then
            rm -rf "$HOME_DIR/.gradle/caches"
            echo "   ✅ Cache Gradle nettoyé"
        fi
    fi
fi

# 5. Nettoyage des containers Docker inutilisés
echo ""
echo "🐳 Nettoyage Docker..."
if command -v docker >/dev/null 2>&1; then
    # Images non utilisées
    unused_images=$(docker images -f "dangling=true" -q | wc -l | tr -d ' ')
    if [ "$unused_images" -gt 0 ]; then
        echo "   📦 $unused_images images Docker non utilisées"
        read -p "   Nettoyer les images Docker non utilisées? (Y/n): " clean_docker_images
        if [[ ! $clean_docker_images =~ ^[Nn]$ ]]; then
            docker image prune -f
            echo "   ✅ Images Docker nettoyées"
        fi
    fi
    
    # Containers arrêtés
    stopped_containers=$(docker ps -a -f "status=exited" -q | wc -l | tr -d ' ')
    if [ "$stopped_containers" -gt 0 ]; then
        echo "   📦 $stopped_containers containers arrêtés"
        read -p "   Supprimer les containers arrêtés? (Y/n): " clean_docker_containers
        if [[ ! $clean_docker_containers =~ ^[Nn]$ ]]; then
            docker container prune -f
            echo "   ✅ Containers nettoyés"
        fi
    fi
else
    echo "   ℹ️  Docker non installé - Nettoyage ignoré"
fi

# 6. Réorganisation par technologie
echo ""
echo "🗂️  Réorganisation des projets par technologie..."
for projects_dir in "${PROJECTS_DIRS[@]}"; do
    if [ -d "$projects_dir" ]; then
        read -p "Réorganiser $projects_dir par technologie? (Y/n): " reorganize_projects
        if [[ ! $reorganize_projects =~ ^[Nn]$ ]]; then
            python3 "$SMARTOPT_DIR/src/reorganizers/smart_reorganizer.py" "$projects_dir"
        fi
    fi
done

# 7. Résumé final
echo ""
echo "✅ NETTOYAGE DÉVELOPPEUR TERMINÉ"
echo "================================"
echo "📊 Actions effectuées:"
echo "   • Vérification sécurité et Git"
echo "   • Analyse des projets de développement"
echo "   • Nettoyage des environnements virtuels"
echo "   • Nettoyage des caches (npm, pip, etc.)"
echo "   • Nettoyage Docker"
echo "   • Réorganisation par technologie"

echo ""
echo "💡 Recommandations post-nettoyage:"
echo "   • Tester vos projets principaux"
echo "   • Recréer les venvs supprimés si nécessaire"
echo "   • Vérifier que Docker fonctionne correctement"
echo ""
echo "📁 Backups dans: ~/SmartOptimizer_Backups/"