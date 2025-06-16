#!/bin/bash

# SmartOptimizer - Installation Automatique Multi-OS
# Support Windows (Git Bash), macOS, Linux

echo "🚀 SmartOptimizer - Installation Automatique"
echo "=============================================="

# Détecter l'OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    PYTHON_CMD="python3"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
    PYTHON_CMD="python3"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="Windows"
    PYTHON_CMD="python"
else
    OS="Unknown"
    PYTHON_CMD="python3"
fi

echo "🖥️  OS détecté: $OS"

# Vérifier Python
echo "🔍 Vérification de Python..."
if command -v $PYTHON_CMD &> /dev/null; then
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
    echo "✅ $PYTHON_VERSION trouvé"
else
    echo "❌ Python non trouvé"
    
    if [[ "$OS" == "macOS" ]]; then
        echo "💡 Pour installer Python sur macOS:"
        echo "   brew install python3"
        echo "   Ou téléchargez depuis python.org"
    elif [[ "$OS" == "Linux" ]]; then
        echo "💡 Pour installer Python sur Linux:"
        echo "   Ubuntu/Debian: sudo apt install python3"
        echo "   Fedora: sudo dnf install python3"
        echo "   Arch: sudo pacman -S python"
    elif [[ "$OS" == "Windows" ]]; then
        echo "💡 Pour installer Python sur Windows:"
        echo "   Téléchargez depuis python.org"
        echo "   Ou utilisez: winget install Python.Python.3"
    fi
    exit 1
fi

# Vérifier que nous sommes dans le bon dossier
if [[ ! -f "smart.py" ]]; then
    echo "❌ Fichier smart.py non trouvé"
    echo "💡 Assurez-vous d'être dans le dossier SmartOptimizer"
    echo "   cd SmartOptimizer"
    exit 1
fi

# Rendre smart.py exécutable (Unix)
if [[ "$OS" != "Windows" ]]; then
    chmod +x smart.py
    echo "✅ Permissions d'exécution configurées"
fi

# Créer la configuration
echo "⚙️  Création de la configuration..."
$PYTHON_CMD smart.py --install

# Test rapide
echo ""
echo "🧪 Test rapide..."
$PYTHON_CMD smart.py --detect

echo ""
echo "🎉 Installation terminée !"
echo ""
echo "📚 Commandes disponibles:"
echo "========================="
echo "📊 Détecter services cloud:     $PYTHON_CMD smart.py --detect"
echo "🏢 Analyser OneDrive Business:  $PYTHON_CMD smart.py --business"
echo "🔍 Vue d'ensemble système:      $PYTHON_CMD smart.py --overview"
echo "📋 Interface menu:              $PYTHON_CMD smart.py"
echo ""
echo "✅ SmartOptimizer est prêt à utiliser !"