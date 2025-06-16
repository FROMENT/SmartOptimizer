#!/usr/bin/env python3
"""
Cloud Nesting Analyzer - Analyse des imbrications entre services cloud
Détecte les problèmes de synchronisation croisée et les doublons d'espace
"""

import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime
import subprocess
import json

class CloudNestingAnalyzer:
    def __init__(self, home_path=None):
        self.home_path = Path(home_path) if home_path else Path.home()
        self.cloud_services = {}
        self.nesting_issues = []
        self.sync_conflicts = []
        self.space_waste = 0
        self.optimization_strategies = []
        
        # Patterns d'imbrication problématiques
        self.problematic_patterns = {
            'cloud_in_cloud': {
                'description': 'Service cloud dans un autre service cloud',
                'severity': 'critique',
                'space_multiplier': 2.0
            },
            'desktop_sync_all': {
                'description': 'Desktop synchronisé par plusieurs services',
                'severity': 'haute',
                'space_multiplier': 1.5
            },
            'documents_everywhere': {
                'description': 'Dossier Documents dans plusieurs clouds',
                'severity': 'haute', 
                'space_multiplier': 1.8
            },
            'recursive_sync': {
                'description': 'Synchronisation récursive (A→B→A)',
                'severity': 'critique',
                'space_multiplier': 3.0
            },
            'backup_in_sync': {
                'description': 'Dossiers de backup dans le cloud sync',
                'severity': 'moyenne',
                'space_multiplier': 1.3
            }
        }
        
    def analyze_cloud_nesting(self):
        """Analyse complète des imbrications cloud"""
        print("🔍 ANALYSE DES IMBRICATIONS CLOUD")
        print("=" * 40)
        
        # 1. Détecter tous les services cloud
        self.detect_all_cloud_services()
        
        # 2. Analyser les imbrications
        self.analyze_nesting_patterns()
        
        # 3. Détecter les doublons d'espace
        self.detect_space_duplication()
        
        # 4. Analyser les conflits de synchronisation
        self.analyze_sync_conflicts()
        
        # 5. Générer les stratégies d'optimisation
        self.generate_optimization_strategies()
        
        # 6. Rapport final
        self.generate_nesting_report()
        
        return len(self.nesting_issues) > 0
        
    def detect_all_cloud_services(self):
        """Détecte tous les services cloud et leurs chemins"""
        print("☁️  Détection des services cloud...")
        
        cloud_definitions = {
            'iCloud Drive': [
                'Library/Mobile Documents/com~apple~CloudDocs',
                'iCloud Drive (Archive)'
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
            ],
            'Desktop (Sync)': [
                'Desktop'
            ],
            'Documents (Sync)': [
                'Documents'
            ]
        }
        
        for service_name, patterns in cloud_definitions.items():
            paths = []
            for pattern in patterns:
                if '*' in pattern:
                    parent = self.home_path / Path(pattern).parent if Path(pattern).parent != '.' else self.home_path
                    if parent.exists():
                        pattern_name = Path(pattern).name.replace('*', '')
                        for item in parent.iterdir():
                            if pattern_name in item.name and item.is_dir():
                                paths.append(item)
                else:
                    full_path = self.home_path / pattern
                    if full_path.exists():
                        paths.append(full_path)
                        
            if paths:
                self.cloud_services[service_name] = {
                    'paths': paths,
                    'is_synced': self.check_if_synced(paths[0]),
                    'size': self.get_directory_size(paths[0]),
                    'file_count': self.get_file_count(paths[0])
                }
                print(f"  ✅ {service_name}: {len(paths)} chemin(s)")
                
    def check_if_synced(self, path):
        """Vérifie si un dossier est synchronisé"""
        # Indicateurs de synchronisation
        sync_indicators = [
            '.icloud', '.tmp', '.gdownload', 
            '.dropbox', '.onedrive', 'desktop.ini'
        ]
        
        try:
            for item in path.iterdir():
                if any(indicator in item.name.lower() for indicator in sync_indicators):
                    return True
                    
            # Vérifier les métadonnées étendues (macOS)
            try:
                result = subprocess.run(['ls', '-la@', str(path)], 
                                      capture_output=True, text=True)
                if 'com.apple.metadata' in result.stdout or 'com.dropbox' in result.stdout:
                    return True
            except:
                pass
                
        except:
            pass
            
        return False
        
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
        
    def get_file_count(self, path):
        """Compte approximativement les fichiers"""
        try:
            count = 0
            for root, dirs, files in os.walk(path):
                count += len(files)
                if count > 10000:  # Limiter pour performance
                    break
            return count
        except:
            return 0
            
    def analyze_nesting_patterns(self):
        """Analyse les patterns d'imbrication problématiques"""
        print("\n🔍 Analyse des patterns d'imbrication...")
        
        # 1. Cloud dans cloud (le pire cas)
        self.detect_cloud_in_cloud()
        
        # 2. Desktop/Documents synchronisés partout
        self.detect_universal_sync_folders()
        
        # 3. Synchronisation récursive
        self.detect_recursive_sync()
        
        # 4. Backups dans le sync
        self.detect_backup_in_sync()
        
        # 5. Dossiers système dans le cloud
        self.detect_system_folders_in_cloud()
        
    def detect_cloud_in_cloud(self):
        """Détecte les services cloud imbriqués dans d'autres"""
        print("  🔍 Recherche de clouds imbriqués...")
        
        cloud_paths = []
        for service_name, info in self.cloud_services.items():
            for path in info['paths']:
                cloud_paths.append((service_name, path))
                
        # Vérifier chaque combinaison
        for i, (service1, path1) in enumerate(cloud_paths):
            for j, (service2, path2) in enumerate(cloud_paths):
                if i != j:
                    # Vérifier si path2 est dans path1
                    try:
                        path2.relative_to(path1)
                        
                        # C'est une imbrication !
                        nested_size = self.get_directory_size(path2)
                        issue = {
                            'type': 'cloud_in_cloud',
                            'parent_service': service1,
                            'nested_service': service2,
                            'parent_path': str(path1),
                            'nested_path': str(path2),
                            'wasted_space': nested_size,
                            'severity': 'critique',
                            'description': f"{service2} imbriqué dans {service1}"
                        }
                        
                        self.nesting_issues.append(issue)
                        self.space_waste += nested_size
                        
                        print(f"    🚨 CRITIQUE: {service2} dans {service1}")
                        print(f"       Espace dupliqué: {self.format_size(nested_size)}")
                        
                    except ValueError:
                        continue
                        
    def detect_universal_sync_folders(self):
        """Détecte Desktop/Documents synchronisés par plusieurs services"""
        print("  🔍 Recherche de dossiers universellement synchronisés...")
        
        critical_folders = ['Desktop', 'Documents', 'Pictures']
        
        for folder_name in critical_folders:
            folder_path = self.home_path / folder_name
            if not folder_path.exists():
                continue
                
            syncing_services = []
            
            # Vérifier quels services synchronisent ce dossier
            for service_name, info in self.cloud_services.items():
                for cloud_path in info['paths']:
                    try:
                        # Le dossier est-il dans un cloud ?
                        folder_path.relative_to(cloud_path)
                        syncing_services.append(service_name)
                    except ValueError:
                        continue
                        
            if len(syncing_services) > 1:
                folder_size = self.get_directory_size(folder_path)
                duplicated_space = folder_size * (len(syncing_services) - 1)
                
                issue = {
                    'type': 'universal_sync',
                    'folder': folder_name,
                    'services': syncing_services,
                    'wasted_space': duplicated_space,
                    'severity': 'haute',
                    'description': f"{folder_name} synchronisé par {len(syncing_services)} services"
                }
                
                self.nesting_issues.append(issue)
                self.space_waste += duplicated_space
                
                print(f"    ⚠️  HAUTE: {folder_name} synchronisé par {syncing_services}")
                print(f"       Espace dupliqué: {self.format_size(duplicated_space)}")
                
    def detect_recursive_sync(self):
        """Détecte les synchronisations récursives (A→B→A)"""
        print("  🔍 Recherche de synchronisations récursives...")
        
        # Construire un graphe des dépendances
        sync_graph = {}
        
        for service_name, info in self.cloud_services.items():
            sync_graph[service_name] = []
            
            for cloud_path in info['paths']:
                # Chercher d'autres services dans ce chemin
                for other_service, other_info in self.cloud_services.items():
                    if other_service != service_name:
                        for other_path in other_info['paths']:
                            try:
                                other_path.relative_to(cloud_path)
                                sync_graph[service_name].append(other_service)
                            except ValueError:
                                continue
                                
        # Détecter les cycles
        def has_cycle(graph, start, visited, path):
            if start in path:
                return path[path.index(start):] + [start]
            if start in visited:
                return None
                
            visited.add(start)
            path.append(start)
            
            for neighbor in graph.get(start, []):
                cycle = has_cycle(graph, neighbor, visited, path.copy())
                if cycle:
                    return cycle
                    
            return None
            
        visited = set()
        for service in sync_graph:
            if service not in visited:
                cycle = has_cycle(sync_graph, service, visited, [])
                if cycle:
                    issue = {
                        'type': 'recursive_sync',
                        'cycle': cycle,
                        'wasted_space': 0,  # Difficile à calculer
                        'severity': 'critique',
                        'description': f"Cycle de sync: {' → '.join(cycle)}"
                    }
                    
                    self.nesting_issues.append(issue)
                    print(f"    🚨 CRITIQUE: Cycle détecté {' → '.join(cycle)}")
                    
    def detect_backup_in_sync(self):
        """Détecte les dossiers de backup dans la synchronisation"""
        print("  🔍 Recherche de backups dans le sync...")
        
        backup_keywords = [
            'backup', 'bak', 'old', 'archive', 'saved', 'copy',
            'time machine', 'backups', 'restore', 'recovery'
        ]
        
        for service_name, info in self.cloud_services.items():
            for cloud_path in info['paths']:
                try:
                    for root, dirs, files in os.walk(cloud_path):
                        # Limiter la profondeur
                        level = len(Path(root).relative_to(cloud_path).parts)
                        if level > 3:
                            dirs.clear()
                            continue
                            
                        for dir_name in dirs:
                            dir_lower = dir_name.lower()
                            if any(keyword in dir_lower for keyword in backup_keywords):
                                backup_path = Path(root) / dir_name
                                backup_size = self.get_directory_size(backup_path)
                                
                                if backup_size > 100 * 1024 * 1024:  # > 100MB
                                    issue = {
                                        'type': 'backup_in_sync',
                                        'service': service_name,
                                        'backup_path': str(backup_path),
                                        'wasted_space': backup_size,
                                        'severity': 'moyenne',
                                        'description': f"Backup '{dir_name}' synchronisé dans {service_name}"
                                    }
                                    
                                    self.nesting_issues.append(issue)
                                    self.space_waste += backup_size
                                    
                                    print(f"    ⚠️  MOYENNE: Backup '{dir_name}' dans {service_name}")
                                    print(f"       Taille: {self.format_size(backup_size)}")
                                    
                except Exception:
                    continue
                    
    def detect_system_folders_in_cloud(self):
        """Détecte les dossiers système dans le cloud"""
        print("  🔍 Recherche de dossiers système dans le cloud...")
        
        system_folders = [
            'Library', 'System', 'Applications', '.Trash',
            'node_modules', '.git', '.svn', '__pycache__',
            '.cache', '.tmp', 'Temp'
        ]
        
        for service_name, info in self.cloud_services.items():
            for cloud_path in info['paths']:
                try:
                    for item in cloud_path.iterdir():
                        if item.is_dir() and item.name in system_folders:
                            system_size = self.get_directory_size(item)
                            
                            if system_size > 50 * 1024 * 1024:  # > 50MB
                                issue = {
                                    'type': 'system_in_cloud',
                                    'service': service_name,
                                    'system_folder': item.name,
                                    'path': str(item),
                                    'wasted_space': system_size,
                                    'severity': 'haute',
                                    'description': f"Dossier système '{item.name}' dans {service_name}"
                                }
                                
                                self.nesting_issues.append(issue)
                                self.space_waste += system_size
                                
                                print(f"    ⚠️  HAUTE: Système '{item.name}' dans {service_name}")
                                print(f"       Taille: {self.format_size(system_size)}")
                                
                except Exception:
                    continue
                    
    def detect_space_duplication(self):
        """Détecte les duplications d'espace entre services"""
        print("\n💾 Analyse des duplications d'espace...")
        
        # Analyser les fichiers identiques entre services
        self.analyze_cross_cloud_duplicates()
        
        # Analyser les structures de dossiers dupliquées
        self.analyze_folder_structure_duplication()
        
    def analyze_cross_cloud_duplicates(self):
        """Analyse les doublons entre services cloud"""
        print("  🔍 Recherche de doublons inter-cloud...")
        
        file_hashes = {}
        
        for service_name, info in self.cloud_services.items():
            for cloud_path in info['paths']:
                try:
                    for root, dirs, files in os.walk(cloud_path):
                        # Limiter pour performance
                        level = len(Path(root).relative_to(cloud_path).parts)
                        if level > 2:
                            dirs.clear()
                            continue
                            
                        for file in files[:100]:  # Échantillon
                            if file.startswith('.'):
                                continue
                                
                            file_path = Path(root) / file
                            try:
                                # Hash rapide pour les petits fichiers
                                if file_path.stat().st_size < 10 * 1024 * 1024:  # < 10MB
                                    file_hash = self.quick_hash(file_path)
                                    if file_hash:
                                        if file_hash not in file_hashes:
                                            file_hashes[file_hash] = []
                                        file_hashes[file_hash].append((service_name, file_path))
                            except:
                                continue
                                
                except Exception:
                    continue
                    
        # Identifier les vrais doublons inter-cloud
        cross_cloud_duplicates = 0
        duplicated_space = 0
        
        for file_hash, locations in file_hashes.items():
            if len(locations) > 1:
                services = set(service for service, path in locations)
                if len(services) > 1:  # Fichier présent dans plusieurs services
                    cross_cloud_duplicates += 1
                    
                    # Calculer l'espace dupliqué
                    file_size = locations[0][1].stat().st_size
                    duplicated_space += file_size * (len(locations) - 1)
                    
        if cross_cloud_duplicates > 0:
            print(f"    📊 {cross_cloud_duplicates} fichiers dupliqués entre services")
            print(f"    💾 Espace dupliqué: {self.format_size(duplicated_space)}")
            self.space_waste += duplicated_space
            
    def analyze_folder_structure_duplication(self):
        """Analyse la duplication des structures de dossiers"""
        print("  🔍 Analyse des structures de dossiers dupliquées...")
        
        folder_structures = {}
        
        for service_name, info in self.cloud_services.items():
            for cloud_path in info['paths']:
                try:
                    structure = []
                    for item in cloud_path.iterdir():
                        if item.is_dir() and not item.name.startswith('.'):
                            structure.append(item.name)
                            
                    structure.sort()
                    structure_key = tuple(structure)
                    
                    if structure_key not in folder_structures:
                        folder_structures[structure_key] = []
                    folder_structures[structure_key].append((service_name, cloud_path))
                    
                except Exception:
                    continue
                    
        # Identifier les structures similaires
        similar_structures = 0
        for structure, services in folder_structures.items():
            if len(services) > 1 and len(structure) > 3:  # Structure significative
                similar_structures += 1
                print(f"    📁 Structure similaire dans {[s[0] for s in services]}")
                
        if similar_structures > 0:
            print(f"    📊 {similar_structures} structures de dossiers similaires détectées")
            
    def analyze_sync_conflicts(self):
        """Analyse les conflits de synchronisation"""
        print("\n⚠️  Analyse des conflits de synchronisation...")
        
        conflict_patterns = [
            'conflicted copy', 'conflict', 'duplicate',
            'case conflict', 'sync conflict'
        ]
        
        total_conflicts = 0
        
        for service_name, info in self.cloud_services.items():
            service_conflicts = 0
            
            for cloud_path in info['paths']:
                try:
                    for root, dirs, files in os.walk(cloud_path):
                        level = len(Path(root).relative_to(cloud_path).parts)
                        if level > 3:
                            dirs.clear()
                            continue
                            
                        for file in files:
                            file_lower = file.lower()
                            if any(pattern in file_lower for pattern in conflict_patterns):
                                service_conflicts += 1
                                total_conflicts += 1
                                
                except Exception:
                    continue
                    
            if service_conflicts > 0:
                print(f"  ⚠️  {service_name}: {service_conflicts} conflits détectés")
                
        if total_conflicts > 0:
            self.sync_conflicts.append({
                'total_conflicts': total_conflicts,
                'description': f"{total_conflicts} fichiers de conflit détectés"
            })
            
    def generate_optimization_strategies(self):
        """Génère les stratégies d'optimisation"""
        print("\n🎯 Génération des stratégies d'optimisation...")
        
        # Stratégies par type de problème
        for issue in self.nesting_issues:
            strategy = self.get_strategy_for_issue(issue)
            if strategy:
                self.optimization_strategies.append(strategy)
                
    def get_strategy_for_issue(self, issue):
        """Génère une stratégie pour un problème spécifique"""
        issue_type = issue['type']
        
        if issue_type == 'cloud_in_cloud':
            return {
                'priority': 'critique',
                'action': 'déplacer_service',
                'description': f"Déplacer {issue['nested_service']} hors de {issue['parent_service']}",
                'space_saving': issue['wasted_space'],
                'steps': [
                    f"1. Arrêter la sync de {issue['nested_service']}",
                    f"2. Déplacer {issue['nested_path']} vers {self.home_path}/{issue['nested_service']}_standalone",
                    f"3. Reconfigurer {issue['nested_service']} sur le nouveau chemin",
                    f"4. Exclure l'ancien chemin de {issue['parent_service']}"
                ]
            }
            
        elif issue_type == 'universal_sync':
            return {
                'priority': 'haute',
                'action': 'choisir_service_principal',
                'description': f"Choisir un service principal pour {issue['folder']}",
                'space_saving': issue['wasted_space'],
                'steps': [
                    f"1. Identifier le service le plus approprié pour {issue['folder']}",
                    f"2. Exclure {issue['folder']} des autres services",
                    f"3. Migrer les fichiers uniques vers le service principal",
                    f"4. Créer des liens symboliques si nécessaire"
                ]
            }
            
        elif issue_type == 'backup_in_sync':
            return {
                'priority': 'moyenne',
                'action': 'déplacer_backup',
                'description': f"Déplacer les backups hors du sync",
                'space_saving': issue['wasted_space'],
                'steps': [
                    f"1. Créer un dossier Backups local (non synchronisé)",
                    f"2. Déplacer {issue['backup_path']} vers le dossier local",
                    f"3. Mettre à jour les scripts de backup",
                    f"4. Exclure les nouveaux chemins de backup du sync"
                ]
            }
            
        elif issue_type == 'system_in_cloud':
            return {
                'priority': 'haute', 
                'action': 'exclure_systeme',
                'description': f"Exclure {issue['system_folder']} du sync cloud",
                'space_saving': issue['wasted_space'],
                'steps': [
                    f"1. Ajouter {issue['system_folder']} aux exclusions du service",
                    f"2. Supprimer {issue['system_folder']} du cloud après backup",
                    f"3. Vérifier que les applications fonctionnent toujours",
                    f"4. Configurer .gitignore ou équivalent si nécessaire"
                ]
            }
            
        return None
        
    def generate_nesting_report(self):
        """Génère le rapport final des imbrications"""
        print(f"\n📊 RAPPORT D'ANALYSE DES IMBRICATIONS")
        print("=" * 45)
        
        print(f"☁️  Services cloud détectés: {len(self.cloud_services)}")
        for service, info in self.cloud_services.items():
            total_size = sum(self.get_directory_size(p) for p in info['paths'])
            print(f"   • {service}: {self.format_size(total_size)}")
            
        print(f"\n🚨 Problèmes d'imbrication détectés: {len(self.nesting_issues)}")
        
        # Grouper par sévérité
        by_severity = {'critique': [], 'haute': [], 'moyenne': []}
        for issue in self.nesting_issues:
            severity = issue.get('severity', 'moyenne')
            by_severity[severity].append(issue)
            
        for severity, issues in by_severity.items():
            if issues:
                print(f"\n🔴 Sévérité {severity.upper()}: {len(issues)} problème(s)")
                for issue in issues[:5]:  # Limiter l'affichage
                    print(f"   • {issue['description']}")
                    if issue.get('wasted_space', 0) > 0:
                        print(f"     💾 Espace gaspillé: {self.format_size(issue['wasted_space'])}")
                        
        print(f"\n💾 ESPACE TOTAL GASPILLÉ: {self.format_size(self.space_waste)}")
        
        if self.sync_conflicts:
            print(f"⚠️  Conflits de sync: {sum(c['total_conflicts'] for c in self.sync_conflicts)}")
            
        print(f"\n🎯 STRATÉGIES D'OPTIMISATION: {len(self.optimization_strategies)}")
        
        # Trier par priorité et économie d'espace
        sorted_strategies = sorted(
            self.optimization_strategies,
            key=lambda s: (
                {'critique': 3, 'haute': 2, 'moyenne': 1}[s['priority']],
                s.get('space_saving', 0)
            ),
            reverse=True
        )
        
        for i, strategy in enumerate(sorted_strategies[:10], 1):
            print(f"\n{i}. {strategy['description']} [{strategy['priority'].upper()}]")
            if strategy.get('space_saving', 0) > 0:
                print(f"   💾 Économie: {self.format_size(strategy['space_saving'])}")
            print(f"   📋 Étapes:")
            for step in strategy['steps'][:3]:
                print(f"      {step}")
            if len(strategy['steps']) > 3:
                print(f"      ... et {len(strategy['steps']) - 3} autres étapes")
                
        # Recommandations générales
        print(f"\n💡 RECOMMANDATIONS GÉNÉRALES:")
        print("=" * 35)
        print("1. 🎯 Définir un service cloud principal par type de contenu")
        print("2. 📁 Exclure Desktop/Documents des services secondaires") 
        print("3. 🔄 Éviter la synchronisation croisée entre services")
        print("4. 🗑️  Déplacer les backups vers un stockage local")
        print("5. ⚙️  Configurer les exclusions appropriées")
        print("6. 📊 Monitorer régulièrement les duplications")
        
        if self.space_waste > 1024**3:  # > 1GB
            print(f"\n🎉 POTENTIEL D'ÉCONOMIE ÉLEVÉ!")
            print(f"   En résolvant ces imbrications, vous pourriez libérer")
            print(f"   {self.format_size(self.space_waste)} d'espace de stockage cloud")
            
    def quick_hash(self, file_path):
        """Calcule un hash rapide d'un fichier"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                # Lire seulement le début et la fin pour les gros fichiers
                chunk = f.read(8192)
                if chunk:
                    hash_md5.update(chunk)
                    if file_path.stat().st_size > 1024*1024:  # > 1MB
                        f.seek(-8192, 2)  # Aller à la fin
                        chunk = f.read(8192)
                        if chunk:
                            hash_md5.update(chunk)
            return hash_md5.hexdigest()[:16]
        except:
            return None
            
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
        
    analyzer = CloudNestingAnalyzer(home_path)
    
    print("🔍 ANALYSEUR D'IMBRICATIONS CLOUD")
    print("Détection des doublons et gaspillages d'espace")
    print()
    
    if analyzer.analyze_cloud_nesting():
        if analyzer.space_waste > 100 * 1024 * 1024:  # > 100MB
            print(f"\n⚠️  ATTENTION: {analyzer.format_size(analyzer.space_waste)} d'espace gaspillé détecté!")
            print("   Consultez les stratégies d'optimisation ci-dessus")
        else:
            print(f"\n✅ Configuration cloud relativement optimisée")
    else:
        print("✅ Aucun problème d'imbrication majeur détecté")

if __name__ == "__main__":
    main()