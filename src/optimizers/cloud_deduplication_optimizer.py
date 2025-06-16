#!/usr/bin/env python3
"""
Cloud Deduplication Optimizer - Optimiseur de déduplication cloud
Résout les problèmes d'imbrication et élimine les doublons inter-cloud
"""

import os
import sys
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import subprocess
import json

class CloudDeduplicationOptimizer:
    def __init__(self, home_path=None):
        self.home_path = Path(home_path) if home_path else Path.home()
        self.backup_dir = Path.home() / "SmartOptimizer_Backups" / "cloud_deduplication" / datetime.now().strftime('%Y%m%d_%H%M%S')
        self.simulation_mode = True
        self.cloud_services = {}
        self.optimization_actions = []
        self.space_recovered = 0
        
        # Configuration des services cloud
        self.cloud_config = {
            'iCloud Drive': {
                'priority': 1,  # Plus haute priorité pour les fichiers Apple
                'best_for': ['documents', 'desktop', 'photos'],
                'exclude_patterns': ['.icloud', 'com~apple~']
            },
            'Google Drive': {
                'priority': 2,
                'best_for': ['collaboration', 'office_docs', 'shared_projects'],
                'exclude_patterns': ['.tmp', '.gdownload', '.gdoc']
            },
            'OneDrive': {
                'priority': 2,
                'best_for': ['office_365', 'business_docs', 'teams'],
                'exclude_patterns': ['~$', '.tmp', '.lock']
            },
            'Dropbox': {
                'priority': 3,
                'best_for': ['creative_projects', 'large_files', 'external_sharing'],
                'exclude_patterns': ['.dropbox', 'conflicted copy']
            },
            'Box': {
                'priority': 4,
                'best_for': ['enterprise', 'compliance'],
                'exclude_patterns': ['.boxsync']
            }
        }
        
    def optimize_cloud_deduplication(self):
        """Optimise la déduplication entre services cloud"""
        print("🔄 OPTIMISEUR DE DÉDUPLICATION CLOUD")
        print("=" * 45)
        
        if not self.simulation_mode:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            
        # 1. Détecter tous les services cloud
        self.detect_cloud_services()
        
        # 2. Analyser les doublons inter-cloud
        self.analyze_cross_cloud_duplicates()
        
        # 3. Résoudre les imbrications problématiques
        self.resolve_cloud_nesting()
        
        # 4. Optimiser les dossiers système synchronisés
        self.optimize_system_folders()
        
        # 5. Créer la structure optimale
        self.create_optimal_structure()
        
        # 6. Rapport final
        self.generate_optimization_report()
        
        return len(self.optimization_actions) > 0
        
    def detect_cloud_services(self):
        """Détecte et analyse tous les services cloud"""
        print("☁️  Détection des services cloud...")
        
        cloud_paths = {
            'iCloud Drive': [
                'Library/Mobile Documents/com~apple~CloudDocs'
            ],
            'Google Drive': [
                'Library/CloudStorage/GoogleDrive-*',
                'Google Drive*'
            ],
            'OneDrive': [
                'Library/CloudStorage/OneDrive-*',
                'OneDrive*'
            ],
            'Dropbox': [
                'Dropbox*'
            ],
            'Box': [
                'Box*'
            ]
        }
        
        for service_name, patterns in cloud_paths.items():
            paths = self.find_service_paths(patterns)
            if paths:
                self.cloud_services[service_name] = {
                    'paths': paths,
                    'size': sum(self.get_directory_size(p) for p in paths),
                    'priority': self.cloud_config.get(service_name, {}).get('priority', 5),
                    'best_for': self.cloud_config.get(service_name, {}).get('best_for', []),
                    'file_inventory': {}
                }
                print(f"  ✅ {service_name}: {len(paths)} chemin(s), {self.format_size(self.cloud_services[service_name]['size'])}")
                
    def find_service_paths(self, patterns):
        """Trouve les chemins d'un service cloud"""
        found_paths = []
        
        for pattern in patterns:
            if '*' in pattern:
                parent_dir = self.home_path / Path(pattern).parent if Path(pattern).parent != '.' else self.home_path
                if parent_dir.exists():
                    pattern_name = Path(pattern).name.replace('*', '')
                    for item in parent_dir.iterdir():
                        if pattern_name in item.name and item.is_dir():
                            found_paths.append(item)
            else:
                full_path = self.home_path / pattern
                if full_path.exists():
                    found_paths.append(full_path)
                    
        return found_paths
        
    def get_directory_size(self, path):
        """Obtient la taille d'un répertoire"""
        try:
            result = subprocess.run(['du', '-sb', str(path)], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return int(result.stdout.split()[0])
        except:
            pass
        return 0
        
    def analyze_cross_cloud_duplicates(self):
        """Analyse les doublons entre services cloud"""
        print("\n🔍 Analyse des doublons inter-cloud...")
        
        # Inventorier tous les fichiers de chaque service
        all_files = {}
        
        for service_name, info in self.cloud_services.items():
            print(f"  📁 Inventaire {service_name}...")
            service_files = {}
            
            for cloud_path in info['paths']:
                files = self.inventory_files(cloud_path)
                service_files.update(files)
                
            info['file_inventory'] = service_files
            
            # Ajouter à l'inventaire global
            for file_hash, file_info in service_files.items():
                if file_hash not in all_files:
                    all_files[file_hash] = []
                all_files[file_hash].append((service_name, file_info))
                
        # Identifier les vrais doublons
        duplicates_found = 0
        total_duplicate_space = 0
        
        for file_hash, locations in all_files.items():
            if len(locations) > 1:
                # Plusieurs services ont le même fichier
                services = [loc[0] for loc in locations]
                file_size = locations[0][1]['size']
                
                duplicates_found += 1
                duplicate_space = file_size * (len(locations) - 1)
                total_duplicate_space += duplicate_space
                
                # Déterminer le meilleur service pour ce fichier
                best_service = self.choose_best_service_for_file(locations)
                
                # Planifier la déduplication
                self.plan_deduplication(file_hash, locations, best_service)
                
        print(f"  📊 {duplicates_found} fichiers dupliqués trouvés")
        print(f"  💾 Espace dupliqué: {self.format_size(total_duplicate_space)}")
        self.space_recovered += total_duplicate_space
        
    def inventory_files(self, cloud_path):
        """Fait l'inventaire des fichiers d'un chemin cloud"""
        files = {}
        
        try:
            for root, dirs, filenames in os.walk(cloud_path):
                # Limiter la profondeur pour la performance
                level = len(Path(root).relative_to(cloud_path).parts)
                if level > 4:
                    dirs.clear()
                    continue
                    
                # Ignorer certains dossiers
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['System', 'Trash', '__pycache__']]
                
                for filename in filenames[:500]:  # Limiter pour performance
                    if filename.startswith('.'):
                        continue
                        
                    file_path = Path(root) / filename
                    try:
                        stat = file_path.stat()
                        
                        # Calculer le hash pour les fichiers moyens
                        if 1024 < stat.st_size < 100 * 1024 * 1024:  # 1KB à 100MB
                            file_hash = self.calculate_file_hash(file_path)
                            if file_hash:
                                files[file_hash] = {
                                    'path': str(file_path),
                                    'name': filename,
                                    'size': stat.st_size,
                                    'modified': stat.st_mtime,
                                    'relative_path': str(file_path.relative_to(cloud_path))
                                }
                                
                    except Exception:
                        continue
                        
        except Exception:
            pass
            
        return files
        
    def calculate_file_hash(self, file_path):
        """Calcule le hash MD5 d'un fichier"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                # Hash rapide : début + fin du fichier
                chunk = f.read(8192)
                if chunk:
                    hash_md5.update(chunk)
                    
                # Pour les gros fichiers, ajouter la fin
                if file_path.stat().st_size > 64 * 1024:
                    f.seek(-8192, 2)
                    chunk = f.read(8192)
                    if chunk:
                        hash_md5.update(chunk)
                        
            return hash_md5.hexdigest()
        except:
            return None
            
    def choose_best_service_for_file(self, locations):
        """Choisit le meilleur service pour garder un fichier"""
        # Trier par priorité des services
        sorted_locations = sorted(locations, key=lambda x: self.cloud_services[x[0]]['priority'])
        
        # Le service avec la plus haute priorité (plus petit nombre)
        best_service = sorted_locations[0][0]
        
        # Vérifications supplémentaires
        file_path = sorted_locations[0][1]['path']
        
        # Préférer iCloud pour les fichiers Desktop/Documents
        if any(folder in file_path for folder in ['/Desktop/', '/Documents/']):
            for service_name, _ in locations:
                if service_name == 'iCloud Drive':
                    return service_name
                    
        # Préférer Google Drive pour les fichiers Office collaboratifs
        if any(ext in file_path.lower() for ext in ['.gdoc', '.gsheet', '.gslides']):
            for service_name, _ in locations:
                if service_name == 'Google Drive':
                    return service_name
                    
        # Préférer OneDrive pour les fichiers Office 365
        if any(ext in file_path.lower() for ext in ['.docx', '.xlsx', '.pptx']):
            for service_name, _ in locations:
                if service_name == 'OneDrive':
                    return service_name
                    
        return best_service
        
    def plan_deduplication(self, file_hash, locations, best_service):
        """Planifie la déduplication d'un fichier"""
        # Garder le fichier dans le meilleur service, supprimer des autres
        files_to_remove = []
        
        for service_name, file_info in locations:
            if service_name != best_service:
                files_to_remove.append({
                    'service': service_name,
                    'path': file_info['path'],
                    'size': file_info['size']
                })
                
        if files_to_remove:
            action = {
                'type': 'deduplicate_file',
                'file_hash': file_hash,
                'keep_in': best_service,
                'remove_from': files_to_remove,
                'space_saved': sum(f['size'] for f in files_to_remove),
                'description': f"Déduplication: garder dans {best_service}, supprimer de {len(files_to_remove)} autre(s) service(s)"
            }
            
            self.optimization_actions.append(action)
            
    def resolve_cloud_nesting(self):
        """Résout les problèmes d'imbrication de services cloud"""
        print("\n🔧 Résolution des imbrications...")
        
        cloud_paths = []
        for service_name, info in self.cloud_services.items():
            for path in info['paths']:
                cloud_paths.append((service_name, path))
                
        # Détecter les imbrications
        for i, (service1, path1) in enumerate(cloud_paths):
            for j, (service2, path2) in enumerate(cloud_paths):
                if i != j:
                    try:
                        # path2 est-il dans path1 ?
                        relative = path2.relative_to(path1)
                        
                        # C'est une imbrication problématique
                        action = {
                            'type': 'resolve_nesting',
                            'parent_service': service1,
                            'nested_service': service2,
                            'nested_path': str(path2),
                            'new_path': str(self.home_path / f"{service2}_Standalone"),
                            'description': f"Déplacer {service2} hors de {service1}",
                            'space_saved': self.get_directory_size(path2)
                        }
                        
                        self.optimization_actions.append(action)
                        print(f"  🚨 Imbrication détectée: {service2} dans {service1}")
                        
                    except ValueError:
                        continue
                        
    def optimize_system_folders(self):
        """Optimise les dossiers système synchronisés"""
        print("\n🗂️  Optimisation des dossiers système...")
        
        critical_folders = ['Desktop', 'Documents', 'Pictures', 'Downloads']
        
        for folder_name in critical_folders:
            folder_path = self.home_path / folder_name
            if not folder_path.exists():
                continue
                
            syncing_services = []
            
            # Vérifier quels services synchronisent ce dossier
            for service_name, info in self.cloud_services.items():
                for cloud_path in info['paths']:
                    try:
                        folder_path.relative_to(cloud_path)
                        syncing_services.append(service_name)
                    except ValueError:
                        continue
                        
            if len(syncing_services) > 1:
                # Choisir le meilleur service pour ce dossier
                best_service = self.choose_best_service_for_folder(folder_name, syncing_services)
                
                action = {
                    'type': 'optimize_system_folder',
                    'folder': folder_name,
                    'current_services': syncing_services,
                    'recommended_service': best_service,
                    'description': f"Synchroniser {folder_name} uniquement avec {best_service}",
                    'space_saved': self.get_directory_size(folder_path) * (len(syncing_services) - 1)
                }
                
                self.optimization_actions.append(action)
                print(f"  📁 {folder_name} synchronisé par {len(syncing_services)} services → {best_service}")
                
    def choose_best_service_for_folder(self, folder_name, syncing_services):
        """Choisit le meilleur service pour un dossier système"""
        # Règles spécifiques par dossier
        if folder_name in ['Desktop', 'Documents']:
            if 'iCloud Drive' in syncing_services:
                return 'iCloud Drive'  # Préférer iCloud pour Desktop/Documents
        elif folder_name == 'Pictures':
            if 'iCloud Drive' in syncing_services:
                return 'iCloud Drive'  # Préférer iCloud Photos
        elif folder_name == 'Downloads':
            # Downloads ne devrait pas être synchronisé
            return 'NONE'
            
        # Par défaut, prendre le service avec la plus haute priorité
        service_priorities = [(s, self.cloud_services[s]['priority']) for s in syncing_services if s in self.cloud_services]
        return min(service_priorities, key=lambda x: x[1])[0] if service_priorities else syncing_services[0]
        
    def create_optimal_structure(self):
        """Crée une structure optimale pour les services cloud"""
        print("\n🏗️  Création de la structure optimale...")
        
        optimal_structure = {
            'iCloud Drive': {
                'folders': ['Desktop', 'Documents', 'Photos'],
                'description': 'Fichiers personnels et système'
            },
            'Google Drive': {
                'folders': ['Work_Collaboration', 'Shared_Projects', 'Google_Workspace'],
                'description': 'Collaboration et projets partagés'
            },
            'OneDrive': {
                'folders': ['Business_Documents', 'Office365_Files', 'Teams_Projects'],
                'description': 'Documents professionnels Office'
            },
            'Dropbox': {
                'folders': ['Creative_Projects', 'Large_Media', 'External_Sharing'],
                'description': 'Projets créatifs et partage externe'
            }
        }
        
        for service_name, structure in optimal_structure.items():
            if service_name in self.cloud_services:
                action = {
                    'type': 'create_optimal_structure',
                    'service': service_name,
                    'folders': structure['folders'],
                    'description': f"Organiser {service_name}: {structure['description']}",
                    'space_saved': 0  # Pas d'économie directe, mais meilleure organisation
                }
                
                self.optimization_actions.append(action)
                
    def execute_optimizations(self):
        """Exécute les optimisations planifiées"""
        if self.simulation_mode:
            print("\n⚠️  MODE SIMULATION - Aucune modification effectuée")
            return
            
        print(f"\n⚡ Exécution des optimisations...")
        
        executed_actions = 0
        total_space_saved = 0
        
        for action in self.optimization_actions:
            try:
                if action['type'] == 'deduplicate_file':
                    self.execute_file_deduplication(action)
                elif action['type'] == 'resolve_nesting':
                    self.execute_nesting_resolution(action)
                elif action['type'] == 'optimize_system_folder':
                    self.execute_system_folder_optimization(action)
                elif action['type'] == 'create_optimal_structure':
                    self.execute_structure_creation(action)
                    
                executed_actions += 1
                total_space_saved += action.get('space_saved', 0)
                
            except Exception as e:
                print(f"  ❌ Erreur lors de {action['description']}: {e}")
                continue
                
        print(f"\n✅ {executed_actions} optimisations exécutées")
        print(f"💾 Espace total récupéré: {self.format_size(total_space_saved)}")
        
    def execute_file_deduplication(self, action):
        """Exécute la déduplication d'un fichier"""
        for file_to_remove in action['remove_from']:
            file_path = Path(file_to_remove['path'])
            if file_path.exists():
                # Backup puis suppression
                backup_path = self.backup_dir / file_path.name
                shutil.copy2(file_path, backup_path)
                file_path.unlink()
                
    def execute_nesting_resolution(self, action):
        """Exécute la résolution d'imbrication"""
        nested_path = Path(action['nested_path'])
        new_path = Path(action['new_path'])
        
        if nested_path.exists():
            new_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(nested_path), str(new_path))
            
    def execute_system_folder_optimization(self, action):
        """Exécute l'optimisation d'un dossier système"""
        # Créer les exclusions appropriées dans les services non recommandés
        folder_name = action['folder']
        recommended_service = action['recommended_service']
        
        for service in action['current_services']:
            if service != recommended_service:
                print(f"  📝 Exclure {folder_name} de {service} (configuration manuelle requise)")
                
    def execute_structure_creation(self, action):
        """Exécute la création de structure optimale"""
        service_name = action['service']
        service_info = self.cloud_services[service_name]
        
        for cloud_path in service_info['paths']:
            for folder_name in action['folders']:
                folder_path = cloud_path / folder_name
                folder_path.mkdir(exist_ok=True)
                
    def generate_optimization_report(self):
        """Génère le rapport d'optimisation"""
        print(f"\n📊 RAPPORT D'OPTIMISATION DÉDUPLICATION")
        print("=" * 50)
        
        print(f"☁️  Services cloud analysés: {len(self.cloud_services)}")
        total_cloud_space = sum(info['size'] for info in self.cloud_services.values())
        print(f"📦 Espace cloud total: {self.format_size(total_cloud_space)}")
        
        print(f"\n🎯 Actions d'optimisation planifiées: {len(self.optimization_actions)}")
        
        # Grouper par type
        action_types = {}
        for action in self.optimization_actions:
            action_type = action['type']
            if action_type not in action_types:
                action_types[action_type] = []
            action_types[action_type].append(action)
            
        for action_type, actions in action_types.items():
            print(f"\n📋 {action_type.replace('_', ' ').title()}: {len(actions)}")
            total_space = sum(a.get('space_saved', 0) for a in actions)
            if total_space > 0:
                print(f"   💾 Espace récupérable: {self.format_size(total_space)}")
                
            for action in actions[:3]:  # Montrer les 3 premières
                print(f"   • {action['description']}")
                
        print(f"\n💾 ESPACE TOTAL RÉCUPÉRABLE: {self.format_size(self.space_recovered)}")
        
        if self.simulation_mode:
            print(f"\n⚠️  MODE SIMULATION ACTIVÉ")
            print(f"   Pour appliquer les optimisations: modifier simulation_mode = False")
        else:
            print(f"\n📁 Sauvegardes: {self.backup_dir}")
            
        # Recommandations post-optimisation
        print(f"\n💡 RECOMMANDATIONS POST-OPTIMISATION:")
        print("=" * 40)
        print("1. 🔄 Configurer les exclusions dans chaque service cloud")
        print("2. 📱 Vérifier la synchronisation sur tous vos appareils")
        print("3. 🗑️  Vider les corbeilles de chaque service cloud")
        print("4. ⚙️  Activer les modes d'économie d'espace (Files On-Demand, etc.)")
        print("5. 📊 Surveiller l'utilisation d'espace les prochaines semaines")
        print("6. 🔄 Réexécuter cette analyse mensuellement")
        
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
        
    optimizer = CloudDeduplicationOptimizer(home_path)
    
    print("🔄 OPTIMISEUR DE DÉDUPLICATION CLOUD")
    print("Élimination des doublons et imbrications entre services")
    print()
    
    if optimizer.optimize_cloud_deduplication():
        if optimizer.space_recovered > 500 * 1024 * 1024:  # > 500MB
            print(f"\n🎉 EXCELLENT POTENTIEL D'OPTIMISATION!")
            print(f"   {optimizer.format_size(optimizer.space_recovered)} d'espace récupérable")
        else:
            print(f"\n✅ Configuration déjà relativement optimisée")
            
        # Exécuter les optimisations si demandé
        if not optimizer.simulation_mode:
            optimizer.execute_optimizations()
    else:
        print("✅ Aucune optimisation nécessaire")

if __name__ == "__main__":
    main()