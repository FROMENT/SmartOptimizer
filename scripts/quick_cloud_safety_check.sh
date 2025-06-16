#!/bin/bash
# Quick Cloud Safety Check - Vérification rapide avant optimisation

echo "🔒 VÉRIFICATION RAPIDE SÉCURITÉ CLOUD"
echo "===================================="

SAFE_TO_PROCEED=true
WARNINGS=()

# 1. Vérifier Google Drive
GDRIVE_PATH="/Users/pascalfroment/Library/CloudStorage/GoogleDrive-pascal.froment@gmail.com"
if [ -d "$GDRIVE_PATH" ]; then
    echo "📁 Google Drive détecté: $GDRIVE_PATH"
    
    # Vérifier les fichiers temporaires de sync
    TEMP_FILES=$(find "$GDRIVE_PATH" -name "*.tmp" -o -name "*.gdownload" 2>/dev/null | wc -l)
    if [ "$TEMP_FILES" -gt 0 ]; then
        echo "  🔴 $TEMP_FILES fichiers de sync temporaires détectés"
        SAFE_TO_PROCEED=false
    else
        echo "  ✅ Pas de sync active détectée"
    fi
    
    # Vérifier les modifications récentes (dernières 5 minutes)
    RECENT_FILES=$(find "$GDRIVE_PATH" -type f -mtime -5m 2>/dev/null | wc -l)
    if [ "$RECENT_FILES" -gt 5 ]; then
        echo "  🟡 $RECENT_FILES fichiers modifiés récemment"
        WARNINGS+=("Google Drive: modifications récentes")
    fi
else
    echo "✅ Google Drive non détecté"
fi

# 2. Vérifier iCloud Drive
ICLOUD_PATH="/Users/pascalfroment/Library/Mobile Documents/com~apple~CloudDocs"
if [ -d "$ICLOUD_PATH" ]; then
    echo "📁 iCloud Drive détecté: $ICLOUD_PATH"
    
    # Vérifier les fichiers .icloud (non téléchargés)
    ICLOUD_FILES=$(find "$ICLOUD_PATH" -name "*.icloud" 2>/dev/null | wc -l)
    if [ "$ICLOUD_FILES" -gt 0 ]; then
        echo "  🔴 $ICLOUD_FILES fichiers .icloud (téléchargement en cours)"
        SAFE_TO_PROCEED=false
    else
        echo "  ✅ Tous les fichiers iCloud téléchargés"
    fi
else
    echo "✅ iCloud Drive non détecté"
fi

# 3. Vérifier Dropbox
DROPBOX_PATH="/Users/pascalfroment/Dropbox"
if [ -d "$DROPBOX_PATH" ]; then
    echo "📁 Dropbox détecté: $DROPBOX_PATH"
    
    # Vérifier le statut Dropbox si disponible
    if command -v dropbox >/dev/null 2>&1; then
        STATUS=$(dropbox status 2>/dev/null)
        if echo "$STATUS" | grep -q "Syncing\|Downloading\|Uploading"; then
            echo "  🔴 Dropbox en cours de synchronisation"
            SAFE_TO_PROCEED=false
        else
            echo "  ✅ Dropbox synchronisé"
        fi
    else
        echo "  ⚠️  Impossible de vérifier le statut Dropbox"
    fi
else
    echo "✅ Dropbox non détecté"
fi

# 4. Vérifications générales
echo ""
echo "🔍 VÉRIFICATIONS GÉNÉRALES:"

# Vérifier les processus de sync actifs
SYNC_PROCESSES=$(ps aux | grep -E "(Google Drive|iCloud|Dropbox|OneDrive)" | grep -v grep | wc -l)
if [ "$SYNC_PROCESSES" -gt 0 ]; then
    echo "  📊 $SYNC_PROCESSES processus de sync cloud actifs"
    ps aux | grep -E "(Google Drive|iCloud|Dropbox|OneDrive)" | grep -v grep | awk '{print "     •", $11, $12, $13}'
fi

# Vérifier l'activité réseau (approximatif)
if command -v nettop >/dev/null 2>&1; then
    NETWORK_ACTIVITY=$(nettop -l 1 -t external 2>/dev/null | grep -E "(Google|iCloud|Dropbox|OneDrive)" | wc -l)
    if [ "$NETWORK_ACTIVITY" -gt 0 ]; then
        echo "  🌐 Activité réseau cloud détectée"
        WARNINGS+=("Activité réseau cloud en cours")
    fi
fi

# 5. Verdict final
echo ""
echo "🎯 VERDICT FINAL:"
echo "================"

if [ "$SAFE_TO_PROCEED" = true ]; then
    if [ ${#WARNINGS[@]} -eq 0 ]; then
        echo "✅ FEUX VERTS - Optimisation sûre"
        echo "   Aucune synchronisation active détectée"
    else
        echo "🟡 PRUDENCE RECOMMANDÉE - Optimisation possible avec précautions"
        echo "   Avertissements:"
        for warning in "${WARNINGS[@]}"; do
            echo "   • $warning"
        done
        echo ""
        echo "   💡 Recommandations:"
        echo "   • Faire une sauvegarde supplémentaire"
        echo "   • Surveiller les notifications cloud pendant l'optimisation"
    fi
else
    echo "🔴 ARRÊT RECOMMANDÉ - Synchronisations actives détectées"
    echo "   ⏳ Attendre la fin des synchronisations avant optimisation"
    echo "   📱 Vérifier les notifications cloud sur vos appareils"
fi

echo ""
echo "⚡ ACTIONS DE SÉCURITÉ SUPPLÉMENTAIRES:"
echo "• Créer une Time Machine avant optimisation"
echo "• Vérifier que tous vos appareils sont connectés"
echo "• Attendre 5-10 minutes après la fin des sync"

echo ""
echo "🕒 Vérification effectuée le $(date '+%Y-%m-%d à %H:%M:%S')"

# Code de sortie
if [ "$SAFE_TO_PROCEED" = true ]; then
    exit 0
else
    exit 1
fi