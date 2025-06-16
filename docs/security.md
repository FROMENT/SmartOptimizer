# Guide de Sécurité SmartOptimizer

## 🔒 Philosophie de sécurité

SmartOptimizer applique le principe **"Sécurité d'abord"** avec des protections multicouches pour prévenir toute perte de données.

## 🛡️ Protections intégrées

### Mode simulation par défaut
- ✅ **Tous les scripts** démarrent en mode simulation
- ✅ **Aucune suppression** sans activation explicite
- ✅ **Prévisualisation complète** des actions proposées

### Sauvegarde automatique
- ✅ **Backup avant toute action** destructive
- ✅ **Répertoire horodaté** pour chaque session
- ✅ **Conservation des métadonnées** (dates, permissions)

### Détection des conflits
- ✅ **Protection des repos Git** actifs
- ✅ **Évitement des fichiers récents** (<24h)
- ✅ **Détection des fichiers verrouillés**

## ☁️ Sécurité Cloud

### Vérifications automatiques

SmartOptimizer vérifie automatiquement:

1. **Google Drive**
   - Fichiers `.tmp`, `.gdownload` en cours
   - Modifications récentes (< 5 minutes)
   - Processus Google Drive actifs

2. **iCloud Drive**  
   - Fichiers `.icloud` non téléchargés
   - Synchronisation en cours
   - État des téléchargements

3. **Dropbox**
   - Status API si disponible
   - Fichiers `.dropbox.cache`
   - Processus de sync actifs

4. **OneDrive**
   - Fichiers temporaires `.tmp`
   - Locks de synchronisation

### Script de vérification

```bash
# Vérification complète recommandée
./scripts/quick_cloud_safety_check.sh

# Vérification Python avancée
python3 src/utils/check_cloud_sync_status.py
```

### Interprétation des résultats

- 🟢 **FEUX VERTS**: Optimisation sûre, aucune sync détectée
- 🟡 **PRUDENCE**: Sync récente, attendre 5-10 minutes
- 🔴 **ARRÊT**: Synchronisation active, reporter l'optimisation

## 🔐 Protocoles de sécurité

### Avant toute optimisation

1. **Vérification cloud obligatoire**
```bash
./scripts/quick_cloud_safety_check.sh
# Attendre le feu vert avant de continuer
```

2. **Sauvegarde Time Machine recommandée**
```bash
# Vérifier que Time Machine est actif
sudo tmutil status
```

3. **Test en mode simulation**
```bash
# Toujours tester avant exécution réelle
python3 src/optimizers/quick_smart_optimizer.py ~/test_folder
```

### Pendant l'optimisation

1. **Surveillance continue**
   - Observer les notifications cloud
   - Vérifier les connexions réseau
   - Contrôler l'activité des processus

2. **Arrêt d'urgence**
```bash
# En cas de problème, arrêter immédiatement
killall python3
# Vérifier les backups automatiques
ls ~/SmartOptimizer_Backups/
```

### Après l'optimisation

1. **Vérification d'intégrité**
```bash
# Tester l'accès aux fichiers conservés
find ~/target_directory -type f -exec file {} \; | head -10
```

2. **Validation des sauvegardes**
```bash
# Vérifier que les backups sont complets
ls -la ~/SmartOptimizer_Backups/latest/
```

## ⚠️ Risques identifiés et mitigations

### Synchronisation cloud interrompue

**Risque**: Suppression pendant une sync peut corrompre les données
**Mitigation**: 
- Vérification automatique pré-optimisation
- Détection des fichiers temporaires
- Arrêt automatique si sync détectée

### Fichiers Git non commités

**Risque**: Perte de code non sauvegardé
**Mitigation**:
- Détection automatique des repos Git
- Protection des fichiers modifiés récemment
- Exclusion des dossiers `.git`

### Suppression de fichiers critiques

**Risque**: Suppression accidentelle de fichiers système
**Mitigation**:
- Liste blanche des répertoires sûrs
- Exclusion des fichiers système
- Scores de confiance conservateurs

### Conflits de nom lors de la réorganisation

**Risque**: Écrasement de fichiers lors du déplacement
**Mitigation**:
- Détection automatique des conflits
- Renommage intelligent avec suffixes
- Mode simulation pour prévisualisation

## 🚨 Procédures d'urgence

### Récupération de fichiers supprimés

1. **Backup SmartOptimizer**
```bash
# Les backups automatiques sont dans:
cd ~/SmartOptimizer_Backups/
ls -la
# Restaurer depuis le backup le plus récent
```

2. **Time Machine**
```bash
# Ouvrir Time Machine
open /Applications/Time\ Machine.app
# Naviguer vers la date d'avant optimisation
```

3. **Corbeille système**
```bash
# Vérifier la corbeille
ls ~/.Trash/
# Restaurer les fichiers si nécessaire
```

### Problèmes de synchronisation cloud

1. **Arrêt immédiat**
```bash
# Stopper tous les processus SmartOptimizer
pkill -f "smartoptimizer\|smart_optimizer"
```

2. **Vérification d'état**
```bash
# Vérifier l'état des services cloud
./scripts/quick_cloud_safety_check.sh
```

3. **Résolution manuelle**
```bash
# Forcer la synchronisation si nécessaire
# Google Drive: Redémarrer l'application
# iCloud: Forcer sync dans Préférences Système
```

## 🔍 Audit et surveillance

### Logs de sécurité

SmartOptimizer génère automatiquement:

- **cloud_sync_safety_report_YYYYMMDD_HHMMSS.txt**: État cloud
- **optimization_log_YYYYMMDD_HHMMSS.txt**: Actions effectuées
- **backup_manifest_YYYYMMDD_HHMMSS.txt**: Liste des sauvegardes

### Surveillance continue

```bash
# Surveiller l'activité en temps réel
tail -f ~/smartoptimizer_activity.log

# Vérifier les processus cloud actifs
watch -n 5 'ps aux | grep -E "(Google|iCloud|Dropbox)"'
```

## 📋 Checklist de sécurité

### Avant utilisation
- [ ] Time Machine activé et récent
- [ ] Vérification cloud safety passée
- [ ] Test en mode simulation effectué
- [ ] Backup manuel des dossiers critiques

### Pendant utilisation  
- [ ] Surveiller les notifications cloud
- [ ] Vérifier l'activité réseau
- [ ] Observer les logs en temps réel
- [ ] Garder un terminal ouvert pour arrêt d'urgence

### Après utilisation
- [ ] Vérifier l'intégrité des fichiers conservés
- [ ] Valider les backups automatiques
- [ ] Tester l'accès aux services cloud
- [ ] Archiver les logs d'optimisation

## 🆘 Contacts d'urgence

- **Support technique**: security@smartoptimizer.dev
- **Issues critiques**: [GitHub Critical Issues](https://github.com/user/SmartOptimizer/issues/new?template=security.md)
- **Chat temps réel**: [Discord SmartOptimizer](https://discord.gg/smartoptimizer)

## 📚 Ressources additionnelles

- [Guide de récupération de données](recovery-guide.md)
- [Protocoles de test de sécurité](security-testing.md)  
- [FAQ Sécurité](security-faq.md)
- [Meilleures pratiques cloud](cloud-best-practices.md)