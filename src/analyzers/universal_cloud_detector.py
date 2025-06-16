#!/usr/bin/env python3
"""
Universal Cloud Detector - Détecteur cloud multi-OS
Support Windows, macOS, Linux + OneDrive Enterprise/Business
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import json
import glob

# Ajouter le répertoire parent pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.platform_detector import PlatformDetector

class UniversalCloudDetector:
    def __init__(self, target_path=None):
        self.platform = PlatformDetector()
        self.target_path = Path(target_path) if target_path else self.platform.home_path
        self.detected_services = {}
        self.business_tenants = []
        
    def detect_all_services(self):
        """Détecte tous les services cloud sur tous les OS"""
        print(f"☁️  DÉTECTION CLOUD UNIVERSELLE")
        print(f"🖥️  OS: {self.platform.system.title()}")
        print("=" * 40)
        
        # Obtenir les chemins selon l'OS
        cloud_paths = self.platform.get_cloud_service_paths()
        
        # Détecter chaque service
        for service_name, possible_paths in cloud_paths.items():
            detected_paths = self.find_existing_paths(possible_paths)
            
            if detected_paths:
                service_info = self.analyze_service(service_name, detected_paths)
                self.detected_services[service_name] = service_info
                
        # Détection spéciale OneDrive Business/Enterprise
        self.detect_onedrive_business()
        
        # Afficher les résultats
        self.display_results()
        
        return len(self.detected_services) > 0
        
    def find_existing_paths(self, possible_paths):
        """Trouve les chemins qui existent réellement"""
        existing_paths = []
        
        for path_pattern in possible_paths:
            if '*' in path_pattern:
                # Utiliser glob pour les patterns
                try:
                    matches = glob.glob(str(path_pattern))
                    for match in matches:
                        path_obj = Path(match)
                        if path_obj.exists() and path_obj.is_dir():
                            existing_paths.append(path_obj)
                except:
                    continue
            else:
                # Chemin direct
                path_obj = Path(path_pattern)
                if path_obj.exists() and path_obj.is_dir():
                    existing_paths.append(path_obj)
                    
        return existing_paths
        
    def analyze_service(self, service_name, paths):
        """Analyse détaillée d'un service cloud"""
        service_info = {
            'name': service_name,
            'paths': [str(p) for p in paths],
            'total_size': 0,
            'file_count': 0,
            'sync_status': 'unknown',
            'last_activity': None,
            'issues': [],
            'business_info': {}
        }
        
        print(f"\n☁️  {service_name} détecté:")
        
        for path in paths:
            print(f"  📁 {path}")
            
            # Analyser la taille
            size = self.get_directory_size(path)
            service_info['total_size'] += size
            print(f"     💾 Taille: {self.format_size(size)}")
            
            # Analyser l'activité
            file_count, last_activity = self.analyze_activity(path)
            service_info['file_count'] += file_count
            
            if last_activity:
                if not service_info['last_activity'] or last_activity > service_info['last_activity']:
                    service_info['last_activity'] = last_activity
                    
            print(f"     📄 Fichiers: {file_count}")
            
            # Détecter le statut de sync
            sync_status = self.detect_sync_status(service_name, path)
            if sync_status != 'unknown':
                service_info['sync_status'] = sync_status
                print(f"     🔄 Sync: {sync_status}")
                
            # Détecter les problèmes
            issues = self.detect_service_issues(service_name, path)
            service_info['issues'].extend(issues)
            
            if issues:
                print(f"     ⚠️  {len(issues)} problème(s) détecté(s)")
                
        # Analyse spéciale pour OneDrive Business
        if 'OneDrive' in service_name and 'Business' in service_name:
            business_info = self.analyze_business_features(paths[0] if paths else None)
            service_info['business_info'] = business_info
            
        return service_info
        
    def get_directory_size(self, path):
        """Calcule la taille d'un répertoire (multi-OS)"""
        try:
            if self.platform.is_windows:
                # Utiliser PowerShell sur Windows pour plus de précision
                cmd = f'(Get-ChildItem -Path "{path}" -Recurse -Force | Measure-Object -Property Length -Sum).Sum'
                result = subprocess.run(['powershell', '-Command', cmd], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0 and result.stdout.strip():
                    return int(result.stdout.strip())
            else:
                # Utiliser du sur Unix
                result = subprocess.run(['du', '-sb', str(path)], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    return int(result.stdout.split()[0])
        except:
            pass
            
        # Fallback manuel
        total_size = 0
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    try:
                        file_path = Path(root) / file
                        total_size += file_path.stat().st_size
                    except:
                        continue
                # Limiter pour éviter les timeouts
                if total_size > 10 * 1024**3:  # 10GB max
                    break
        except:
            pass
            
        return total_size
        
    def analyze_activity(self, path):
        """Analyse l'activité dans un dossier"""
        file_count = 0
        last_activity = None
        
        try:
            for root, dirs, files in os.walk(path):
                file_count += len(files)
                
                # Vérifier les dates de modification récentes
                for file in files[:50]:  # Échantillon
                    try:
                        file_path = Path(root) / file
                        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        
                        if not last_activity or mtime > last_activity:
                            last_activity = mtime
                            
                    except:
                        continue
                        
                # Limiter la profondeur
                level = len(Path(root).relative_to(path).parts)
                if level > 3:
                    dirs.clear()
                    
                # Limiter le nombre total pour la performance
                if file_count > 10000:
                    break
                    
        except Exception:
            pass
            
        return file_count, last_activity
        
    def detect_sync_status(self, service_name, path):
        """Détecte le statut de synchronisation"""
        
        # Indicateurs de sync par service et OS
        sync_indicators = {
            'Windows': {
                'OneDrive': ['.tmp', '~$', '.lock'],
                'Google Drive': ['.tmp', '.gdownload'],
                'Dropbox': ['.dropbox.cache', 'desktop.ini'],
                'Box': ['.boxsync']
            },
            'Darwin': {  # macOS
                'OneDrive': ['.tmp', '.lock', 'Icon\r'],
                'Google Drive': ['.tmp', '.gdownload'],
                'Dropbox': ['.dropbox', '.dropbox.cache'],
                'iCloud': ['.icloud']
            },
            'Linux': {
                'OneDrive': ['.tmp', '.lock'],
                'Google Drive': ['.tmp'],
                'Dropbox': ['.dropbox']
            }
        }
        
        os_indicators = sync_indicators.get(self.platform.system.title(), {})
        service_indicators = []
        
        # Trouver les indicateurs pour ce service
        for key, indicators in os_indicators.items():
            if key in service_name:
                service_indicators = indicators
                break
                
        if not service_indicators:
            return 'unknown'
            
        # Chercher les indicateurs
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    for indicator in service_indicators:
                        if indicator in file.lower():
                            return 'syncing'
                            
                # Limiter la recherche
                level = len(Path(root).relative_to(path).parts)
                if level > 2:
                    dirs.clear()
                    
        except Exception:
            pass
            
        return 'idle'
        
    def detect_service_issues(self, service_name, path):
        """Détecte les problèmes spécifiques à un service"""
        issues = []
        
        try:
            # Problèmes communs
            
            # 1. Fichiers de conflit
            conflict_count = 0
            for root, dirs, files in os.walk(path):
                for file in files:
                    if any(pattern in file.lower() for pattern in 
                          ['conflict', 'conflicted', 'case conflict', 'sync conflict']):
                        conflict_count += 1
                        
                level = len(Path(root).relative_to(path).parts)
                if level > 2:
                    dirs.clear()
                    
            if conflict_count > 0:
                issues.append(f"{conflict_count} fichiers de conflit détectés")
                
            # 2. Fichiers très volumineux (>1GB)
            large_files = 0
            for root, dirs, files in os.walk(path):
                for file in files[:100]:  # Échantillon
                    try:
                        file_path = Path(root) / file
                        if file_path.stat().st_size > 1024**3:  # 1GB
                            large_files += 1
                    except:
                        continue
                        
                level = len(Path(root).relative_to(path).parts)
                if level > 1:
                    dirs.clear()
                    
            if large_files > 5:
                issues.append(f"{large_files} fichiers très volumineux (>1GB)")
                
            # 3. Problèmes spécifiques OneDrive
            if 'OneDrive' in service_name:
                # Fichiers avec caractères problématiques
                problem_chars = 0
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if any(char in file for char in ['<', '>', ':', '"', '|', '?', '*']):
                            problem_chars += 1
                            
                    level = len(Path(root).relative_to(path).parts)
                    if level > 2:
                        dirs.clear()
                        
                if problem_chars > 0:
                    issues.append(f"{problem_chars} fichiers avec caractères interdits OneDrive")
                    
        except Exception:
            pass
            
        return issues
        
    def detect_onedrive_business(self):
        """Détection spécialisée OneDrive Business/Enterprise"""
        print(f"\n🏢 Détection OneDrive Business/Enterprise...")
        
        tenants = self.platform.detect_onedrive_business_tenants()
        
        for tenant in tenants:
            print(f"  📋 Tenant: {tenant['name']}")
            print(f"     Type: {tenant['type']}")
            
            if 'local_path' in tenant:
                path = Path(tenant['local_path'])
                if path.exists():
                    size = self.get_directory_size(path)
                    print(f"     💾 Taille: {self.format_size(size)}")
                    
                    # Analyser les caractéristiques business
                    business_features = self.analyze_business_features(path)
                    if business_features:
                        print(f"     🏢 Fonctionnalités entreprise détectées:")
                        for feature in business_features:
                            print(f"        • {feature}")
                            
            self.business_tenants.append(tenant)
            
    def analyze_business_features(self, path):
        """Analyse les fonctionnalités OneDrive Business"""
        features = []
        
        try:
            # Chercher des dossiers typiques entreprise
            business_folders = [
                'Teams', 'SharePoint', 'Projects', 'Shared', 
                'Company', 'Department', 'Policies'
            ]
            
            for item in path.iterdir():
                if item.is_dir():
                    folder_name = item.name.lower()
                    for business_folder in business_folders:
                        if business_folder.lower() in folder_name:
                            features.append(f"Dossier {business_folder}")
                            
            # Chercher des fichiers Office avec métadonnées entreprise
            office_files = 0
            for file_path in path.rglob("*.docx"):
                office_files += 1
                if office_files > 20:  # Beaucoup de documents Office
                    features.append("Nombreux documents Office")
                    break
                    
        except Exception:
            pass
            
        return features
        
    def display_results(self):
        """Affiche les résultats de détection"""
        
        if not self.detected_services:
            print("\n✅ Aucun service cloud détecté")
            return
            
        print(f"\n📊 RÉSUMÉ DE DÉTECTION")
        print("=" * 25)
        
        total_size = 0
        total_files = 0
        total_issues = 0
        
        for service_name, info in self.detected_services.items():
            total_size += info['total_size']
            total_files += info['file_count']
            total_issues += len(info['issues'])
            
        print(f"Services détectés: {len(self.detected_services)}")
        print(f"Espace cloud total: {self.format_size(total_size)}")
        print(f"Fichiers total: {total_files:,}")
        print(f"Problèmes détectés: {total_issues}")
        
        if self.business_tenants:
            print(f"Tenants entreprise: {len(self.business_tenants)}")
            
        # Recommandations par OS
        self.generate_os_specific_recommendations()
        
    def generate_os_specific_recommendations(self):
        """Génère des recommandations spécifiques à l'OS"""
        print(f"\n💡 RECOMMANDATIONS {self.platform.system.upper()}")
        print("=" * 35)
        
        if self.platform.is_windows:
            self.generate_windows_recommendations()
        elif self.platform.is_macos:
            self.generate_macos_recommendations()
        elif self.platform.is_linux:
            self.generate_linux_recommendations()
            
    def generate_windows_recommendations(self):
        """Recommandations spécifiques Windows"""
        print("🖥️  Optimisations Windows:")
        print("   • Activer 'Files On-Demand' pour OneDrive")
        print("   • Utiliser 'Storage Sense' pour nettoyer automatiquement")
        print("   • Configurer les exclusions Windows Defender")
        print("   • Utiliser PowerShell pour l'automatisation")
        
        if 'OneDrive Business' in self.detected_services:
            print("   • Configurer les stratégies GPO pour OneDrive Business")
            print("   • Utiliser SharePoint pour la collaboration")
            
    def generate_macos_recommendations(self):
        """Recommandations spécifiques macOS"""
        print("🍎 Optimisations macOS:")
        print("   • Utiliser iCloud Drive comme service principal")
        print("   • Activer 'Optimize Mac Storage' dans System Preferences")
        print("   • Configurer les exclusions Time Machine")
        print("   • Utiliser Automator pour l'automatisation")
        
    def generate_linux_recommendations(self):
        """Recommandations spécifiques Linux"""
        print("🐧 Optimisations Linux:")
        print("   • Utiliser rclone pour une meilleure gestion cloud")
        print("   • Configurer systemd pour l'automatisation")
        print("   • Utiliser FUSE pour monter les services cloud")
        print("   • Considérer des clients tiers comme OneDrive Free Client")
        
    def format_size(self, size_bytes):
        """Formate une taille en bytes"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} PB"

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Universal Cloud Detector')
    parser.add_argument('path', nargs='?', default=None, 
                       help='Path to analyze (default: user home)')
    parser.add_argument('--json', action='store_true',
                       help='Output results in JSON format')
    
    args = parser.parse_args()
    
    detector = UniversalCloudDetector(args.path)
    
    if detector.detect_all_services():
        if args.json:
            # Output JSON pour intégration
            results = {
                'platform': detector.platform.get_system_info(),
                'services': detector.detected_services,
                'business_tenants': detector.business_tenants
            }
            print(json.dumps(results, indent=2, default=str))
    else:
        if not args.json:
            print("ℹ️  Aucun service cloud détecté à optimiser")

if __name__ == "__main__":
    main()