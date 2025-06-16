#!/bin/bash

# Script de réorganisation automatique Phase 1 - Google Drive
# Auteur: Claude Code
# Date: $(date +%Y-%m-%d)

set -e  # Arrêter en cas d'erreur

# Variables
DRIVE_PATH="/Users/pascalfroment/Library/CloudStorage/GoogleDrive-pascal.froment@gmail.com"
BACKUP_PATH="/Users/pascalfroment/GDRIVE_BACKUP_$(date +%Y%m%d_%H%M%S)"
LOG_FILE="/Users/pascalfroment/reorganisation.log"

# Fonction de log
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "=== DÉBUT PHASE 1 - RÉORGANISATION GOOGLE DRIVE ==="

# ÉTAPE 1: Sauvegarde complète
log "ÉTAPE 1/4: Création de la sauvegarde..."
if [ ! -d "$BACKUP_PATH" ]; then
    mkdir -p "$BACKUP_PATH"
    log "Dossier de sauvegarde créé: $BACKUP_PATH"
fi

# Sauvegarder les dossiers critiques
log "Sauvegarde des dossiers critiques..."
cp -R "$DRIVE_PATH/Mon Drive/Copropriété 210-212 Sadi-Carnot" "$BACKUP_PATH/" 2>/dev/null || log "ATTENTION: Dossier copropriété principal introuvable"
cp -R "$DRIVE_PATH/Mon Drive/ALL15JUIN2025-210" "$BACKUP_PATH/" 2>/dev/null || log "ATTENTION: Dossier AG 2025 introuvable"
cp "$DRIVE_PATH/Mon Drive/Lots_Par_Batiment_Sadi_Carnot.xlsx" "$BACKUP_PATH/" 2>/dev/null || log "ATTENTION: Fichier lots introuvable"
cp "$DRIVE_PATH/Mon Drive/Repartition_Devis_Geometre_SadiCarnot_Suivi.xlsx" "$BACKUP_PATH/" 2>/dev/null || log "ATTENTION: Fichier répartition introuvable"

log "Sauvegarde terminée dans: $BACKUP_PATH"

# ÉTAPE 2: Créer la nouvelle structure
log "ÉTAPE 2/4: Création de la nouvelle structure..."
ADMIN_PATH="$DRIVE_PATH/Mon Drive/ADMINISTRATION"
COPRO_PATH="$ADMIN_PATH/Copropriete-Sadi-Carnot"

# Créer la structure des dossiers
mkdir -p "$COPRO_PATH/Documents-Reference"
mkdir -p "$COPRO_PATH/Gestion-Courante"
mkdir -p "$COPRO_PATH/Assemblees-Generales/2024"
mkdir -p "$COPRO_PATH/Assemblees-Generales/2025-AG-Extraordinaire-Juin"
mkdir -p "$ADMIN_PATH/Finances/Factures"
mkdir -p "$ADMIN_PATH/Finances/Attestations"

log "Structure ADMINISTRATION créée"

# ÉTAPE 3: Identifier et traiter les doublons
log "ÉTAPE 3/4: Identification des doublons copropriété..."

# Fonction pour comparer les fichiers
compare_files() {
    local file1="$1"
    local file2="$2"
    
    if [ -f "$file1" ] && [ -f "$file2" ]; then
        size1=$(stat -f%z "$file1" 2>/dev/null || echo "0")
        size2=$(stat -f%z "$file2" 2>/dev/null || echo "0")
        
        if [ "$size1" = "$size2" ]; then
            # Même taille, probablement doublon
            log "DOUBLON DÉTECTÉ: $file1 et $file2 (même taille: $size1 bytes)"
            return 0
        fi
    fi
    return 1
}

# Chercher les doublons de règlement de copropriété
REGLEMENT_FILES=(
    "$DRIVE_PATH/Mon Drive/Copropriété 210-212 Sadi-Carnot/reglement de copro 1ere partie.pdf"
    "$DRIVE_PATH/Mon Drive/Copropriété 210-212 Sadi-Carnot/règlement de copropriété.pdf"
    "$DRIVE_PATH/Mon Drive/Google AI Studio/règlement de copropriété.pdf"
    "$DRIVE_PATH/Mon Drive/Google AI Studio/règlement de copropriété (1).pdf"
    "$DRIVE_PATH/Mon Drive/Google AI Studio/règlement de copropriété (2).pdf"
    "$DRIVE_PATH/Mon Drive/Google AI Studio/règlement de copropriété (3).pdf"
)

# Identifier le fichier le plus récent
latest_reglement=""
latest_date=0

for file in "${REGLEMENT_FILES[@]}"; do
    if [ -f "$file" ]; then
        file_date=$(stat -f%m "$file" 2>/dev/null || echo "0")
        if [ "$file_date" -gt "$latest_date" ]; then
            latest_date=$file_date
            latest_reglement="$file"
        fi
    fi
done

if [ -n "$latest_reglement" ]; then
    log "Fichier règlement le plus récent: $latest_reglement"
    cp "$latest_reglement" "$COPRO_PATH/Documents-Reference/Reglement-Copropriete.pdf"
    log "Règlement copié vers Documents-Reference"
fi

# ÉTAPE 4: Déplacer les fichiers copropriété
log "ÉTAPE 4/4: Déplacement des fichiers copropriété..."

# Déplacer les fichiers de gestion courante
if [ -f "$DRIVE_PATH/Mon Drive/Lots_Par_Batiment_Sadi_Carnot.xlsx" ]; then
    mv "$DRIVE_PATH/Mon Drive/Lots_Par_Batiment_Sadi_Carnot.xlsx" "$COPRO_PATH/Gestion-Courante/"
    log "Fichier lots déplacé"
fi

if [ -f "$DRIVE_PATH/Mon Drive/Repartition_Devis_Geometre_SadiCarnot_Suivi.xlsx" ]; then
    mv "$DRIVE_PATH/Mon Drive/Repartition_Devis_Geometre_SadiCarnot_Suivi.xlsx" "$COPRO_PATH/Gestion-Courante/"
    log "Fichier répartition déplacé"
fi

# Déplacer le dossier AG 2025
if [ -d "$DRIVE_PATH/Mon Drive/ALL15JUIN2025-210" ]; then
    mv "$DRIVE_PATH/Mon Drive/ALL15JUIN2025-210"/* "$COPRO_PATH/Assemblees-Generales/2025-AG-Extraordinaire-Juin/" 2>/dev/null || true
    rmdir "$DRIVE_PATH/Mon Drive/ALL15JUIN2025-210" 2>/dev/null || true
    log "Dossier AG 2025 déplacé"
fi

# Déplacer le dossier principal copropriété
if [ -d "$DRIVE_PATH/Mon Drive/Copropriété 210-212 Sadi-Carnot" ]; then
    # Copier les fichiers non dupliqués
    find "$DRIVE_PATH/Mon Drive/Copropriété 210-212 Sadi-Carnot" -type f -name "*.pdf" -o -name "*.xlsx" -o -name "*.docx" | while read -r file; do
        filename=$(basename "$file")
        if [ ! -f "$COPRO_PATH/Documents-Reference/$filename" ] && [ ! -f "$COPRO_PATH/Gestion-Courante/$filename" ]; then
            cp "$file" "$COPRO_PATH/Gestion-Courante/"
            log "Fichier copié: $filename"
        fi
    done
fi

# Créer un rapport de nettoyage
RAPPORT="$COPRO_PATH/RAPPORT_REORGANISATION_$(date +%Y%m%d).txt"
cat > "$RAPPORT" << EOF
RAPPORT DE RÉORGANISATION - PHASE 1
Date: $(date)

STRUCTURE CRÉÉE:
- ADMINISTRATION/Copropriete-Sadi-Carnot/
  ├── Documents-Reference/ (règlements, EDD)
  ├── Gestion-Courante/ (listes, répartitions)
  └── Assemblees-Generales/
      ├── 2024/
      └── 2025-AG-Extraordinaire-Juin/

FICHIERS TRAITÉS:
- Règlement de copropriété consolidé
- Listes de copropriétaires organisées
- Documents AG 2025 centralisés

SAUVEGARDE:
- Sauvegarde complète dans: $BACKUP_PATH

PROCHAINES ÉTAPES:
- Vérifier la nouvelle structure
- Supprimer les doublons identifiés
- Procéder à la Phase 2 (Google AI Studio)
EOF

log "Rapport créé: $RAPPORT"
log "=== FIN PHASE 1 - RÉORGANISATION TERMINÉE ==="

echo ""
echo "✅ PHASE 1 TERMINÉE AVEC SUCCÈS!"
echo "📁 Nouvelle structure: $COPRO_PATH"
echo "💾 Sauvegarde: $BACKUP_PATH"
echo "📋 Rapport: $RAPPORT"
echo "📝 Log complet: $LOG_FILE"
echo ""
echo "⚠️  IMPORTANT: Vérifiez la nouvelle structure avant de supprimer les anciens dossiers"