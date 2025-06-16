#!/usr/bin/env python3
"""
Universal Installer - Installation multi-OS pour SmartOptimizer v1.2.0
Support Windows, macOS, Linux avec détection automatique

Auteur: Pascal Froment <pascal.froment@gmail.com>
GitHub: https://github.com/FROMENT/SmartOptimizer
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

class UniversalInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.is_windows = self.system == 'windows'
        self.is_macos = self.system == 'darwin'
        self.is_linux = self.system == 'linux'
        
        self.project_root = Path(__file__).parent
        self.home_path = Path.home()
        
    def install(self):
        """Installation principale multi-OS"""
        self.print_header()
        
        # Vérifications prérequises
        if not self.check_prerequisites():
            return False
            
        # Installation par OS
        if self.is_windows:
            return self.install_windows()
        elif self.is_macos:
            return self.install_macos()
        elif self.is_linux:
            return self.install_linux()
        else:
            print(f"❌ OS non supporté: {self.system}")
            return False
            
    def print_header(self):
        """Affiche l'en-tête d'installation"""
        print("🚀 SMARTOPTIMIZER v1.2.0 - INSTALLATION UNIVERSELLE")
        print("=" * 55)
        print(f"🖥️  OS détecté: {platform.system()} {platform.release()}")
        print(f"🐍 Python: {platform.python_version()}")
        print(f"📁 Home: {self.home_path}")
        print()
        
        print("🆕 Nouveautés v1.2.0:")
        print("   • Support multi-OS (Windows, macOS, Linux)")
        print("   • OneDrive Business/Enterprise complet")
        print("   • Détection automatique des tenants")
        print("   • Optimisation cross-platform")
        print()
        
    def check_prerequisites(self):
        """Vérifie les prérequis"""
        print("🔍 Vérification des prérequis...")
        
        # Vérifier Python
        python_version = sys.version_info
        if python_version < (3, 7):
            print(f"❌ Python 3.7+ requis, détecté: {platform.python_version()}")
            return False
        print(f"✅ Python {platform.python_version()}")
        
        # Vérifier les modules de base
        required_modules = ['pathlib', 'subprocess', 'json', 'hashlib']
        for module in required_modules:
            try:
                __import__(module)
                print(f"✅ Module {module}")
            except ImportError:
                print(f"❌ Module manquant: {module}")
                return False
                
        return True
        
    def install_windows(self):
        """Installation spécifique Windows"""
        print("🖥️  Installation Windows...")
        
        # Vérifier PowerShell
        if not self.check_powershell():
            print("⚠️  PowerShell recommandé pour une meilleure performance")
            
        # Installer les dépendances optionnelles
        self.install_windows_dependencies()
        
        # Configuration Windows
        self.configure_windows()
        
        # Créer les raccourcis
        self.create_windows_shortcuts()
        
        return True
        
    def install_macos(self):
        """Installation spécifique macOS"""
        print("🍎 Installation macOS...")
        
        # Vérifier les outils de développement
        if not self.check_xcode_tools():
            print("ℹ️  Outils de développement Xcode recommandés")
            
        # Installer les dépendances optionnelles
        self.install_macos_dependencies()
        
        # Configuration macOS
        self.configure_macos()
        
        return True
        
    def install_linux(self):
        """Installation spécifique Linux"""
        print("🐧 Installation Linux...")
        
        # Détecter la distribution
        distro = self.detect_linux_distro()
        print(f"   Distribution détectée: {distro}")
        
        # Installer les dépendances selon la distribution
        self.install_linux_dependencies(distro)
        
        # Configuration Linux
        self.configure_linux()
        
        return True
        
    def check_powershell(self):
        """Vérifie la disponibilité de PowerShell"""
        try:
            result = subprocess.run(['powershell', '-Command', 'echo "test"'], 
                                  capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
            
    def check_xcode_tools(self):
        """Vérifie les outils de développement Xcode"""
        try:
            result = subprocess.run(['xcode-select', '--version'], 
                                  capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
            
    def detect_linux_distro(self):
        """Détecte la distribution Linux"""
        try:
            if Path('/etc/os-release').exists():
                with open('/etc/os-release') as f:
                    content = f.read()
                    if 'ubuntu' in content.lower():
                        return 'ubuntu'
                    elif 'debian' in content.lower():
                        return 'debian'
                    elif 'fedora' in content.lower():
                        return 'fedora'
                    elif 'centos' in content.lower():
                        return 'centos'
                    elif 'arch' in content.lower():
                        return 'arch'
        except:
            pass
        return 'unknown'
        
    def install_windows_dependencies(self):
        """Installe les dépendances Windows"""
        print("   📦 Installation des dépendances Windows...")
        
        # Tenter d'installer via pip
        dependencies = ['Pillow', 'requests']
        for dep in dependencies:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                              check=True, capture_output=True)
                print(f"   ✅ {dep}")
            except:
                print(f"   ⚠️  {dep} - Installation optionnelle")
                
        # Vérifier winreg (inclus dans Python Windows)
        try:
            import winreg
            print("   ✅ winreg (accès registre)")
        except ImportError:
            print("   ⚠️  winreg non disponible")
            
    def install_macos_dependencies(self):
        """Installe les dépendances macOS"""
        print("   📦 Installation des dépendances macOS...")
        
        dependencies = ['Pillow', 'requests']
        for dep in dependencies:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                              check=True, capture_output=True)
                print(f"   ✅ {dep}")
            except:
                print(f"   ⚠️  {dep} - Installation optionnelle")
                
    def install_linux_dependencies(self, distro):
        """Installe les dépendances Linux selon la distribution"""
        print(f"   📦 Installation des dépendances Linux ({distro})...")
        
        # Dépendances Python
        dependencies = ['Pillow', 'requests']
        for dep in dependencies:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                              check=True, capture_output=True)
                print(f"   ✅ {dep}")
            except:
                print(f"   ⚠️  {dep} - Installation optionnelle")
                
        # Suggestions selon la distribution
        if distro in ['ubuntu', 'debian']:
            print("   💡 Pour OneDrive sur Ubuntu/Debian:")
            print("      sudo apt install onedrive")
        elif distro == 'fedora':
            print("   💡 Pour OneDrive sur Fedora:")
            print("      sudo dnf install onedrive")
        elif distro == 'arch':
            print("   💡 Pour OneDrive sur Arch:")
            print("      yay -S onedrive-abraunegg")
            
    def configure_windows(self):
        """Configuration spécifique Windows"""
        print("   ⚙️  Configuration Windows...")
        
        # Créer la configuration
        config_content = self.generate_config('windows')
        config_path = self.project_root / 'smartoptimizer.conf'
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
            
        print(f"   ✅ Configuration: {config_path}")
        
        # Rendre les scripts Python exécutables (pas nécessaire sur Windows)
        self.make_scripts_executable()
        
    def configure_macos(self):
        """Configuration spécifique macOS"""
        print("   ⚙️  Configuration macOS...")
        
        # Créer la configuration
        config_content = self.generate_config('macos')
        config_path = self.project_root / 'smartoptimizer.conf'
        
        with open(config_path, 'w') as f:
            f.write(config_content)
            
        print(f"   ✅ Configuration: {config_path}")
        
        # Rendre les scripts exécutables
        self.make_scripts_executable()
        
    def configure_linux(self):
        """Configuration spécifique Linux"""
        print("   ⚙️  Configuration Linux...")
        
        # Créer la configuration
        config_content = self.generate_config('linux')
        config_path = self.project_root / 'smartoptimizer.conf'
        
        with open(config_path, 'w') as f:
            f.write(config_content)
            
        print(f"   ✅ Configuration: {config_path}")
        
        # Rendre les scripts exécutables
        self.make_scripts_executable()
        
    def generate_config(self, os_type):
        """Génère la configuration selon l'OS"""
        
        if os_type == 'windows':
            backup_dir = f"{self.home_path}\\SmartOptimizer_Backups"
            temp_dir = "C:\\Temp\\SmartOptimizer"
        else:
            backup_dir = f"{self.home_path}/SmartOptimizer_Backups"
            temp_dir = "/tmp/SmartOptimizer"
            
        config = f"""# SmartOptimizer v1.2.0 - Configuration {os_type.title()}
# Génération automatique: {platform.system()} {platform.release()}

# Configuration de base
BACKUP_DIR="{backup_dir}"
TEMP_DIR="{temp_dir}"
SIMULATION_MODE=true
CONFIDENCE_THRESHOLD=70

# Configuration cloud
CLOUD_OPTIMIZATION=true
CLOUD_DEDUPLICATION_ENABLED=true
CLOUD_NESTING_DETECTION=true
CLOUD_SAFETY_CHECK_REQUIRED=true

# Support OneDrive Business/Enterprise
ONEDRIVE_BUSINESS_SUPPORT=true
TENANT_DETECTION=true

# Configuration OS
TARGET_OS="{os_type}"
CROSS_PLATFORM_MODE=true

# Performance
MAX_FILE_SCAN=10000
TIMEOUT_SECONDS=120
PARALLEL_PROCESSING=true
"""
        
        return config
        
    def make_scripts_executable(self):
        """Rend les scripts exécutables (Unix)"""
        if self.is_windows:
            return  # Pas nécessaire sur Windows
            
        executable_patterns = [
            'src/analyzers/*.py',
            'src/optimizers/*.py', 
            'src/reorganizers/*.py',
            'src/utils/*.py',
            'scripts/*.sh',
            'examples/*.sh',
            '*.py'
        ]
        
        for pattern in executable_patterns:
            for file_path in self.project_root.glob(pattern):
                if file_path.is_file():
                    try:
                        file_path.chmod(0o755)
                    except:
                        pass
                        
    def create_windows_shortcuts(self):
        """Crée des raccourcis Windows"""
        if not self.is_windows:
            return
            
        print("   🔗 Création des raccourcis Windows...")
        
        desktop = Path.home() / 'Desktop'
        if desktop.exists():
            try:
                # Créer un raccourci vers le détecteur cloud
                shortcut_content = f"""@echo off
cd /d "{self.project_root}"
python src\\analyzers\\universal_cloud_detector.py
pause"""
                
                shortcut_path = desktop / 'SmartOptimizer_CloudDetector.bat'
                with open(shortcut_path, 'w') as f:
                    f.write(shortcut_content)
                    
                print(f"   ✅ Raccourci: {shortcut_path}")
            except:
                print("   ⚠️  Impossible de créer les raccourcis")
                
    def create_start_menu_entries(self):
        """Crée les entrées du menu Démarrer (Windows)"""
        if not self.is_windows:
            return
            
        try:
            start_menu = Path.home() / 'AppData/Roaming/Microsoft/Windows/Start Menu/Programs'
            smartopt_folder = start_menu / 'SmartOptimizer'
            smartopt_folder.mkdir(exist_ok=True)
            
            # Créer les raccourcis
            shortcuts = {
                'Cloud Detector': 'src\\analyzers\\universal_cloud_detector.py',
                'Quick Overview': 'src\\analyzers\\ultra_quick_overview.py',
                'Safety Check': 'scripts\\quick_cloud_safety_check.sh'
            }
            
            for name, script_path in shortcuts.items():
                shortcut_content = f"""@echo off
cd /d "{self.project_root}"
python {script_path}
pause"""
                
                shortcut_file = smartopt_folder / f'{name}.bat'
                with open(shortcut_file, 'w') as f:
                    f.write(shortcut_content)
                    
        except:
            pass
            
    def display_completion_message(self):
        """Affiche le message de fin d'installation"""
        print()
        print("✅ INSTALLATION TERMINÉE")
        print("=" * 30)
        
        print(f"🖥️  SmartOptimizer v1.2.0 installé pour {platform.system()}")
        print(f"📁 Répertoire: {self.project_root}")
        
        print()
        print("🎯 COMMANDES DISPONIBLES:")
        print("========================")
        
        if self.is_windows:
            print("📊 Détection cloud:")
            print(f"   python {self.project_root}\\src\\analyzers\\universal_cloud_detector.py")
            print()
            print("🔒 Vérification sécurité:")
            print(f"   {self.project_root}\\scripts\\quick_cloud_safety_check.sh")
            print()
        else:
            print("📊 Détection cloud:")
            print(f"   python3 {self.project_root}/src/analyzers/universal_cloud_detector.py")
            print()
            print("🔒 Vérification sécurité:")
            print(f"   {self.project_root}/scripts/quick_cloud_safety_check.sh")
            print()
            
        print("☁️  Optimisation multi-OS:")
        if self.is_windows:
            print(f"   python {self.project_root}\\src\\optimizers\\cloud_deduplication_optimizer.py")
        else:
            print(f"   python3 {self.project_root}/src/optimizers/cloud_deduplication_optimizer.py")
            
        print()
        print("📚 Documentation:")
        print("   • Guide utilisateur: docs/user-guide.md")
        print("   • Support multi-OS: MULTI_OS_GUIDE.md")
        print("   • OneDrive Business: ONEDRIVE_BUSINESS_GUIDE.md")
        
        print()
        print("🏢 SUPPORT ONEDRIVE BUSINESS:")
        print("============================")
        print("✅ Détection automatique des tenants")
        print("✅ Support Windows, macOS, Linux")
        print("✅ Optimisation cross-platform")
        print("✅ Gestion des conflits entreprise")
        
        if self.is_windows:
            print()
            print("🖥️  SPÉCIAL WINDOWS:")
            print("   • Raccourcis créés sur le Bureau")
            print("   • Support registre OneDrive")
            print("   • Intégration PowerShell")
            
def main():
    installer = UniversalInstaller()
    
    print("🌍 SmartOptimizer - Installation Universelle")
    print("Support Windows, macOS, Linux + OneDrive Business")
    print()
    
    try:
        if installer.install():
            installer.display_completion_message()
            print()
            print("🎉 Installation réussie! SmartOptimizer est prêt.")
            return 0
        else:
            print("❌ Erreur durant l'installation")
            return 1
    except KeyboardInterrupt:
        print()
        print("❌ Installation interrompue par l'utilisateur")
        return 1
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())