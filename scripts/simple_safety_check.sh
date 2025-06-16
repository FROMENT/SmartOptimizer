#!/bin/bash
# Simple Safety Check - Vérification basique avant optimisation

echo "🔒 VÉRIFICATION SÉCURITÉ RAPIDE"
echo "=============================="

# 1. Vérifier les processus cloud actifs
echo "📊 Processus cloud en cours:"
CLOUD_PROCS=$(ps aux | grep -iE "(googledrive|icloud|dropbox|onedrive|sync)" | grep -v grep)

if [ -n "$CLOUD_PROCS" ]; then
    echo "$CLOUD_PROCS" | while read line; do
        echo "  🔄 $(echo $line | awk '{print $11}')"
    done
    echo ""
    echo "🟡 ATTENTION: Processus cloud détectés"
    echo "   → Vérifiez manuellement l'état de sync"
else
    echo "  ✅ Aucun processus cloud actif détecté"
fi

# 2. Vérifier l'existence des dossiers cloud
echo ""
echo "📁 Services cloud détectés:"

GDRIVE="/Users/pascalfroment/Library/CloudStorage/GoogleDrive-pascal.froment@gmail.com"
ICLOUD="/Users/pascalfroment/Library/Mobile Documents/com~apple~CloudDocs"
DROPBOX="/Users/pascalfroment/Dropbox"

if [ -d "$GDRIVE" ]; then
    echo "  📂 Google Drive présent"
fi

if [ -d "$ICLOUD" ]; then
    echo "  ☁️  iCloud Drive présent"
fi

if [ -d "$DROPBOX" ]; then
    echo "  📦 Dropbox présent"
fi

# 3. Vérifications simples
echo ""
echo "⚡ VÉRIFICATIONS RAPIDES:"

# Vérifier si des fichiers sont en cours de téléchargement
DOWNLOADING=$(lsof 2>/dev/null | grep -i "download\|sync\|cloud" | wc -l)
if [ "$DOWNLOADING" -gt 0 ]; then
    echo "  🔄 $DOWNLOADING processus d'écriture actifs (possibles téléchargements)"
else
    echo "  ✅ Pas de téléchargements détectés"
fi

# Vérifier l'activité réseau récente
NETWORK_CONN=$(netstat -an 2>/dev/null | grep -i "established" | wc -l)
echo "  🌐 $NETWORK_CONN connexions réseau actives"

echo ""
echo "🎯 RECOMMANDATIONS DE SÉCURITÉ:"
echo "==============================="
echo "✅ TOUJOURS FAIRE avant optimisation:"
echo "   1. 💾 Créer une Time Machine"
echo "   2. ⏳ Attendre 5 minutes après toute activité cloud"
echo "   3. 📱 Vérifier sync terminée sur vos appareils"
echo "   4. 🔒 Faire des sauvegardes supplémentaires des dossiers critiques"
echo ""
echo "🚨 NOS SCRIPTS INCLUENT DES SAUVEGARDES AUTOMATIQUES:"
echo "   • Mode simulation par défaut (# rm commenté)"
echo "   • BACKUP_DIR automatique avant toute suppression"
echo "   • Vérifications multiples avant actions"
echo ""
echo "⚠️  EN CAS DE DOUTE: Reporter l'optimisation"

echo ""
echo "🕒 $(date '+%Y-%m-%d %H:%M:%S')"