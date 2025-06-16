#!/usr/bin/env python3
"""
Cloud Services Detector - Détection et analyse de tous les services cloud
Détecte iCloud, OneDrive, Google Drive, Dropbox, Box, etc.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import json

class CloudServicesDetector:
    def __init__(self, home_path=None):
        self.home_path = Path(home_path) if home_path else Path.home()
        self.cloud_services = {}
        self.optimization_opportunities = []
        
        # Définition des services cloud à détecter
        self.cloud_definitions = {
            'iCloud Drive': {
                'paths': [
                    'Library/Mobile Documents/com~apple~CloudDocs',
                    'iCloud Drive (Archive)',
                    'Library/Mobile Documents'
                ],
                'indicators': ['.icloud', 'com~apple~'],
                'processes': ['bird', 'cloudd'],
                'optimization_strategy': 'apple_optimized'
            },
            'Google Drive': {
                'paths': [
                    'Library/CloudStorage/GoogleDrive-*',
                    'Google Drive',
                    'GoogleDrive'
                ],
                'indicators': ['.tmp', '.gdownload', '.gdoc', '.gsheet'],
                'processes': ['Google Drive'],
                'optimization_strategy': 'google_optimized'
            },
            'OneDrive': {
                'paths': [
                    'Library/CloudStorage/OneDrive-*',
                    'OneDrive',
                    'OneDrive - *'
                ],
                'indicators': ['.tmp', '~$', '.lock'],
                'processes': ['OneDrive', 'Microsoft OneDrive'],
                'optimization_strategy': 'microsoft_optimized'
            },
            'Dropbox': {
                'paths': [
                    'Dropbox',
                    'Dropbox (Personal)',
                    'Dropbox (Business)'
                ],
                'indicators': ['.dropbox', '.dropbox.cache'],
                'processes': ['Dropbox'],
                'optimization_strategy': 'dropbox_optimized'
            },
            'Box': {
                'paths': [
                    'Box',
                    'Box Sync'
                ],
                'indicators': ['.boxsync'],
                'processes': ['Box'],
                'optimization_strategy': 'box_optimized'
            },
            'pCloud': {
                'paths': [
                    'pCloudDrive',
                    'pCloud'
                ],
                'indicators': ['.pcloud'],
                'processes': ['pCloud'],
                'optimization_strategy': 'generic_cloud'
            },
            'Mega': {
                'paths': [
                    'MEGAsync',
                    'Mega'
                ],
                'indicators': ['.mega'],
                'processes': ['MEGAsync'],
                'optimization_strategy': 'generic_cloud'
            }
        }
        
    def detect_all_cloud_services(self):
        """Détecte tous les services cloud présents"""
        print("☁️  DÉTECTION DES SERVICES CLOUD")
        print("=" * 40)
        
        for service_name, config in self.cloud_definitions.items():
            service_info = self.detect_service(service_name, config)
            if service_info['detected']:
                self.cloud_services[service_name] = service_info
                
        if not self.cloud_services:
            print("✅ Aucun service cloud détecté")
            return False
            
        # Analyser les opportunités d'optimisation
        self.analyze_optimization_opportunities()
        return True
        
    def detect_service(self, service_name, config):
        """Détecte un service cloud spécifique"""
        service_info = {
            'detected': False,
            'paths': [],
            'total_size': 0,
            'file_count': 0,
            'sync_active': False,
            'optimization_potential': 0,
            'issues': [],
            'strategy': config['optimization_strategy']
        }
        
        # 1. Rechercher les chemins
        detected_paths = self.find_service_paths(config['paths'])
        if not detected_paths:
            return service_info
            
        service_info['detected'] = True
        service_info['paths'] = detected_paths
        
        print(f"\n☁️  {service_name} détecté:")
        
        # 2. Analyser chaque chemin trouvé
        for path in detected_paths:
            path_info = self.analyze_cloud_path(path, config)
            service_info['total_size'] += path_info['size']
            service_info['file_count'] += path_info['file_count']
            service_info['issues'].extend(path_info['issues'])
            
            if path_info['sync_active']:
                service_info['sync_active'] = True
                
            print(f"  📁 {path}")
            print(f"     💾 Taille: {self.format_size(path_info['size'])}")
            print(f"     📄 Fichiers: {path_info['file_count']}")
            
            if path_info['issues']:
                print(f"     ⚠️  Problèmes: {len(path_info['issues'])}")
                for issue in path_info['issues'][:3]:
                    print(f"        • {issue}")
                    
        # 3. Vérifier les processus actifs
        if self.check_service_processes(config['processes']):
            service_info['sync_active'] = True
            print(f"  🔄 Processus de sync actif")
        else:
            print(f"  ✅ Pas de sync active")
            
        # 4. Calculer le potentiel d'optimisation
        service_info['optimization_potential'] = self.calculate_optimization_potential(service_info)
        print(f"  📊 Potentiel d'optimisation: {service_info['optimization_potential']}%")
        
        return service_info
        
    def find_service_paths(self, path_patterns):
        """Trouve les chemins d'un service cloud"""
        found_paths = []
        
        for pattern in path_patterns:
            if '*' in pattern:
                # Pattern avec wildcard
                parent_dir = self.home_path / Path(pattern).parent
                if parent_dir.exists():
                    pattern_name = Path(pattern).name.replace('*', '')
                    for item in parent_dir.iterdir():
                        if pattern_name in item.name and item.is_dir():
                            found_paths.append(str(item))
            else:
                # Chemin direct
                full_path = self.home_path / pattern
                if full_path.exists():
                    found_paths.append(str(full_path))
                    
        return found_paths
        
    def analyze_cloud_path(self, cloud_path, config):
        """Analyse un chemin cloud spécifique"""
        path_info = {
            'size': 0,
            'file_count': 0,
            'sync_active': False,
            'issues': []
        }
        
        cloud_dir = Path(cloud_path)
        
        try:
            # Calcul rapide de la taille avec du
            result = subprocess.run(['du', '-sb', str(cloud_dir)], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                path_info['size'] = int(result.stdout.split()[0])
        except:
            pass
            
        # Comptage des fichiers (échantillon)
        try:
            file_count = 0
            sync_files = 0
            
            for root, dirs, files in os.walk(cloud_dir):
                # Limiter la profondeur pour la performance
                level = len(Path(root).relative_to(cloud_dir).parts)
                if level > 3:
                    dirs.clear()
                    continue
                    
                file_count += len(files)
                
                # Détecter les indicateurs de sync
                for file in files:
                    for indicator in config['indicators']:
                        if indicator in file.lower():
                            sync_files += 1
                            path_info['sync_active'] = True
                            
                if file_count > 10000:  # Limiter pour la performance
                    break
                    
            path_info['file_count'] = file_count
            
            if sync_files > 0:
                path_info['issues'].append(f"{sync_files} fichiers de sync détectés")
                
        except Exception as e:
            path_info['issues'].append(f"Erreur d'analyse: {e}")
            
        # Détecter les problèmes spécifiques
        self.detect_cloud_issues(cloud_dir, config, path_info)
        
        return path_info
        
    def detect_cloud_issues(self, cloud_dir, config, path_info):
        """Détecte les problèmes spécifiques à un service cloud"""
        
        # Problèmes communs
        try:
            # Fichiers très volumineux non adaptés au cloud
            large_files = []
            for root, dirs, files in os.walk(cloud_dir):
                level = len(Path(root).relative_to(cloud_dir).parts)
                if level > 2:
                    dirs.clear()
                    continue
                    
                for file in files[:100]:  # Limiter l'échantillon
                    file_path = Path(root) / file
                    try:
                        if file_path.stat().st_size > 1024*1024*1024:  # > 1GB
                            large_files.append(file)
                    except:
                        continue
                        
                if len(large_files) >= 10:
                    break
                    
            if large_files:
                path_info['issues'].append(f"{len(large_files)} fichiers > 1GB")
                
            # Doublons potentiels
            duplicates = self.detect_cloud_duplicates(cloud_dir)
            if duplicates > 0:
                path_info['issues'].append(f"{duplicates} doublons potentiels")
                
            # Fichiers anciens non utilisés
            old_files = self.detect_old_unused_files(cloud_dir)
            if old_files > 0:
                path_info['issues'].append(f"{old_files} fichiers anciens (>1 an)")
                
        except Exception as e:
            path_info['issues'].append(f"Erreur détection problèmes: {e}")
            
    def detect_cloud_duplicates(self, cloud_dir):
        """Détecte les doublons dans un dossier cloud"""
        duplicates = 0
        seen_names = set()
        
        try:
            for root, dirs, files in os.walk(cloud_dir):
                level = len(Path(root).relative_to(cloud_dir).parts)
                if level > 2:
                    dirs.clear()
                    continue
                    
                for file in files[:200]:  # Échantillon
                    base_name = Path(file).stem.lower()
                    
                    # Patterns de doublons
                    if any(pattern in base_name for pattern in [
                        'copy', '(1)', '(2)', 'duplicate', 'backup'
                    ]):
                        duplicates += 1
                    elif base_name in seen_names:
                        duplicates += 1
                    else:
                        seen_names.add(base_name)
                        
        except:
            pass
            
        return duplicates
        
    def detect_old_unused_files(self, cloud_dir):
        """Détecte les fichiers anciens non utilisés"""
        old_files = 0
        one_year_ago = datetime.now() - timedelta(days=365)
        
        try:
            for root, dirs, files in os.walk(cloud_dir):
                level = len(Path(root).relative_to(cloud_dir).parts)
                if level > 2:
                    dirs.clear()
                    continue
                    
                for file in files[:100]:  # Échantillon
                    file_path = Path(root) / file
                    try:
                        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if mtime < one_year_ago:
                            old_files += 1
                    except:
                        continue
                        
        except:
            pass
            
        return old_files
        
    def check_service_processes(self, process_names):
        """Vérifie si des processus du service sont actifs"""
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            processes = result.stdout.lower()
            
            for process_name in process_names:
                if process_name.lower() in processes:
                    return True
                    
        except:
            pass
            
        return False
        
    def calculate_optimization_potential(self, service_info):
        """Calcule le potentiel d'optimisation d'un service"""
        potential = 0
        
        # Plus de problèmes = plus de potentiel
        potential += min(50, len(service_info['issues']) * 10)
        
        # Gros volume = plus de potentiel
        if service_info['total_size'] > 10 * 1024**3:  # > 10GB
            potential += 30
        elif service_info['total_size'] > 1 * 1024**3:  # > 1GB
            potential += 20
            
        # Beaucoup de fichiers = potentiel de doublons
        if service_info['file_count'] > 10000:
            potential += 20
        elif service_info['file_count'] > 1000:
            potential += 10
            
        return min(100, potential)
        
    def analyze_optimization_opportunities(self):
        """Analyse les opportunités d'optimisation globales"""
        print(f"\n💡 OPPORTUNITÉS D'OPTIMISATION")
        print("=" * 35)
        
        total_cloud_size = 0
        total_issues = 0
        
        for service_name, info in self.cloud_services.items():
            total_cloud_size += info['total_size']
            total_issues += len(info['issues'])
            
            if info['optimization_potential'] > 50:
                opportunity = {
                    'service': service_name,
                    'potential': info['optimization_potential'],
                    'strategy': info['strategy'],
                    'size': info['total_size'],
                    'issues': info['issues']
                }
                self.optimization_opportunities.append(opportunity)
                
        print(f"📊 Total espace cloud: {self.format_size(total_cloud_size)}")
        print(f"⚠️  Total problèmes détectés: {total_issues}")
        print(f"🎯 Services optimisables: {len(self.optimization_opportunities)}")
        
        # Proposer des stratégies d'optimisation
        self.generate_optimization_strategies()
        
    def generate_optimization_strategies(self):
        """Génère des stratégies d'optimisation spécifiques"""
        print(f"\n🎯 STRATÉGIES D'OPTIMISATION RECOMMANDÉES")
        print("=" * 45)
        
        if not self.optimization_opportunities:
            print("✅ Aucune optimisation majeure nécessaire")
            return
            
        for opportunity in sorted(self.optimization_opportunities, 
                                key=lambda x: x['potential'], reverse=True):
            
            print(f"\n☁️  {opportunity['service']} ({opportunity['potential']}% potentiel)")
            print(f"   💾 Taille: {self.format_size(opportunity['size'])}")
            
            strategy = self.get_optimization_strategy(opportunity['strategy'])
            for action in strategy:
                print(f"   {action}")
                
    def get_optimization_strategy(self, strategy_type):
        """Retourne les actions pour une stratégie d'optimisation"""
        strategies = {
            'apple_optimized': [
                "🔄 Optimiser le stockage iCloud dans Préférences Système",
                "📱 Activer 'Optimiser le stockage Mac' pour les Photos",
                "🗂️  Déplacer les gros fichiers vers 'iCloud Drive seulement'",
                "🧹 Vider la corbeille iCloud Drive",
                "📋 Archiver les anciens documents"
            ],
            'google_optimized': [
                "🔄 Utiliser 'Streaming files' au lieu de 'Mirror files'",
                "📁 Archiver les anciens Google Docs/Sheets",
                "🗑️  Nettoyer la corbeille Google Drive",
                "📸 Compresser les photos avec Google Photos",
                "🔗 Convertir les gros fichiers en liens partagés"
            ],
            'microsoft_optimized': [
                "☁️  Activer 'Files On-Demand' dans OneDrive",
                "📁 Déplacer les gros fichiers vers OneDrive Archive",
                "🗑️  Vider la corbeille OneDrive",
                "📋 Utiliser OneDrive Personal Vault pour les documents sensibles",
                "🔄 Synchroniser seulement les dossiers essentiels"
            ],
            'dropbox_optimized': [
                "💧 Activer 'Smart Sync' pour les gros dossiers",
                "🗂️  Utiliser Dropbox Paper au lieu de fichiers Word",
                "🗑️  Nettoyer les anciennes versions de fichiers",
                "📦 Archiver les projets terminés",
                "🔗 Utiliser les liens partagés pour les gros fichiers"
            ],
            'box_optimized': [
                "📦 Activer Box Drive pour optimiser l'espace local",
                "🗂️  Organiser en dossiers par projet/client",
                "🗑️  Nettoyer les anciennes versions",
                "🔄 Synchroniser seulement les dossiers actifs"
            ],
            'generic_cloud': [
                "💾 Configurer la synchronisation sélective",
                "📁 Organiser en structure de dossiers claire",
                "🗑️  Nettoyer les fichiers temporaires",
                "🔄 Vérifier les paramètres de synchronisation"
            ]
        }
        
        return strategies.get(strategy_type, strategies['generic_cloud'])
        
    def generate_optimization_commands(self):
        """Génère les commandes d'optimisation pour SmartOptimizer"""
        print(f"\n🔧 COMMANDES D'OPTIMISATION SMARTOPTIMIZER")
        print("=" * 45)
        
        for service_name, info in self.cloud_services.items():
            if info['optimization_potential'] > 30:
                for path in info['paths']:
                    print(f"\n# Optimiser {service_name}")
                    print(f"python3 src/optimizers/cloud_optimizer.py \"{path}\"")
                    print(f"python3 src/reorganizers/smart_reorganizer.py \"{path}\"")
                    
    def format_size(self, size_bytes):
        """Formate une taille en bytes"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} PB"

def main():
    if len(sys.argv) > 1:
        home_path = sys.argv[1]
    else:
        home_path = None
        
    detector = CloudServicesDetector(home_path)
    
    if detector.detect_all_cloud_services():
        detector.generate_optimization_commands()
        
        print(f"\n✅ Détection terminée")
        print(f"   Services détectés: {len(detector.cloud_services)}")
        print(f"   Opportunités d'optimisation: {len(detector.optimization_opportunities)}")
    else:
        print("ℹ️  Aucun service cloud détecté à optimiser")

if __name__ == "__main__":
    main()