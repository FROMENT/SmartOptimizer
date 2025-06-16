#!/bin/bash
# Cloud Optimization Workflow - Optimisation complète de tous les services cloud

echo "☁️  OPTIMISATION COMPLÈTE DES SERVICES CLOUD"
echo "============================================"

HOME_DIR="$HOME"
SMARTOPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 1. Détection de tous les services cloud
echo "🔍 Étape 1: Détection des services cloud..."
python3 "$SMARTOPT_DIR/src/analyzers/cloud_services_detector.py" "$HOME_DIR"

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de la détection des services cloud"
    exit 1
fi

echo ""

# 2. Vérification sécurité cloud obligatoire
echo "🔒 Étape 2: Vérification sécurité cloud (OBLIGATOIRE)..."
"$SMARTOPT_DIR/scripts/quick_cloud_safety_check.sh"

if [ $? -ne 0 ]; then
    echo "❌ Vérification sécurité échouée - ARRÊT"
    echo "   Attendez la fin des synchronisations avant d'optimiser"
    exit 1
fi

echo "✅ Sécurité cloud validée - Optimisation peut procéder"
echo ""

# 3. Optimisation par service cloud détecté
echo "⚡ Étape 3: Optimisation des services cloud détectés..."

# iCloud Drive
ICLOUD_PATH="$HOME_DIR/Library/Mobile Documents/com~apple~CloudDocs"
if [ -d "$ICLOUD_PATH" ]; then
    echo ""
    echo "🍎 Optimisation iCloud Drive..."
    read -p "Optimiser iCloud Drive? (Y/n): " optimize_icloud
    if [[ ! $optimize_icloud =~ ^[Nn]$ ]]; then
        python3 "$SMARTOPT_DIR/src/optimizers/cloud_optimizer.py" "$ICLOUD_PATH"
    fi
fi

# Google Drive (détecter dynamiquement)
GOOGLE_DRIVE_PATHS=(
    "$HOME_DIR/Library/CloudStorage/GoogleDrive-"*
    "$HOME_DIR/Google Drive"
    "$HOME_DIR/GoogleDrive"
)

for gdrive_pattern in "${GOOGLE_DRIVE_PATHS[@]}"; do
    for gdrive_path in $gdrive_pattern; do
        if [ -d "$gdrive_path" ]; then
            echo ""
            echo "📊 Optimisation Google Drive..."
            echo "   Chemin: $gdrive_path"
            read -p "Optimiser ce Google Drive? (Y/n): " optimize_gdrive
            if [[ ! $optimize_gdrive =~ ^[Nn]$ ]]; then
                python3 "$SMARTOPT_DIR/src/optimizers/cloud_optimizer.py" "$gdrive_path"
            fi
            break
        fi
    done
done

# OneDrive (détecter dynamiquement)
ONEDRIVE_PATHS=(
    "$HOME_DIR/Library/CloudStorage/OneDrive-"*
    "$HOME_DIR/OneDrive"*
)

for onedrive_pattern in "${ONEDRIVE_PATHS[@]}"; do
    for onedrive_path in $onedrive_pattern; do
        if [ -d "$onedrive_path" ]; then
            echo ""
            echo "💼 Optimisation OneDrive..."
            echo "   Chemin: $onedrive_path"
            read -p "Optimiser ce OneDrive? (Y/n): " optimize_onedrive
            if [[ ! $optimize_onedrive =~ ^[Nn]$ ]]; then
                python3 "$SMARTOPT_DIR/src/optimizers/cloud_optimizer.py" "$onedrive_path"
            fi
            break
        fi
    done
done

# Dropbox
DROPBOX_PATHS=(
    "$HOME_DIR/Dropbox"
    "$HOME_DIR/Dropbox (Personal)"
    "$HOME_DIR/Dropbox (Business)"
)

for dropbox_path in "${DROPBOX_PATHS[@]}"; do
    if [ -d "$dropbox_path" ]; then
        echo ""
        echo "📦 Optimisation Dropbox..."
        echo "   Chemin: $dropbox_path"
        read -p "Optimiser ce Dropbox? (Y/n): " optimize_dropbox
        if [[ ! $optimize_dropbox =~ ^[Nn]$ ]]; then
            python3 "$SMARTOPT_DIR/src/optimizers/cloud_optimizer.py" "$dropbox_path"
        fi
        break
    fi
done

# Box
BOX_PATHS=(
    "$HOME_DIR/Box"
    "$HOME_DIR/Box Sync"
)

for box_path in "${BOX_PATHS[@]}"; do
    if [ -d "$box_path" ]; then
        echo ""
        echo "📋 Optimisation Box..."
        echo "   Chemin: $box_path"
        read -p "Optimiser ce Box? (Y/n): " optimize_box
        if [[ ! $optimize_box =~ ^[Nn]$ ]]; then
            python3 "$SMARTOPT_DIR/src/optimizers/cloud_optimizer.py" "$box_path"
        fi
        break
    fi
done

# 4. Optimisation globale des doublons inter-cloud
echo ""
echo "🔄 Étape 4: Détection de doublons entre services cloud..."
read -p "Rechercher les doublons entre tous les services cloud? (Y/n): " find_cross_duplicates
if [[ ! $find_cross_duplicates =~ ^[Nn]$ ]]; then
    echo "   🔍 Analyse des doublons inter-cloud en cours..."
    
    # Créer une liste de tous les chemins cloud
    CLOUD_PATHS_FILE="/tmp/smartopt_cloud_paths.txt"
    > "$CLOUD_PATHS_FILE"
    
    # Ajouter tous les chemins cloud détectés
    for cloud_path in "$ICLOUD_PATH" $GOOGLE_DRIVE_PATHS $ONEDRIVE_PATHS "${DROPBOX_PATHS[@]}" "${BOX_PATHS[@]}"; do
        if [ -d "$cloud_path" ]; then
            echo "$cloud_path" >> "$CLOUD_PATHS_FILE"
        fi
    done
    
    # Exécuter la détection de doublons multi-répertoires
    if [ -s "$CLOUD_PATHS_FILE" ]; then
        echo "   📊 Comparaison entre $(wc -l < "$CLOUD_PATHS_FILE") services cloud..."
        python3 "$SMARTOPT_DIR/src/optimizers/quick_smart_optimizer.py" --multi-directory "$CLOUD_PATHS_FILE"
    fi
    
    rm -f "$CLOUD_PATHS_FILE"
fi

# 5. Vérification finale et recommandations
echo ""
echo "🎯 Étape 5: Vérification finale et recommandations..."

# Recalculer l'utilisation après optimisation
echo "📊 Recalcul de l'utilisation des services cloud..."
python3 "$SMARTOPT_DIR/src/analyzers/cloud_services_detector.py" "$HOME_DIR"

# Recommandations spécifiques par service
echo ""
echo "💡 RECOMMANDATIONS POST-OPTIMISATION:"
echo "====================================="

echo ""
echo "🍎 iCloud Drive:"
echo "   • Activez 'Optimiser le stockage Mac' dans Préférences Système > Apple ID"
echo "   • Utilisez iCloud Photos pour optimiser l'espace photo"
echo "   • Déplacez les gros fichiers vers 'Stocké dans iCloud uniquement'"

echo ""
echo "📊 Google Drive:"
echo "   • Passez en mode 'Streaming' au lieu de 'Miroir' dans l'app Google Drive"
echo "   • Convertissez les documents Office en Google Docs/Sheets pour économiser l'espace"
echo "   • Utilisez Google Photos pour les images (stockage séparé)"

echo ""
echo "💼 OneDrive:"
echo "   • Activez 'Fichiers à la demande' dans les paramètres OneDrive"
echo "   • Utilisez OneDrive Personal Vault pour les documents sensibles"
echo "   • Synchronisez seulement les dossiers nécessaires"

echo ""
echo "📦 Dropbox:"
echo "   • Activez 'Smart Sync' pour les dossiers volumineux"
echo "   • Utilisez Dropbox Paper au lieu de fichiers Word/PDF quand possible"
echo "   • Archivez les anciens projets avec Dropbox Archive"

# 6. Configuration de la surveillance continue
echo ""
echo "⚙️  Étape 6: Configuration de la surveillance (optionnel)..."
read -p "Configurer une surveillance mensuelle automatique? (y/N): " setup_monitoring
if [[ $setup_monitoring =~ ^[Yy]$ ]]; then
    
    # Créer un script de surveillance
    MONITORING_SCRIPT="$HOME_DIR/.smartoptimizer_cloud_monitor.sh"
    
    cat > "$MONITORING_SCRIPT" << 'EOF'
#!/bin/bash
# SmartOptimizer Cloud Monitoring - Surveillance automatique
SMARTOPT_DIR="$(dirname "$(realpath "$0")")/SmartOptimizer"

echo "🤖 SmartOptimizer - Surveillance automatique cloud"
echo "=================================================="
echo "Date: $(date)"

# Vérifier la sécurité cloud
"$SMARTOPT_DIR/scripts/quick_cloud_safety_check.sh" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Services cloud stables"
    
    # Analyser les changements
    echo "📊 Analyse des changements depuis la dernière vérification..."
    python3 "$SMARTOPT_DIR/src/analyzers/cloud_services_detector.py" "$HOME" > "/tmp/smartopt_cloud_report_$(date +%Y%m%d).txt"
    
    echo "📄 Rapport sauvegardé: /tmp/smartopt_cloud_report_$(date +%Y%m%d).txt"
else
    echo "⚠️  Synchronisations cloud actives - Surveillance reportée"
fi

echo "Prochaine vérification: $(date -d '+1 month')"
EOF

    chmod +x "$MONITORING_SCRIPT"
    
    echo "   📅 Script de surveillance créé: $MONITORING_SCRIPT"
    echo "   ⏰ Pour automatiser: ajouter à crontab avec 'crontab -e':"
    echo "      0 9 1 * * $MONITORING_SCRIPT"
fi

# 7. Résumé final
echo ""
echo "✅ OPTIMISATION CLOUD TERMINÉE"
echo "=============================="
echo "📊 Actions effectuées:"
echo "   • Détection de tous les services cloud"
echo "   • Vérification sécurité obligatoire"
echo "   • Optimisation spécifique par service"
echo "   • Détection de doublons inter-cloud"
echo "   • Recommandations personnalisées"

echo ""
echo "💾 Sauvegardes dans:"
echo "   ~/SmartOptimizer_Backups/cloud_optimization/"

echo ""
echo "📱 Prochaines étapes recommandées:"
echo "   1. Vérifiez les optimisations sur vos autres appareils"
echo "   2. Configurez les paramètres cloud selon les recommandations"
echo "   3. Surveillez l'espace libéré dans les prochains jours"
echo "   4. Réexécutez ce script mensuel pour maintenance"

echo ""
echo "🎉 Vos services cloud sont maintenant optimisés!"