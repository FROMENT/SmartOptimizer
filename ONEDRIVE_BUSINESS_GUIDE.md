# 🏢 Guide OneDrive Business/Enterprise - SmartOptimizer v1.2.0

## 🎯 Support Complet Multi-OS

SmartOptimizer v1.2.0 offre le **premier support vraiment universel** pour OneDrive Business/Enterprise sur **Windows**, **macOS** et **Linux**.

---

## 🔍 Détection Automatique des Tenants

### 🖥️ Windows - Registre
```bash
# Détection via registre Windows
python smart.py --business
```

**Détection automatique :**
- `HKEY_CURRENT_USER\SOFTWARE\Microsoft\OneDrive\Accounts\Business1`
- Nom du tenant, URL SharePoint, chemin local
- Support multi-organisations

### 🍎 macOS - CloudStorage
```bash
# Détection via CloudStorage natif
python3 smart.py --business
```

**Chemins détectés :**
- `~/Library/CloudStorage/OneDrive-[TenantName]`
- `~/Library/Preferences/com.microsoft.OneDrive-mac.plist`
- Support préférences système

### 🐧 Linux - Clients Tiers
```bash
# Détection via configuration clients
python3 smart.py --business
```

**Clients supportés :**
- OneDrive Free Client (abraunegg)
- rclone OneDrive configuration
- Configuration `~/.config/onedrive`

---

## 🎯 Cas d'Usage Entreprise

### 👥 Multi-Tenants
```bash
# Analyser tous les tenants
python3 src/analyzers/universal_cloud_detector.py --json

# Résultat exemple:
{
  "business_tenants": [
    {
      "name": "Contoso Ltd",
      "type": "Business",
      "local_path": "/Users/john/OneDrive - Contoso",
      "url": "https://contoso.sharepoint.com"
    },
    {
      "name": "Partner Corp", 
      "type": "Business_Guest",
      "local_path": "/Users/john/OneDrive - Partner Corp"
    }
  ]
}
```

### 📊 SharePoint Integration
```bash
# Sites SharePoint synchronisés
SharePoint - [SiteName]/
Teams - [TeamName]/
```

**Fonctionnalités détectées :**
- Documents collaboratifs
- Bibliothèques de documents
- Espaces Teams synchronisés
- Stratégies de compliance

---

## ⚙️ Configuration par OS

### 🖥️ Windows
```powershell
# Files On-Demand OneDrive
Set-ItemProperty -Path "HKCU:\Software\Microsoft\OneDrive" -Name "FilesOnDemandEnabled" -Value 1

# Stratégies GPO
# Group Policy Management pour contrôle entreprise
```

### 🍎 macOS
```bash
# Exclusions Time Machine
sudo tmutil addexclusion "/Users/$USER/OneDrive - Company"

# Préférences OneDrive
defaults read com.microsoft.OneDrive-mac
```

### 🐧 Linux
```bash
# systemd service OneDrive
systemctl --user enable onedrive
systemctl --user start onedrive

# Configuration multi-tenant
onedrive --display-config
```

---

## 🛡️ Sécurité Entreprise

### 🔒 Compliance
- **Respect des stratégies GPO**
- **Préservation des métadonnées**
- **Audit trail des modifications**
- **Sauvegardes avant optimisation**

### 📋 Validation
```bash
# Vérifier les stratégies actives
python3 smart.py --business

# Contrôler la synchronisation
# Avant optimisation automatique
```

---

## 📊 Optimisation Entreprise

### 🎯 Stratégies par Type
- **Documents Office** : Priorité conservation
- **Teams/SharePoint** : Synchronisation préservée
- **Archives** : Optimisation agressive
- **Collaboratif** : Déduplication prudente

### 🔧 Commandes Spécialisées
```bash
# Analyse OneDrive Business uniquement
python3 smart.py --business

# Optimisation avec respect compliance
python3 src/optimizers/cloud_deduplication_optimizer.py --business-mode

# Rapport détaillé pour audit
python3 src/analyzers/universal_cloud_detector.py --json > business_report.json
```

---

## 🚀 Workflows Entreprise

### 📈 Audit Mensuel
```bash
#!/bin/bash
# Script audit_onedrive_business.sh

# 1. Détection des tenants
python3 smart.py --business > tenants_report.txt

# 2. Analyse des problèmes
python3 src/analyzers/cloud_nesting_analyzer.py ~/

# 3. Rapport de compliance
python3 src/analyzers/universal_cloud_detector.py --json > compliance_report.json

# 4. Recommandations d'optimisation
echo "Rapport généré: $(date)" >> audit_log.txt
```

### 🧹 Nettoyage Contrôlé
```bash
# Mode simulation pour validation
SIMULATION_MODE=true python3 src/optimizers/cloud_deduplication_optimizer.py

# Après approbation, nettoyage réel
SIMULATION_MODE=false python3 src/optimizers/cloud_deduplication_optimizer.py
```

---

## 🔧 Résolution de Problèmes

### ❌ Problèmes Courants

#### Tenant Non Détecté
```bash
# Windows: Vérifier le registre
reg query "HKCU\Software\Microsoft\OneDrive"

# macOS: Vérifier CloudStorage
ls ~/Library/CloudStorage/OneDrive-*

# Linux: Vérifier la configuration
ls ~/.config/onedrive/
```

#### Synchronisation Bloquée
```bash
# Redémarrer OneDrive
# Windows: Restart OneDrive from system tray
# macOS: killall "OneDrive"
# Linux: systemctl --user restart onedrive
```

#### Permissions Insuffisantes
```bash
# Vérifier les droits d'accès
python3 smart.py --install
# Configure automatiquement les permissions
```

---

## 📚 Documentation Avancée

### 🔗 Liens Utiles
- **Microsoft 365 Admin Center** : Configuration tenant
- **SharePoint Admin** : Gestion des sites
- **OneDrive Admin** : Stratégies de synchronisation
- **Azure AD** : Gestion des utilisateurs et groupes

### 📖 Guides Connexes
- `MULTI_OS_GUIDE.md` - Support multi-plateforme
- `GUIDE_DEDOUBLONNAGE.md` - Optimisation des doublons
- `docs/security.md` - Sécurité et compliance

---

## 🎉 Conclusion

SmartOptimizer v1.2.0 révolutionne la gestion OneDrive Business/Enterprise en offrant :

✅ **Détection automatique** sur tous les OS  
✅ **Support multi-tenants** avec métadonnées  
✅ **Compliance entreprise** respectée  
✅ **Optimisation intelligente** préservant la collaboration  
✅ **Audit et reporting** intégrés  

**OneDrive Business n'a jamais été aussi simple à optimiser ! 🚀**