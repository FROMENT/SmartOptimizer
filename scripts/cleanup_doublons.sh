#!/bin/bash
# Script de nettoyage automatique des doublons Google Drive
# Basé sur les patterns identifiés lors de la réorganisation
# ATTENTION: Vérifiez avant d'exécuter!

set -e

DRIVE_PATH="/Users/pascalfroment/Library/CloudStorage/GoogleDrive-pascal.froment@gmail.com/Mon Drive"
LOG_FILE="/Users/pascalfroment/cleanup_doublons.log"

# Fonction de log
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "=== DÉBUT NETTOYAGE DES DOUBLONS ==="

# Sauvegarder les fichiers avant suppression
BACKUP_DIR="/Users/pascalfroment/DOUBLONS_BACKUP_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
log "Dossier de sauvegarde créé: $BACKUP_DIR"

# Fonction pour sauvegarder et supprimer
safe_remove() {
    local file="$1"
    local reason="$2"
    
    if [ -f "$file" ]; then
        # Créer la structure de dossier dans le backup
        local rel_path=$(dirname "${file#$DRIVE_PATH/}")
        mkdir -p "$BACKUP_DIR/$rel_path"
        
        # Copier vers backup
        cp "$file" "$BACKUP_DIR/$rel_path/" 2>/dev/null || true
        
        log "SUPPRESSION: $file ($reason)"
        # Décommenter la ligne suivante pour supprimer réellement
        # rm "$file"
        echo "# rm \"$file\"  # $reason"
    fi
}

# 1. Supprimer les doublons de règlement de copropriété (garder le plus récent)
log "ÉTAPE 1: Nettoyage des règlements de copropriété"

# Les doublons identifiés dans Google AI Studio
safe_remove "$DRIVE_PATH/Google AI Studio/règlement de copropriété.pdf" "Doublon - version consolidée disponible"
safe_remove "$DRIVE_PATH/Google AI Studio/règlement de copropriété (2).pdf" "Doublon - version consolidée disponible"
safe_remove "$DRIVE_PATH/Google AI Studio/règlement de copropriété (3).pdf" "Doublon - version consolidée disponible"

# 2. Supprimer les anciens dossiers vides après réorganisation
log "ÉTAPE 2: Suppression des dossiers vides"

# Fonction pour supprimer les dossiers vides
remove_empty_dirs() {
    local dir="$1"
    if [ -d "$dir" ]; then
        # Compter les fichiers (pas les dossiers cachés)
        local file_count=$(find "$dir" -type f -not -path "*/.*" | wc -l)
        if [ "$file_count" -eq 0 ]; then
            log "DOSSIER VIDE: $dir"
            echo "# rmdir \"$dir\"  # Dossier vide après réorganisation"
        fi
    fi
}

remove_empty_dirs "$DRIVE_PATH/Copropriété 210-212 Sadi-Carnot"
remove_empty_dirs "$DRIVE_PATH/ALL15JUIN2025-210"

# 3. Identifier les fichiers temporaires et de sauvegarde
log "ÉTAPE 3: Nettoyage des fichiers temporaires"

# Chercher les fichiers avec patterns de doublons
find "$DRIVE_PATH" -name "**(1).*" -type f | while read -r file; do
    safe_remove "$file" "Fichier numéroté - probable doublon"
done

find "$DRIVE_PATH" -name "**(2).*" -type f | while read -r file; do
    safe_remove "$file" "Fichier numéroté - probable doublon"
done

find "$DRIVE_PATH" -name "~$*" -type f | while read -r file; do
    safe_remove "$file" "Fichier temporaire Office"
done

# 4. Nettoyer les fichiers de cache et temporaires
log "ÉTAPE 4: Nettoyage des caches"

find "$DRIVE_PATH" -name ".DS_Store" -type f | while read -r file; do
    safe_remove "$file" "Cache système macOS"
done

find "$DRIVE_PATH" -name "Thumbs.db" -type f | while read -r file; do
    safe_remove "$file" "Cache miniatures Windows"
done

# 5. Générer un rapport de nettoyage
RAPPORT="$BACKUP_DIR/RAPPORT_NETTOYAGE_$(date +%Y%m%d).txt"
cat > "$RAPPORT" << EOF
RAPPORT DE NETTOYAGE DES DOUBLONS
Date: $(date)

ACTIONS EFFECTUÉES:
1. Doublons de règlements de copropriété supprimés
2. Dossiers vides identifiés
3. Fichiers temporaires et numérotés nettoyés  
4. Caches système supprimés

SAUVEGARDE:
- Tous les fichiers supprimés sauvegardés dans: $BACKUP_DIR

INSTRUCTIONS:
- Vérifiez le contenu du backup avant de valider
- Décommentez les lignes 'rm' dans ce script pour supprimer réellement
- Testez d'abord sur un petit nombre de fichiers

PROCHAINES ÉTAPES:
- Vérifier que tous les fichiers importants sont dans ADMINISTRATION/
- Supprimer les dossiers sources vides
- Valider la nouvelle organisation
EOF

log "Rapport créé: $RAPPORT"
log "=== FIN NETTOYAGE DES DOUBLONS ==="

echo ""
echo "✅ ANALYSE DE NETTOYAGE TERMINÉE!"
echo "📁 Sauvegarde: $BACKUP_DIR"
echo "📋 Rapport: $RAPPORT"
echo "📝 Log: $LOG_FILE"
echo ""
echo "⚠️  IMPORTANT:"
echo "   - Ce script montre les actions à effectuer (lignes avec #)"
echo "   - Vérifiez le backup avant de décommenter les suppressions"
echo "   - Modifiez le script pour supprimer réellement les fichiers"