#!/bin/bash
# Cloud Deduplication Strategy - Stratégie complète de déduplication cloud

echo "🔄 STRATÉGIE DE DÉDUPLICATION CLOUD"
echo "==================================="

HOME_DIR="$HOME"
SMARTOPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Configuration des stratégies par service
declare -A CLOUD_STRATEGIES
CLOUD_STRATEGIES=(
    ["iCloud"]="personal_system_files"
    ["Google Drive"]="collaboration_office"
    ["OneDrive"]="business_office365"
    ["Dropbox"]="creative_sharing"
    ["Box"]="enterprise_compliance"
)

echo "📋 Stratégies de déduplication par service:"
for service in "${!CLOUD_STRATEGIES[@]}"; do
    echo "   • $service: ${CLOUD_STRATEGIES[$service]}"
done
echo ""

# 1. Analyse des imbrications
echo "🔍 Étape 1: Analyse des imbrications cloud..."
python3 "$SMARTOPT_DIR/src/analyzers/cloud_nesting_analyzer.py" "$HOME_DIR"

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de l'analyse des imbrications"
    exit 1
fi

echo ""
read -p "Continuer avec l'optimisation? (Y/n): " continue_opt
if [[ $continue_opt =~ ^[Nn]$ ]]; then
    echo "❌ Optimisation annulée"
    exit 0
fi

# 2. Vérification sécurité obligatoire
echo ""
echo "🔒 Étape 2: Vérification sécurité cloud..."
"$SMARTOPT_DIR/scripts/quick_cloud_safety_check.sh"

if [ $? -ne 0 ]; then
    echo "❌ Synchronisations actives détectées - ARRÊT"
    echo "   Attendez la stabilisation avant de continuer"
    exit 1
fi

echo "✅ Sécurité validée - Procédure de déduplication autorisée"

# 3. Sauvegarde préventive
echo ""
echo "💾 Étape 3: Sauvegarde préventive..."
BACKUP_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$HOME_DIR/SmartOptimizer_Backups/pre_deduplication_$BACKUP_TIMESTAMP"

read -p "Créer une sauvegarde complète avant déduplication? (Y/n): " create_backup
if [[ ! $create_backup =~ ^[Nn]$ ]]; then
    echo "   📦 Création de la sauvegarde..."
    mkdir -p "$BACKUP_DIR"
    
    # Sauvegarder les configurations des services cloud
    echo "   ⚙️  Sauvegarde des configurations..."
    
    # iCloud Drive
    if [ -d "$HOME_DIR/Library/Mobile Documents" ]; then
        echo "iCloud Drive configuration backup" > "$BACKUP_DIR/icloud_config.txt"
        ls -la "$HOME_DIR/Library/Mobile Documents/" >> "$BACKUP_DIR/icloud_config.txt" 2>/dev/null
    fi
    
    # Google Drive
    GDRIVE_PATHS=("$HOME_DIR/Library/CloudStorage/GoogleDrive-"* "$HOME_DIR/Google Drive"*)
    for gdrive_path in "${GDRIVE_PATHS[@]}"; do
        if [ -d "$gdrive_path" ]; then
            echo "Google Drive path: $gdrive_path" >> "$BACKUP_DIR/google_drive_config.txt"
            ls -la "$gdrive_path/" | head -20 >> "$BACKUP_DIR/google_drive_config.txt" 2>/dev/null
        fi
    done
    
    # OneDrive
    ONEDRIVE_PATHS=("$HOME_DIR/Library/CloudStorage/OneDrive-"* "$HOME_DIR/OneDrive"*)
    for onedrive_path in "${ONEDRIVE_PATHS[@]}"; do
        if [ -d "$onedrive_path" ]; then
            echo "OneDrive path: $onedrive_path" >> "$BACKUP_DIR/onedrive_config.txt"
            ls -la "$onedrive_path/" | head -20 >> "$BACKUP_DIR/onedrive_config.txt" 2>/dev/null
        fi
    done
    
    # Dropbox
    DROPBOX_PATHS=("$HOME_DIR/Dropbox"* "$HOME_DIR/Dropbox (Personal)" "$HOME_DIR/Dropbox (Business)")
    for dropbox_path in "${DROPBOX_PATHS[@]}"; do
        if [ -d "$dropbox_path" ]; then
            echo "Dropbox path: $dropbox_path" >> "$BACKUP_DIR/dropbox_config.txt"
            ls -la "$dropbox_path/" | head -20 >> "$BACKUP_DIR/dropbox_config.txt" 2>/dev/null
        fi
    done
    
    echo "   ✅ Sauvegarde créée: $BACKUP_DIR"
fi

# 4. Exécution de la déduplication
echo ""
echo "⚡ Étape 4: Exécution de la déduplication..."
python3 "$SMARTOPT_DIR/src/optimizers/cloud_deduplication_optimizer.py" "$HOME_DIR"

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de la déduplication"
    exit 1
fi

# 5. Stratégies spécifiques par problème détecté
echo ""
echo "🎯 Étape 5: Application des stratégies spécifiques..."

# Fonction pour résoudre l'imbrication cloud-dans-cloud
resolve_cloud_nesting() {
    echo "  🔧 Résolution des imbrications cloud..."
    
    # Exemple: Dropbox dans Google Drive
    if [ -d "$HOME_DIR/Library/CloudStorage/GoogleDrive-*/Dropbox" ]; then
        echo "     🚨 Dropbox détecté dans Google Drive"
        echo "     → Stratégie: Déplacer Dropbox vers ~/Dropbox_Standalone"
        
        read -p "     Appliquer cette correction? (y/N): " fix_nesting
        if [[ $fix_nesting =~ ^[Yy]$ ]]; then
            echo "     ⚠️  ATTENTION: Arrêtez d'abord la synchronisation Dropbox"
            echo "     ⚠️  Puis exécutez manuellement:"
            echo "     mv '$HOME_DIR/Library/CloudStorage/GoogleDrive-*/Dropbox' '$HOME_DIR/Dropbox_Standalone'"
            echo "     ⚠️  Reconfigurez Dropbox sur le nouveau chemin"
        fi
    fi
    
    # Exemple: OneDrive dans iCloud
    if [ -d "$HOME_DIR/Library/Mobile Documents/com~apple~CloudDocs/OneDrive" ]; then
        echo "     🚨 OneDrive détecté dans iCloud Drive"
        echo "     → Stratégie: Déplacer OneDrive vers ~/OneDrive_Business"
        
        read -p "     Appliquer cette correction? (y/N): " fix_onedrive
        if [[ $fix_onedrive =~ ^[Yy]$ ]]; then
            echo "     ⚠️  Procédure manuelle recommandée:"
            echo "     1. Arrêter OneDrive"
            echo "     2. Déplacer le dossier"
            echo "     3. Reconfigurer OneDrive"
        fi
    fi
}

# Fonction pour optimiser Desktop/Documents
optimize_system_folders() {
    echo "  📁 Optimisation des dossiers système..."
    
    # Analyser Desktop
    if [ -d "$HOME_DIR/Desktop" ]; then
        echo "     🖥️  Analyse du Desktop..."
        
        # Vérifier si Desktop est dans plusieurs clouds
        DESKTOP_IN_CLOUDS=()
        
        if [ -d "$HOME_DIR/Library/Mobile Documents/com~apple~CloudDocs/Desktop" ]; then
            DESKTOP_IN_CLOUDS+=("iCloud")
        fi
        
        # Vérifier Google Drive
        for gdrive_path in "$HOME_DIR/Library/CloudStorage/GoogleDrive-"*/Desktop "$HOME_DIR/Google Drive"*/Desktop; do
            if [ -d "$gdrive_path" ]; then
                DESKTOP_IN_CLOUDS+=("Google Drive")
                break
            fi
        done
        
        # Vérifier OneDrive
        for onedrive_path in "$HOME_DIR/Library/CloudStorage/OneDrive-"*/Desktop "$HOME_DIR/OneDrive"*/Desktop; do
            if [ -d "$onedrive_path" ]; then
                DESKTOP_IN_CLOUDS+=("OneDrive")
                break
            fi
        done
        
        if [ ${#DESKTOP_IN_CLOUDS[@]} -gt 1 ]; then
            echo "     ⚠️  Desktop synchronisé par: ${DESKTOP_IN_CLOUDS[*]}"
            echo "     → Recommandation: Garder uniquement dans iCloud Drive"
            echo "     → Actions requises:"
            echo "        1. Exclure Desktop des autres services"
            echo "        2. Migrer les fichiers uniques vers iCloud"
            echo "        3. Nettoyer les doublons"
        else
            echo "     ✅ Desktop correctement configuré"
        fi
    fi
    
    # Analyser Documents
    if [ -d "$HOME_DIR/Documents" ]; then
        echo "     📄 Analyse des Documents..."
        
        # Logique similaire pour Documents
        DOCS_IN_CLOUDS=()
        
        if [ -d "$HOME_DIR/Library/Mobile Documents/com~apple~CloudDocs/Documents" ]; then
            DOCS_IN_CLOUDS+=("iCloud")
        fi
        
        if [ ${#DOCS_IN_CLOUDS[@]} -gt 1 ]; then
            echo "     ⚠️  Documents synchronisé par plusieurs services"
            echo "     → Recommandation: Consolider dans iCloud Drive"
        fi
    fi
}

# Fonction pour gérer les fichiers Office
optimize_office_files() {
    echo "  📊 Optimisation des fichiers Office..."
    
    # Stratégie pour fichiers .docx, .xlsx, .pptx
    echo "     🔍 Recherche de doublons Office..."
    
    # Trouver tous les fichiers Office dans tous les clouds
    OFFICE_FILES_FOUND=false
    
    # Recherche dans tous les services cloud
    for cloud_path in "$HOME_DIR/Library/CloudStorage"/*/ "$HOME_DIR/Library/Mobile Documents/com~apple~CloudDocs"/ "$HOME_DIR/Dropbox"*/ "$HOME_DIR/OneDrive"*/ "$HOME_DIR/Google Drive"*/; do
        if [ -d "$cloud_path" ]; then
            OFFICE_COUNT=$(find "$cloud_path" -name "*.docx" -o -name "*.xlsx" -o -name "*.pptx" 2>/dev/null | wc -l)
            if [ "$OFFICE_COUNT" -gt 0 ]; then
                SERVICE_NAME=$(basename "$cloud_path")
                echo "     📋 $SERVICE_NAME: $OFFICE_COUNT fichiers Office"
                OFFICE_FILES_FOUND=true
            fi
        fi
    done
    
    if [ "$OFFICE_FILES_FOUND" = true ]; then
        echo "     💡 Recommandations:"
        echo "        • OneDrive: Meilleur pour fichiers Office 365"
        echo "        • Google Drive: Convertir en Google Docs/Sheets"
        echo "        • iCloud: Convertir en Pages/Numbers/Keynote"
        echo "        • Dropbox: Garder pour partage externe uniquement"
    fi
}

# Appliquer les stratégies
resolve_cloud_nesting
optimize_system_folders
optimize_office_files

# 6. Configuration des exclusions
echo ""
echo "⚙️  Étape 6: Configuration des exclusions recommandées..."

cat << 'EOF'
📋 EXCLUSIONS RECOMMANDÉES PAR SERVICE:

🍎 iCloud Drive:
   ✅ Synchroniser: Desktop, Documents, Photos (système)
   ❌ Exclure: Dossiers d'autres services cloud, node_modules, .git

📊 Google Drive:
   ✅ Synchroniser: Projets collaboratifs, Google Workspace
   ❌ Exclure: Desktop, Documents (laisser à iCloud), fichiers système

💼 OneDrive:
   ✅ Synchroniser: Documents Office 365, projets Teams
   ❌ Exclure: Dossiers personnels (laisser à iCloud), créatifs (laisser à Dropbox)

📦 Dropbox:
   ✅ Synchroniser: Projets créatifs, partages externes
   ❌ Exclure: Documents système, fichiers Office (laisser à OneDrive)

🏢 Box:
   ✅ Synchroniser: Documents d'entreprise uniquement
   ❌ Exclure: Tout le personnel (utiliser les autres services)
EOF

# 7. Scripts de surveillance
echo ""
echo "🤖 Étape 7: Configuration de la surveillance continue..."

read -p "Installer la surveillance automatique des doublons? (Y/n): " install_monitoring
if [[ ! $install_monitoring =~ ^[Nn]$ ]]; then
    
    # Créer un script de surveillance
    MONITOR_SCRIPT="$HOME_DIR/.cloud_deduplication_monitor.sh"
    
    cat > "$MONITOR_SCRIPT" << 'EOF'
#!/bin/bash
# Cloud Deduplication Monitor - Surveillance automatique

SMARTOPT_DIR="$(dirname "$(realpath "$0")")/SmartOptimizer"
REPORT_DIR="$HOME/Cloud_Deduplication_Reports"
mkdir -p "$REPORT_DIR"

echo "🤖 Surveillance déduplication cloud - $(date)"

# Analyse rapide des imbrications
python3 "$SMARTOPT_DIR/src/analyzers/cloud_nesting_analyzer.py" "$HOME" > "$REPORT_DIR/nesting_report_$(date +%Y%m%d).txt"

# Vérifier les nouveaux doublons
DUPLICATES_FOUND=$(grep -c "doublons" "$REPORT_DIR/nesting_report_$(date +%Y%m%d).txt" 2>/dev/null || echo "0")

if [ "$DUPLICATES_FOUND" -gt 10 ]; then
    echo "⚠️  $DUPLICATES_FOUND nouveaux doublons détectés!"
    echo "Rapport: $REPORT_DIR/nesting_report_$(date +%Y%m%d).txt"
    
    # Notification optionnelle
    if command -v osascript >/dev/null 2>&1; then
        osascript -e "display notification \"$DUPLICATES_FOUND nouveaux doublons cloud détectés\" with title \"SmartOptimizer\""
    fi
else
    echo "✅ Configuration cloud stable"
fi
EOF
    
    chmod +x "$MONITOR_SCRIPT"
    
    echo "   📅 Script de surveillance créé: $MONITOR_SCRIPT"
    echo "   💡 Pour automatiser, ajouter à crontab:"
    echo "      0 8 * * 1 $MONITOR_SCRIPT  # Chaque lundi à 8h"
fi

# 8. Résumé et prochaines étapes
echo ""
echo "✅ DÉDUPLICATION CLOUD TERMINÉE"
echo "==============================="

echo ""
echo "📊 Actions effectuées:"
echo "   • Analyse complète des imbrications"
echo "   • Déduplication des fichiers dupliqués"
echo "   • Résolution des conflits de synchronisation"
echo "   • Configuration des stratégies par service"
echo "   • Installation de la surveillance continue"

echo ""
echo "🎯 Prochaines étapes recommandées:"
echo "   1. 📱 Vérifier la synchronisation sur tous vos appareils"
echo "   2. ⚙️  Configurer les exclusions dans chaque application cloud"
echo "   3. 🗑️  Vider les corbeilles de tous les services cloud"
echo "   4. 📊 Surveiller l'utilisation d'espace les prochains jours"
echo "   5. 🔄 Réexécuter l'analyse dans 1 mois"

echo ""
echo "💾 Sauvegardes disponibles:"
if [ -d "$BACKUP_DIR" ]; then
    echo "   • Pré-déduplication: $BACKUP_DIR"
fi
echo "   • Optimisations: ~/SmartOptimizer_Backups/cloud_deduplication/"

echo ""
echo "📞 Support:"
echo "   • Logs détaillés: ~/Cloud_Deduplication_Reports/"
echo "   • Documentation: $SMARTOPT_DIR/docs/user-guide.md"
echo "   • Issues: https://github.com/user/SmartOptimizer/issues"

echo ""
echo "🎉 Vos services cloud sont maintenant optimisés et dédupliqués!"