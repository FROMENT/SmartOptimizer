#!/usr/bin/env python3
"""
Platform Detector - Détection et gestion multi-OS
Support pour Windows, macOS, Linux avec chemins cloud spécifiques
"""

import os
import sys
import platform
from pathlib import Path
import subprocess

class PlatformDetector:
    def __init__(self):
        self.system = platform.system().lower()
        self.home_path = Path.home()
        self.username = os.getenv('USER') or os.getenv('USERNAME') or 'user'
        
        # Détection détaillée de l'OS
        self.is_windows = self.system == 'windows'
        self.is_macos = self.system == 'darwin'
        self.is_linux = self.system == 'linux'
        
        # Détection de l'environnement
        self.is_wsl = self.detect_wsl()
        self.is_admin = self.check_admin_rights()
        
    def detect_wsl(self):
        """Détecte si on est dans Windows Subsystem for Linux"""
        try:
            with open('/proc/version', 'r') as f:
                return 'microsoft' in f.read().lower()
        except:
            return False
            
    def check_admin_rights(self):
        """Vérifie les droits administrateur/root"""
        if self.is_windows:
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        else:
            return os.geteuid() == 0
            
    def get_cloud_service_paths(self):
        """Retourne les chemins des services cloud par OS"""
        paths = {
            'iCloud Drive': [],
            'Google Drive': [],
            'OneDrive Personal': [],
            'OneDrive Business': [],
            'OneDrive Enterprise': [],
            'Dropbox': [],
            'Box': [],
            'Sync.com': [],
            'pCloud': [],
            'MEGA': []
        }
        
        if self.is_windows:
            paths.update(self._get_windows_cloud_paths())
        elif self.is_macos:
            paths.update(self._get_macos_cloud_paths())
        elif self.is_linux:
            paths.update(self._get_linux_cloud_paths())
            
        return paths
        
    def _get_windows_cloud_paths(self):
        """Chemins cloud spécifiques Windows"""
        base_paths = {
            'iCloud Drive': [
                f'C:\\Users\\{self.username}\\iCloudDrive',
                f'C:\\Users\\{self.username}\\iCloud Drive'
            ],
            'Google Drive': [
                f'C:\\Users\\{self.username}\\Google Drive',
                f'C:\\Users\\{self.username}\\GoogleDrive',
                'G:\\',  # Drive mappé
                'H:\\'   # Drive alternatif
            ],
            'OneDrive Personal': [
                f'C:\\Users\\{self.username}\\OneDrive',
                f'C:\\Users\\{self.username}\\OneDrive - Personal'
            ],
            'OneDrive Business': [
                f'C:\\Users\\{self.username}\\OneDrive - *',
                f'C:\\Users\\{self.username}\\*\\OneDrive*',
                # Chemins typiques entreprise
                f'C:\\Users\\{self.username}\\OneDrive - Contoso',
                f'C:\\Users\\{self.username}\\OneDrive - Microsoft',
                f'C:\\Users\\{self.username}\\OneDrive for Business'
            ],
            'OneDrive Enterprise': [
                # Patterns SharePoint/Enterprise
                f'C:\\Users\\{self.username}\\*\\SharePoint*',
                f'C:\\Users\\{self.username}\\*\\Teams*',
                # Drives mappés entreprise
                'O:\\',  # OneDrive Enterprise
                'S:\\',  # SharePoint
                'T:\\'   # Teams
            ],
            'Dropbox': [
                f'C:\\Users\\{self.username}\\Dropbox',
                f'C:\\Users\\{self.username}\\Dropbox (Personal)',
                f'C:\\Users\\{self.username}\\Dropbox (Business)',
                f'C:\\Users\\{self.username}\\Dropbox (*)'
            ],
            'Box': [
                f'C:\\Users\\{self.username}\\Box',
                f'C:\\Users\\{self.username}\\Box Sync',
                'B:\\'  # Drive mappé Box
            ],
            'Sync.com': [
                f'C:\\Users\\{self.username}\\Sync',
                f'C:\\Users\\{self.username}\\Sync.com'
            ],
            'pCloud': [
                f'C:\\Users\\{self.username}\\pCloudDrive',
                'P:\\'  # Drive virtuel pCloud
            ],
            'MEGA': [
                f'C:\\Users\\{self.username}\\MEGA',
                f'C:\\Users\\{self.username}\\MEGAsync',
                'M:\\'  # Drive virtuel MEGA
            ]
        }
        
        return base_paths
        
    def _get_macos_cloud_paths(self):
        """Chemins cloud spécifiques macOS"""
        base_paths = {
            'iCloud Drive': [
                f'{self.home_path}/Library/Mobile Documents/com~apple~CloudDocs',
                f'{self.home_path}/iCloud Drive (Archive)',
                '/Users/Shared/iCloud Drive'
            ],
            'Google Drive': [
                f'{self.home_path}/Library/CloudStorage/GoogleDrive-*',
                f'{self.home_path}/Google Drive',
                f'{self.home_path}/GoogleDrive',
                '/Volumes/GoogleDrive'
            ],
            'OneDrive Personal': [
                f'{self.home_path}/OneDrive',
                f'{self.home_path}/OneDrive - Personal',
                f'{self.home_path}/Library/CloudStorage/OneDrive-Personal'
            ],
            'OneDrive Business': [
                f'{self.home_path}/Library/CloudStorage/OneDrive-*',
                f'{self.home_path}/OneDrive - *',
                f'{self.home_path}/OneDrive for Business',
                # Patterns entreprise macOS
                f'/Volumes/OneDrive - *',
                '/Volumes/OneDrive for Business'
            ],
            'OneDrive Enterprise': [
                # SharePoint et Teams sur macOS
                f'{self.home_path}/Library/CloudStorage/SharePoint-*',
                f'{self.home_path}/Library/CloudStorage/Teams-*',
                f'/Volumes/SharePoint - *',
                f'/Volumes/Teams - *'
            ],
            'Dropbox': [
                f'{self.home_path}/Dropbox',
                f'{self.home_path}/Dropbox (Personal)',
                f'{self.home_path}/Dropbox (Business)',
                '/Volumes/Dropbox'
            ],
            'Box': [
                f'{self.home_path}/Box',
                f'{self.home_path}/Box Sync',
                '/Volumes/Box'
            ],
            'Sync.com': [
                f'{self.home_path}/Sync',
                f'{self.home_path}/Sync.com'
            ],
            'pCloud': [
                f'{self.home_path}/pCloudDrive',
                '/Volumes/pCloud'
            ],
            'MEGA': [
                f'{self.home_path}/MEGA',
                f'{self.home_path}/MEGAsync',
                '/Volumes/MEGA'
            ]
        }
        
        return base_paths
        
    def _get_linux_cloud_paths(self):
        """Chemins cloud spécifiques Linux"""
        base_paths = {
            'iCloud Drive': [
                # Via navigateur ou solutions tierces
                f'{self.home_path}/.icloud',
                f'{self.home_path}/iCloud',
                f'{self.home_path}/Documents/iCloud'
            ],
            'Google Drive': [
                f'{self.home_path}/GoogleDrive',
                f'{self.home_path}/Google Drive',
                f'{self.home_path}/.google-drive',
                '/mnt/google-drive',
                '/media/google-drive'
            ],
            'OneDrive Personal': [
                f'{self.home_path}/OneDrive',
                f'{self.home_path}/.onedrive',
                '/mnt/onedrive'
            ],
            'OneDrive Business': [
                f'{self.home_path}/OneDrive-Business',
                f'{self.home_path}/OneDrive-*',
                f'{self.home_path}/.onedrive-business',
                '/mnt/onedrive-business'
            ],
            'OneDrive Enterprise': [
                f'{self.home_path}/SharePoint',
                f'{self.home_path}/Teams',
                f'{self.home_path}/.sharepoint',
                '/mnt/sharepoint'
            ],
            'Dropbox': [
                f'{self.home_path}/Dropbox',
                f'{self.home_path}/.dropbox',
                '/mnt/dropbox'
            ],
            'Box': [
                f'{self.home_path}/Box',
                f'{self.home_path}/.box',
                '/mnt/box'
            ],
            'Sync.com': [
                f'{self.home_path}/Sync',
                f'{self.home_path}/.sync'
            ],
            'pCloud': [
                f'{self.home_path}/pCloudDrive',
                f'{self.home_path}/.pcloud',
                '/mnt/pcloud'
            ],
            'MEGA': [
                f'{self.home_path}/MEGA',
                f'{self.home_path}/.mega',
                '/mnt/mega'
            ]
        }
        
        return base_paths
        
    def detect_onedrive_business_tenants(self):
        """Détecte les tenants OneDrive Business/Enterprise"""
        tenants = []
        
        if self.is_windows:
            tenants.extend(self._detect_windows_onedrive_tenants())
        elif self.is_macos:
            tenants.extend(self._detect_macos_onedrive_tenants())
        elif self.is_linux:
            tenants.extend(self._detect_linux_onedrive_tenants())
            
        return tenants
        
    def _detect_windows_onedrive_tenants(self):
        """Détecte les tenants OneDrive sur Windows"""
        tenants = []
        
        # Vérifier le registre Windows pour OneDrive Business
        try:
            import winreg
            
            # Clé registre OneDrive Business
            key_path = r"SOFTWARE\Microsoft\OneDrive\Accounts\Business1"
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                    tenant_name = winreg.QueryValueEx(key, "DisplayName")[0]
                    tenant_url = winreg.QueryValueEx(key, "SPOResourceId")[0]
                    local_path = winreg.QueryValueEx(key, "UserFolder")[0]
                    
                    tenants.append({
                        'name': tenant_name,
                        'url': tenant_url,
                        'local_path': local_path,
                        'type': 'Business'
                    })
            except:
                pass
                
        except ImportError:
            # Fallback sans registre
            pass
            
        # Détecter par structure de dossiers
        onedrive_root = Path(f"C:\\Users\\{self.username}")
        for item in onedrive_root.glob("OneDrive - *"):
            if item.is_dir():
                tenant_name = item.name.replace("OneDrive - ", "")
                tenants.append({
                    'name': tenant_name,
                    'local_path': str(item),
                    'type': 'Business_Detected'
                })
                
        return tenants
        
    def _detect_macos_onedrive_tenants(self):
        """Détecte les tenants OneDrive sur macOS"""
        tenants = []
        
        # Vérifier les préférences OneDrive
        plist_paths = [
            f"{self.home_path}/Library/Preferences/com.microsoft.OneDrive-mac.plist",
            f"{self.home_path}/Library/Group Containers/UBF8T346G9.OneDriveSyncClientSuite/com.microsoft.OneDrive-mac.plist"
        ]
        
        for plist_path in plist_paths:
            if Path(plist_path).exists():
                try:
                    # Utiliser plutil pour lire les préférences
                    result = subprocess.run(['plutil', '-p', plist_path], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        # Parser les informations du tenant
                        # (Simplifié - dans la vraie vie, parser le XML)
                        tenants.append({
                            'name': 'Business_from_plist',
                            'config_path': plist_path,
                            'type': 'Business'
                        })
                except:
                    pass
                    
        # Détecter par CloudStorage
        cloudstorage_path = Path(f"{self.home_path}/Library/CloudStorage")
        if cloudstorage_path.exists():
            for item in cloudstorage_path.glob("OneDrive-*"):
                if item.is_dir() and "Personal" not in item.name:
                    tenant_name = item.name.replace("OneDrive-", "")
                    tenants.append({
                        'name': tenant_name,
                        'local_path': str(item),
                        'type': 'Business_CloudStorage'
                    })
                    
        return tenants
        
    def _detect_linux_onedrive_tenants(self):
        """Détecte les tenants OneDrive sur Linux"""
        tenants = []
        
        # Vérifier les configurations onedrive (client libre)
        config_paths = [
            f"{self.home_path}/.config/onedrive",
            f"{self.home_path}/.onedrive"
        ]
        
        for config_path in config_paths:
            config_dir = Path(config_path)
            if config_dir.exists():
                for item in config_dir.iterdir():
                    if item.is_dir():
                        # Chaque sous-dossier peut être un tenant
                        tenants.append({
                            'name': item.name,
                            'config_path': str(item),
                            'type': 'Linux_Config'
                        })
                        
        return tenants
        
    def get_system_info(self):
        """Retourne les informations système détaillées"""
        info = {
            'os': self.system,
            'platform': platform.platform(),
            'architecture': platform.machine(),
            'python_version': platform.python_version(),
            'username': self.username,
            'home_path': str(self.home_path),
            'is_admin': self.is_admin,
            'is_wsl': self.is_wsl
        }
        
        # Informations spécifiques par OS
        if self.is_windows:
            info.update(self._get_windows_info())
        elif self.is_macos:
            info.update(self._get_macos_info())
        elif self.is_linux:
            info.update(self._get_linux_info())
            
        return info
        
    def _get_windows_info(self):
        """Informations spécifiques Windows"""
        info = {}
        try:
            info['windows_version'] = platform.win32_ver()
            info['domain'] = os.getenv('USERDOMAIN', 'Unknown')
            info['computer_name'] = os.getenv('COMPUTERNAME', 'Unknown')
        except:
            pass
        return info
        
    def _get_macos_info(self):
        """Informations spécifiques macOS"""
        info = {}
        try:
            info['macos_version'] = platform.mac_ver()
            result = subprocess.run(['sw_vers'], capture_output=True, text=True)
            if result.returncode == 0:
                info['system_version'] = result.stdout
        except:
            pass
        return info
        
    def _get_linux_info(self):
        """Informations spécifiques Linux"""
        info = {}
        try:
            info['linux_distribution'] = platform.freedesktop_os_release()
            if Path('/etc/os-release').exists():
                with open('/etc/os-release') as f:
                    info['os_release'] = f.read()
        except:
            pass
        return info
        
    def get_temp_directory(self):
        """Retourne le répertoire temporaire approprié"""
        if self.is_windows:
            return Path(os.getenv('TEMP', 'C:\\Temp'))
        else:
            return Path('/tmp')
            
    def get_config_directory(self):
        """Retourne le répertoire de configuration approprié"""
        if self.is_windows:
            return Path(os.getenv('APPDATA', f'C:\\Users\\{self.username}\\AppData\\Roaming'))
        elif self.is_macos:
            return Path(f'{self.home_path}/Library/Application Support')
        else:  # Linux
            return Path(f'{self.home_path}/.config')
            
    def format_path_for_os(self, path):
        """Formate un chemin selon l'OS"""
        path_obj = Path(path)
        
        if self.is_windows:
            # Utiliser les backslashes sur Windows
            return str(path_obj).replace('/', '\\')
        else:
            # Utiliser les slashes sur Unix
            return str(path_obj).replace('\\', '/')

def main():
    detector = PlatformDetector()
    
    print("🖥️  DÉTECTION PLATEFORME")
    print("=" * 30)
    
    # Informations système
    system_info = detector.get_system_info()
    print(f"OS: {system_info['os'].title()}")
    print(f"Plateforme: {system_info['platform']}")
    print(f"Utilisateur: {system_info['username']}")
    print(f"Home: {system_info['home_path']}")
    print(f"Admin/Root: {system_info['is_admin']}")
    
    if detector.is_wsl:
        print("🐧 WSL détecté")
        
    # Services cloud détectés
    print(f"\n☁️  Chemins cloud configurés:")
    cloud_paths = detector.get_cloud_service_paths()
    for service, paths in cloud_paths.items():
        if paths:
            print(f"  {service}:")
            for path in paths[:3]:  # Montrer 3 premiers chemins
                print(f"    • {path}")
                
    # Tenants OneDrive Business
    tenants = detector.detect_onedrive_business_tenants()
    if tenants:
        print(f"\n🏢 Tenants OneDrive Business détectés:")
        for tenant in tenants:
            print(f"  • {tenant['name']} ({tenant['type']})")
            if 'local_path' in tenant:
                print(f"    📁 {tenant['local_path']}")

if __name__ == "__main__":
    main()