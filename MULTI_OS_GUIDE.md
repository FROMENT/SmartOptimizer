# 🌍 Guide Multi-OS SmartOptimizer v1.2.0

## 🎯 Support Universel

SmartOptimizer v1.2.0 introduit le **support complet multi-OS** avec optimisation cloud intelligente pour **Windows**, **macOS** et **Linux**.

---

## 🖥️ Installation par OS

### Windows 10/11
```powershell
# Installation automatique
python install_universal.py

# Ou installation manuelle
git clone https://github.com/user/SmartOptimizer.git
cd SmartOptimizer
python install_universal.py
```

**Fonctionnalités Windows :**
- ✅ **Détection registre** OneDrive Business
- ✅ **Intégration PowerShell** pour performance
- ✅ **Raccourcis Bureau** automatiques
- ✅ **Support drives mappés** (G:, O:, S:)

### macOS 12+ (Monterey)
```bash
# Installation automatique
python3 install_universal.py

# Avec Homebrew (recommandé)
brew install python3
git clone https://github.com/user/SmartOptimizer.git
cd SmartOptimizer
python3 install_universal.py
```

**Fonctionnalités macOS :**
- ✅ **CloudStorage natif** (~/Library/CloudStorage)
- ✅ **Préférences système** intégrées
- ✅ **Spotlight exclusions** automatiques
- ✅ **iCloud Drive optimisé**

### Linux (Ubuntu/Debian/Fedora/Arch)
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip git
git clone https://github.com/user/SmartOptimizer.git
cd SmartOptimizer
python3 install_universal.py

# Fedora
sudo dnf install python3 python3-pip git
git clone https://github.com/user/SmartOptimizer.git
cd SmartOptimizer
python3 install_universal.py

# Arch Linux
sudo pacman -S python python-pip git
git clone https://github.com/user/SmartOptimizer.git
cd SmartOptimizer
python3 install_universal.py
```

**Fonctionnalités Linux :**
- ✅ **Clients tiers** OneDrive (abraunegg)
- ✅ **FUSE mounting** pour services cloud
- ✅ **Systemd integration** pour automatisation
- ✅ **rclone compatibility**

---

## ☁️ Détection Cloud par OS

### 🖥️ Windows - Chemins Détectés
```
📁 OneDrive Personal:
   C:\Users\[user]\OneDrive
   C:\Users\[user]\OneDrive - Personal

🏢 OneDrive Business:
   C:\Users\[user]\OneDrive - [Company]
   C:\Users\[user]\OneDrive for Business
   O:\ (drive mappé)

📊 Google Drive:
   C:\Users\[user]\Google Drive
   G:\ (drive mappé)

📦 Dropbox:
   C:\Users\[user]\Dropbox
   C:\Users\[user]\Dropbox (Business)

🍎 iCloud Drive:
   C:\Users\[user]\iCloudDrive
```

### 🍎 macOS - Chemins Détectés
```
📁 OneDrive Personal:
   ~/OneDrive
   ~/Library/CloudStorage/OneDrive-Personal

🏢 OneDrive Business:
   ~/Library/CloudStorage/OneDrive-[TenantName]
   ~/OneDrive - [Company]

📊 Google Drive:
   ~/Library/CloudStorage/GoogleDrive-[email]
   ~/Google Drive

🍎 iCloud Drive:
   ~/Library/Mobile Documents/com~apple~CloudDocs
   
📦 Dropbox:
   ~/Dropbox
   ~/Dropbox (Business)
```

### 🐧 Linux - Chemins Détectés
```
📁 OneDrive (via clients tiers):
   ~/.onedrive
   ~/OneDrive
   /mnt/onedrive

📊 Google Drive (via rclone/clients):
   ~/GoogleDrive
   ~/.google-drive
   /mnt/google-drive

📦 Dropbox:
   ~/Dropbox
   ~/.dropbox

☁️ Autres services:
   ~/[ServiceName]
   ~/.config/[service]
   /mnt/[service]
```

---

## 🏢 OneDrive Business/Enterprise

### Détection Automatique des Tenants

#### Windows - Registre
```python
# Détection via registre Windows
HKEY_CURRENT_USER\SOFTWARE\Microsoft\OneDrive\Accounts\Business1
- DisplayName: "Contoso Ltd"
- SPOResourceId: "https://contoso.sharepoint.com"
- UserFolder: "C:\Users\john\OneDrive - Contoso"
```

#### macOS - Préférences
```bash
# Détection via plists macOS
~/Library/Preferences/com.microsoft.OneDrive-mac.plist
~/Library/Group Containers/UBF8T346G9.OneDriveSyncClientSuite/
```

#### Linux - Configuration
```bash
# Détection via clients tiers
~/.config/onedrive/config
~/.onedrive/[tenant_name]/
```

### Cas d'Usage Entreprise

#### Multi-Tenants
```bash
# Détecter tous les tenants
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

#### SharePoint Integration
```bash
# Détecter les sites SharePoint synchronisés
SharePoint - [SiteName]
Teams - [TeamName]
```

---

## 🔧 Optimisations Spécifiques par OS

### Windows Optimizations
```powershell
# Files On-Demand OneDrive
Set-ItemProperty -Path "HKCU:\Software\Microsoft\OneDrive" -Name "FilesOnDemandEnabled" -Value 1

# Storage Sense activation
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\StorageSense" -Name "01" -Value 1

# Windows Defender exclusions
Add-MpPreference -ExclusionPath "C:\Users\$env:USERNAME\OneDrive"
```

### macOS Optimizations
```bash
# iCloud Drive optimization
defaults write com.apple.bird optimize-storage -bool true

# Spotlight exclusions
sudo mdutil -i off "/Users/$USER/OneDrive"

# Time Machine exclusions  
sudo tmutil addexclusion "/Users/$USER/OneDrive"
```

### Linux Optimizations
```bash
# systemd service for OneDrive
systemctl --user enable onedrive
systemctl --user start onedrive

# FUSE mount optimization
echo "user_allow_other" | sudo tee -a /etc/fuse.conf

# rclone configuration
rclone config create onedrive onedrive
```

---

## 🚀 Commandes Multi-OS

### Détection Universelle
```bash
# Windows
python src\analyzers\universal_cloud_detector.py

# macOS/Linux  
python3 src/analyzers/universal_cloud_detector.py
```

### Optimisation Cross-Platform
```bash
# Windows
python src\optimizers\cloud_deduplication_optimizer.py C:\Users\%USERNAME%

# macOS/Linux
python3 src/optimizers/cloud_deduplication_optimizer.py ~/
```

### Vérification Sécurité
```bash
# Windows (PowerShell/Git Bash)
scripts\quick_cloud_safety_check.sh

# macOS/Linux
./scripts/quick_cloud_safety_check.sh
```

---

## 🔄 Migration Cross-Platform

### Windows → macOS
```bash
# 1. Exporter la configuration Windows
python src\analyzers\universal_cloud_detector.py --json > windows_config.json

# 2. Sur macOS, importer et adapter
python3 src/utils/platform_migrator.py --from windows_config.json
```

### macOS → Linux
```bash
# 1. Sauvegarder la configuration macOS
python3 src/analyzers/universal_cloud_detector.py --json > macos_config.json

# 2. Sur Linux, configurer les clients équivalents
python3 src/utils/platform_migrator.py --from macos_config.json --target linux
```

---

## 🛡️ Sécurité Multi-OS

### Vérifications par OS

#### Windows
- ✅ **Processus OneDrive** actifs
- ✅ **Registre** cohérent
- ✅ **Files On-Demand** status
- ✅ **SharePoint sync** status

#### macOS
- ✅ **CloudStorage** status
- ✅ **Préférences système** sync
- ✅ **Spotlight indexing** status
- ✅ **iCloud sync** status

#### Linux
- ✅ **systemd services** status
- ✅ **Mount points** actifs
- ✅ **Client sync** status
- ✅ **FUSE** availability

---

## 📋 Troubleshooting par OS

### Windows Issues
```powershell
# Reset OneDrive
%localappdata%\Microsoft\OneDrive\onedrive.exe /reset

# Check registry
reg query "HKCU\Software\Microsoft\OneDrive"

# PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### macOS Issues
```bash
# Reset iCloud Drive
killall bird
killall cloudd

# Check preferences
defaults read com.apple.bird

# Permissions repair
sudo chmod -R 755 ~/Library/Mobile\ Documents/
```

### Linux Issues
```bash
# Reset OneDrive client
systemctl --user restart onedrive

# Check configuration
onedrive --display-config

# Permissions
chmod 755 ~/.config/onedrive/
```

---

## 🎯 Fonctionnalités Avancées

### API Integration
```python
# Utilisation programmatique
from src.utils.platform_detector import PlatformDetector
from src.analyzers.universal_cloud_detector import UniversalCloudDetector

detector = UniversalCloudDetector()
services = detector.detect_all_services()
```

### Automatisation
```bash
# Cron (Linux/macOS)
0 9 * * 1 /path/to/SmartOptimizer/src/analyzers/universal_cloud_detector.py

# Task Scheduler (Windows)
schtasks /create /tn "SmartOptimizer" /tr "python C:\SmartOptimizer\src\analyzers\universal_cloud_detector.py"
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: SmartOptimizer Analysis
  run: |
    python3 src/analyzers/universal_cloud_detector.py --json > cloud_report.json
```

---

## 🌟 Roadmap Multi-OS

### v1.3 (Prochain)
- [ ] **Interface graphique** Tkinter cross-platform
- [ ] **API REST** pour intégration entreprise
- [ ] **Plugin navigateur** pour tous les OS

### v2.0 (Vision)
- [ ] **Client natif** Windows/macOS/Linux
- [ ] **Synchronisation multi-appareils**
- [ ] **Mode collaboratif** entreprise

---

## 🆘 Support Multi-OS

### Par OS
- **Windows**: [Windows Issues](https://github.com/user/SmartOptimizer/issues?q=label%3Awindows)
- **macOS**: [macOS Issues](https://github.com/user/SmartOptimizer/issues?q=label%3Amacos)  
- **Linux**: [Linux Issues](https://github.com/user/SmartOptimizer/issues?q=label%3Alinux)

### Documentation
- 📖 **Guide général**: `docs/user-guide.md`
- 🏢 **OneDrive Business**: `ONEDRIVE_BUSINESS_GUIDE.md`
- 🔒 **Sécurité**: `docs/security.md`

**SmartOptimizer v1.2.0 - La première solution d'optimisation cloud vraiment universelle !** 🌍