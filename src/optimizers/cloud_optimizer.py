#!/usr/bin/env python3
"""
Cloud Optimizer - Optimiseur spécialisé pour les services cloud
Optimise iCloud, OneDrive, Google Drive avec stratégies spécifiques
"""

import os
import sys
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
import subprocess
import json

class CloudOptimizer:
    def __init__(self, cloud_path):
        self.cloud_path = Path(cloud_path)
        self.cloud_service = self.detect_cloud_service()
        self.backup_dir = Path.home() / "SmartOptimizer_Backups" / "cloud_optimization" / datetime.now().strftime('%Y%m%d_%H%M%S')
        self.simulation_mode = True
        self.stats = {
            'files_analyzed': 0,
            'duplicates_found': 0,
            'large_files_found': 0,
            'old_files_found': 0,
            'space_recoverable': 0,
            'optimization_actions': []
        }
        
    def detect_cloud_service(self):
        """Détecte le type de service cloud"""
        path_str = str(self.cloud_path).lower()
        
        if 'icloud' in path_str or 'mobile documents' in path_str:
            return 'icloud'
        elif 'google' in path_str or 'googledrive' in path_str:
            return 'google_drive'
        elif 'onedrive' in path_str:
            return 'onedrive'
        elif 'dropbox' in path_str:
            return 'dropbox'
        elif 'box' in path_str:
            return 'box'
        else:
            return 'generic'
            
    def optimize_cloud_storage(self):
        """Optimise le stockage cloud avec stratégies spécifiques"""
        print(f"☁️  OPTIMISATION CLOUD: {self.cloud_service.upper()}")
        print(f"📁 Chemin: {self.cloud_path}")
        print("=" * 60)
        
        if not self.cloud_path.exists():
            print(f"❌ Chemin cloud inexistant: {self.cloud_path}")
            return False
            
        # Créer le répertoire de backup
        if not self.simulation_mode:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            
        # 1. Analyse initiale
        self.analyze_cloud_content()
        
        # 2. Optimisations spécifiques au service
        self.apply_service_specific_optimizations()
        
        # 3. Optimisations génériques
        self.apply_generic_optimizations()
        
        # 4. Rapport final
        self.generate_optimization_report()
        
        return True
        
    def analyze_cloud_content(self):
        """Analyse le contenu du dossier cloud"""
        print("🔍 Analyse du contenu cloud...")
        
        duplicates = {}
        large_files = []
        old_files = []
        
        for root, dirs, files in os.walk(self.cloud_path):
            # Ignorer les dossiers système
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['System', 'Trash']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = Path(root) / file
                self.stats['files_analyzed'] += 1
                
                try:
                    stat = file_path.stat()
                    size = stat.st_size
                    mtime = datetime.fromtimestamp(stat.st_mtime)
                    
                    # Détecter les gros fichiers (>100MB)
                    if size > 100 * 1024 * 1024:
                        large_files.append({
                            'path': file_path,
                            'size': size,
                            'modified': mtime
                        })
                        
                    # Détecter les vieux fichiers (>2 ans)
                    if mtime < datetime.now() - timedelta(days=730):
                        old_files.append({
                            'path': file_path,
                            'size': size,
                            'modified': mtime
                        })
                        
                    # Détecter les doublons potentiels
                    if size < 50 * 1024 * 1024:  # Seulement pour fichiers <50MB
                        file_hash = self.calculate_file_hash(file_path)
                        if file_hash:
                            if file_hash not in duplicates:
                                duplicates[file_hash] = []
                            duplicates[file_hash].append(file_path)
                            
                except Exception as e:
                    continue
                    
        # Traiter les résultats
        self.process_analysis_results(duplicates, large_files, old_files)
        
    def calculate_file_hash(self, file_path):
        """Calcule le hash MD5 d'un fichier (pour les petits fichiers)"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                chunk = f.read(8192)  # Lire seulement le début pour les gros fichiers
                if chunk:
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()[:16]  # Hash court
        except:
            return None
            
    def process_analysis_results(self, duplicates, large_files, old_files):
        """Traite les résultats de l'analyse"""
        
        # Doublons
        real_duplicates = {k: v for k, v in duplicates.items() if len(v) > 1}
        self.stats['duplicates_found'] = len(real_duplicates)
        
        if real_duplicates:
            print(f"  🔄 {len(real_duplicates)} groupes de doublons trouvés")
            for file_hash, files in list(real_duplicates.items())[:5]:
                print(f"     • {len(files)} copies de {files[0].name}")
                
        # Gros fichiers
        self.stats['large_files_found'] = len(large_files)
        if large_files:
            print(f"  📦 {len(large_files)} fichiers volumineux (>100MB)")
            for large_file in large_files[:5]:
                size_mb = large_file['size'] / (1024 * 1024)
                print(f"     • {large_file['path'].name} ({size_mb:.1f}MB)")
                
        # Vieux fichiers
        self.stats['old_files_found'] = len(old_files)
        if old_files:
            print(f"  📅 {len(old_files)} fichiers anciens (>2 ans)")
            
        # Stocker pour optimisation
        self.duplicates = real_duplicates
        self.large_files = large_files
        self.old_files = old_files
        
    def apply_service_specific_optimizations(self):
        """Applique les optimisations spécifiques au service cloud"""
        print(f"\n⚡ Optimisations spécifiques {self.cloud_service}...")
        
        if self.cloud_service == 'icloud':
            self.optimize_icloud()
        elif self.cloud_service == 'google_drive':
            self.optimize_google_drive()
        elif self.cloud_service == 'onedrive':
            self.optimize_onedrive()
        elif self.cloud_service == 'dropbox':
            self.optimize_dropbox()
        else:
            self.optimize_generic_cloud()
            
    def optimize_icloud(self):
        """Optimisations spécifiques iCloud"""
        
        # 1. Organiser par type dans des dossiers appropriés
        self.organize_icloud_structure()
        
        # 2. Identifier les fichiers .icloud non téléchargés
        self.handle_icloud_placeholders()
        
        # 3. Optimiser les photos (si dossier Photos détecté)
        self.optimize_icloud_photos()
        
    def organize_icloud_structure(self):
        """Organise la structure iCloud Drive"""
        suggested_structure = {
            'Documents_Active': ['doc', 'docx', 'pdf', 'txt', 'pages'],
            'Spreadsheets': ['xls', 'xlsx', 'numbers', 'csv'],
            'Presentations': ['ppt', 'pptx', 'key'],
            'Images_Graphics': ['jpg', 'png', 'gif', 'psd', 'ai'],
            'Archive_Old': []  # Pour les vieux fichiers
        }
        
        print("  🗂️  Organisation de la structure iCloud...")
        
        for folder_name, extensions in suggested_structure.items():
            folder_path = self.cloud_path / folder_name
            
            if extensions:  # Dossiers par type
                files_to_move = []
                for ext in extensions:
                    files_to_move.extend(self.cloud_path.glob(f"*.{ext}"))
                    files_to_move.extend(self.cloud_path.glob(f"*.{ext.upper()}"))
                    
                if files_to_move:
                    action = f"Créer {folder_name} et déplacer {len(files_to_move)} fichiers {extensions}"
                    self.stats['optimization_actions'].append(action)
                    print(f"     📁 {action}")
                    
                    if not self.simulation_mode:
                        folder_path.mkdir(exist_ok=True)
                        for file_path in files_to_move:
                            try:
                                shutil.move(str(file_path), str(folder_path / file_path.name))
                            except:
                                continue
                                
    def handle_icloud_placeholders(self):
        """Gère les fichiers .icloud (placeholders)"""
        icloud_files = list(self.cloud_path.rglob("*.icloud"))
        
        if icloud_files:
            print(f"  ☁️  {len(icloud_files)} fichiers iCloud non téléchargés")
            
            large_placeholders = []
            for placeholder in icloud_files:
                original_name = placeholder.name.replace('.icloud', '')
                # Estimer la taille depuis le nom si possible
                large_placeholders.append(placeholder)
                
            if large_placeholders:
                action = f"Identifier {len(large_placeholders)} placeholders à télécharger ou archiver"
                self.stats['optimization_actions'].append(action)
                print(f"     📥 {action}")
                
    def optimize_icloud_photos(self):
        """Optimise les photos iCloud"""
        photos_folders = ['Photos', 'Pictures', 'Images']
        
        for folder_name in photos_folders:
            photos_path = self.cloud_path / folder_name
            if photos_path.exists():
                print(f"  📸 Optimisation du dossier {folder_name}...")
                
                # Détecter les formats inefficaces
                inefficient_formats = list(photos_path.glob("*.bmp")) + list(photos_path.glob("*.tiff"))
                
                if inefficient_formats:
                    action = f"Convertir {len(inefficient_formats)} images vers JPEG pour économiser l'espace"
                    self.stats['optimization_actions'].append(action)
                    print(f"     🔄 {action}")
                    
    def optimize_google_drive(self):
        """Optimisations spécifiques Google Drive"""
        
        # 1. Identifier les Google Docs natifs vs fichiers uploadés
        self.optimize_google_native_files()
        
        # 2. Organiser par projet/client
        self.organize_google_drive_structure()
        
        # 3. Gérer les fichiers partagés
        self.optimize_google_shared_files()
        
    def optimize_google_native_files(self):
        """Optimise les fichiers Google natifs"""
        google_extensions = ['.gdoc', '.gsheet', '.gslides', '.gdraw']
        
        native_files = []
        for ext in google_extensions:
            native_files.extend(self.cloud_path.rglob(f"*{ext}"))
            
        if native_files:
            print(f"  📝 {len(native_files)} fichiers Google natifs (optimaux)")
            
        # Identifier les fichiers Word/Excel qui pourraient être convertis
        convertible_files = list(self.cloud_path.rglob("*.docx")) + list(self.cloud_path.rglob("*.xlsx"))
        
        if convertible_files:
            action = f"Convertir {len(convertible_files)} fichiers Office en Google Docs pour économiser l'espace"
            self.stats['optimization_actions'].append(action)
            print(f"     🔄 {action}")
            
    def organize_google_drive_structure(self):
        """Organise la structure Google Drive"""
        suggested_structure = {
            'Active_Projects': [],
            'Shared_With_Me': [],
            'Archive_Completed': [],
            'Personal_Documents': []
        }
        
        print("  🗂️  Organisation Google Drive par projets...")
        
        # Détecter les dossiers projet (contenant beaucoup de fichiers)
        project_folders = []
        for item in self.cloud_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                file_count = len(list(item.iterdir())[:100])  # Échantillon
                if file_count > 10:
                    project_folders.append(item)
                    
        if project_folders:
            action = f"Organiser {len(project_folders)} dossiers projets dans une structure claire"
            self.stats['optimization_actions'].append(action)
            print(f"     📁 {action}")
            
    def optimize_google_shared_files(self):
        """Optimise les fichiers partagés Google"""
        # Note: Détection basique car les métadonnées de partage ne sont pas accessibles via filesystem
        print("  🔗 Recommandation: Vérifier les fichiers partagés dans l'interface Google Drive")
        
        action = "Réviser les permissions de partage et nettoyer les anciens partages"
        self.stats['optimization_actions'].append(action)
        
    def optimize_onedrive(self):
        """Optimisations spécifiques OneDrive"""
        
        # 1. Organiser par type Office
        self.optimize_office_files()
        
        # 2. Gérer les fichiers volumineux
        self.optimize_onedrive_large_files()
        
        # 3. Structure professionnelle
        self.organize_onedrive_business_structure()
        
    def optimize_office_files(self):
        """Optimise les fichiers Office dans OneDrive"""
        office_files = {
            'Word': list(self.cloud_path.rglob("*.docx")) + list(self.cloud_path.rglob("*.doc")),
            'Excel': list(self.cloud_path.rglob("*.xlsx")) + list(self.cloud_path.rglob("*.xls")),
            'PowerPoint': list(self.cloud_path.rglob("*.pptx")) + list(self.cloud_path.rglob("*.ppt"))
        }
        
        for app_name, files in office_files.items():
            if files:
                print(f"  📊 {len(files)} fichiers {app_name}")
                
                # Identifier les versions temporaires et de récupération
                temp_files = [f for f in files if '~$' in f.name or 'AutoRecovery' in f.name]
                
                if temp_files:
                    action = f"Nettoyer {len(temp_files)} fichiers temporaires {app_name}"
                    self.stats['optimization_actions'].append(action)
                    print(f"     🧹 {action}")
                    
    def optimize_onedrive_large_files(self):
        """Optimise les gros fichiers OneDrive"""
        if self.large_files:
            print(f"  📦 Gestion des {len(self.large_files)} gros fichiers...")
            
            # Catégoriser par type
            videos = [f for f in self.large_files if f['path'].suffix.lower() in ['.mp4', '.avi', '.mov']]
            archives = [f for f in self.large_files if f['path'].suffix.lower() in ['.zip', '.rar', '.7z']]
            
            if videos:
                action = f"Considérer compression ou archivage de {len(videos)} vidéos volumineuses"
                self.stats['optimization_actions'].append(action)
                print(f"     🎬 {action}")
                
            if archives:
                action = f"Réviser la nécessité de {len(archives)} archives volumineuses"
                self.stats['optimization_actions'].append(action)
                print(f"     📦 {action}")
                
    def organize_onedrive_business_structure(self):
        """Organise OneDrive avec une structure professionnelle"""
        business_structure = {
            'Current_Projects': [],
            'Client_Documents': [],
            'Templates_Resources': [],
            'Archive_Completed': [],
            'Personal_Workspace': []
        }
        
        print("  💼 Organisation structure professionnelle...")
        
        # Détecter les fichiers qui sembleraient être des templates
        potential_templates = []
        for file_path in self.cloud_path.rglob("*template*"):
            potential_templates.append(file_path)
        for file_path in self.cloud_path.rglob("*model*"):
            potential_templates.append(file_path)
            
        if potential_templates:
            action = f"Organiser {len(potential_templates)} templates dans un dossier dédié"
            self.stats['optimization_actions'].append(action)
            print(f"     📋 {action}")
            
    def optimize_dropbox(self):
        """Optimisations spécifiques Dropbox"""
        
        # 1. Gérer les conflits de version
        self.resolve_dropbox_conflicts()
        
        # 2. Optimiser la structure par projet
        self.organize_dropbox_projects()
        
        # 3. Gérer les fichiers partagés
        self.optimize_dropbox_sharing()
        
    def resolve_dropbox_conflicts(self):
        """Résout les conflits de version Dropbox"""
        conflict_files = list(self.cloud_path.rglob("* (Conflicted copy *"))
        conflict_files.extend(self.cloud_path.rglob("* (Case Conflict*)"))
        
        if conflict_files:
            print(f"  ⚠️  {len(conflict_files)} conflits de version détectés")
            
            action = f"Résoudre {len(conflict_files)} conflits de version Dropbox"
            self.stats['optimization_actions'].append(action)
            print(f"     🔧 {action}")
            
            # Calculer l'espace récupérable
            total_conflict_size = 0
            for conflict_file in conflict_files:
                try:
                    total_conflict_size += conflict_file.stat().st_size
                except:
                    continue
                    
            if total_conflict_size > 0:
                self.stats['space_recoverable'] += total_conflict_size
                print(f"     💾 Espace récupérable: {self.format_size(total_conflict_size)}")
                
    def optimize_dropbox_projects(self):
        """Optimise l'organisation des projets Dropbox"""
        print("  📁 Organisation des projets Dropbox...")
        
        # Détecter les dossiers projet actifs vs anciens
        project_folders = []
        for item in self.cloud_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Vérifier la date de dernière modification
                try:
                    latest_mtime = max(f.stat().st_mtime for f in item.rglob("*") if f.is_file())
                    last_modified = datetime.fromtimestamp(latest_mtime)
                    
                    if last_modified < datetime.now() - timedelta(days=180):  # 6 mois
                        project_folders.append(('archive', item))
                    else:
                        project_folders.append(('active', item))
                except:
                    project_folders.append(('unknown', item))
                    
        archive_candidates = [p for status, p in project_folders if status == 'archive']
        
        if archive_candidates:
            action = f"Archiver {len(archive_candidates)} projets inactifs depuis >6 mois"
            self.stats['optimization_actions'].append(action)
            print(f"     📦 {action}")
            
    def optimize_dropbox_sharing(self):
        """Optimise les fichiers partagés Dropbox"""
        # Détecter les gros fichiers qui pourraient être des liens
        large_shared_candidates = [f for f in self.large_files if f['size'] > 500 * 1024 * 1024]  # >500MB
        
        if large_shared_candidates:
            action = f"Convertir {len(large_shared_candidates)} gros fichiers en liens partagés"
            self.stats['optimization_actions'].append(action)
            print(f"     🔗 {action}")
            
    def optimize_generic_cloud(self):
        """Optimisations génériques pour services cloud inconnus"""
        print("  🔧 Optimisations génériques...")
        
        # Organisation basique par type
        self.organize_generic_structure()
        
    def organize_generic_structure(self):
        """Organisation générique par type de fichier"""
        file_categories = {
            'Documents': ['pdf', 'doc', 'docx', 'txt', 'rtf'],
            'Spreadsheets': ['xls', 'xlsx', 'csv'],
            'Presentations': ['ppt', 'pptx'],
            'Images': ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
            'Videos': ['mp4', 'avi', 'mov', 'mkv'],
            'Archives': ['zip', 'rar', '7z', 'tar']
        }
        
        for category, extensions in file_categories.items():
            files_in_category = []
            for ext in extensions:
                files_in_category.extend(self.cloud_path.glob(f"*.{ext}"))
                files_in_category.extend(self.cloud_path.glob(f"*.{ext.upper()}"))
                
            if files_in_category:
                action = f"Organiser {len(files_in_category)} fichiers dans le dossier {category}"
                self.stats['optimization_actions'].append(action)
                print(f"     📁 {action}")
                
    def apply_generic_optimizations(self):
        """Applique les optimisations génériques"""
        print("\n🧹 Optimisations génériques...")
        
        # 1. Traiter les doublons
        self.handle_duplicates()
        
        # 2. Gérer les vieux fichiers
        self.handle_old_files()
        
        # 3. Nettoyer les fichiers temporaires
        self.clean_temporary_files()
        
    def handle_duplicates(self):
        """Gère les fichiers dupliqués"""
        if hasattr(self, 'duplicates') and self.duplicates:
            print(f"  🔄 Traitement de {len(self.duplicates)} groupes de doublons...")
            
            total_recoverable = 0
            for file_hash, files in self.duplicates.items():
                if len(files) > 1:
                    # Garder le plus récent, supprimer les autres
                    files_sorted = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)
                    best_file = files_sorted[0]
                    duplicates_to_remove = files_sorted[1:]
                    
                    for dup_file in duplicates_to_remove:
                        try:
                            file_size = dup_file.stat().st_size
                            total_recoverable += file_size
                            
                            if not self.simulation_mode:
                                # Backup puis suppression
                                backup_path = self.backup_dir / dup_file.name
                                shutil.copy2(dup_file, backup_path)
                                dup_file.unlink()
                                
                        except:
                            continue
                            
            if total_recoverable > 0:
                self.stats['space_recoverable'] += total_recoverable
                action = f"Supprimer doublons - Espace récupérable: {self.format_size(total_recoverable)}"
                self.stats['optimization_actions'].append(action)
                print(f"     💾 {action}")
                
    def handle_old_files(self):
        """Gère les vieux fichiers"""
        if hasattr(self, 'old_files') and self.old_files:
            print(f"  📅 Traitement de {len(self.old_files)} fichiers anciens...")
            
            # Proposer archivage plutôt que suppression
            archive_folder = self.cloud_path / "Archive_Old_Files"
            
            total_old_size = sum(f['size'] for f in self.old_files)
            
            action = f"Archiver {len(self.old_files)} fichiers anciens ({self.format_size(total_old_size)})"
            self.stats['optimization_actions'].append(action)
            print(f"     📦 {action}")
            
            if not self.simulation_mode:
                archive_folder.mkdir(exist_ok=True)
                for old_file in self.old_files[:10]:  # Limiter pour la sécurité
                    try:
                        shutil.move(str(old_file['path']), str(archive_folder / old_file['path'].name))
                    except:
                        continue
                        
    def clean_temporary_files(self):
        """Nettoie les fichiers temporaires"""
        temp_patterns = ['*.tmp', '*.temp', '~$*', '.DS_Store', 'Thumbs.db', '*.bak']
        
        temp_files = []
        for pattern in temp_patterns:
            temp_files.extend(self.cloud_path.rglob(pattern))
            
        if temp_files:
            print(f"  🗑️  {len(temp_files)} fichiers temporaires trouvés")
            
            total_temp_size = 0
            for temp_file in temp_files:
                try:
                    total_temp_size += temp_file.stat().st_size
                    
                    if not self.simulation_mode:
                        temp_file.unlink()
                        
                except:
                    continue
                    
            if total_temp_size > 0:
                self.stats['space_recoverable'] += total_temp_size
                action = f"Supprimer fichiers temporaires - Espace récupéré: {self.format_size(total_temp_size)}"
                self.stats['optimization_actions'].append(action)
                print(f"     🗑️  {action}")
                
    def generate_optimization_report(self):
        """Génère le rapport d'optimisation"""
        print(f"\n📊 RAPPORT D'OPTIMISATION CLOUD")
        print("=" * 40)
        
        print(f"☁️  Service: {self.cloud_service.upper()}")
        print(f"📁 Chemin: {self.cloud_path}")
        print(f"📄 Fichiers analysés: {self.stats['files_analyzed']}")
        print(f"🔄 Groupes de doublons: {self.stats['duplicates_found']}")
        print(f"📦 Fichiers volumineux: {self.stats['large_files_found']}")
        print(f"📅 Fichiers anciens: {self.stats['old_files_found']}")
        print(f"💾 Espace récupérable: {self.format_size(self.stats['space_recoverable'])}")
        
        print(f"\n🎯 ACTIONS D'OPTIMISATION ({len(self.stats['optimization_actions'])}):")
        for i, action in enumerate(self.stats['optimization_actions'], 1):
            print(f"  {i:2d}. {action}")
            
        if self.simulation_mode:
            print(f"\n⚠️  MODE SIMULATION - Aucune modification effectuée")
            print(f"   Pour appliquer les optimisations: modifier simulation_mode = False")
        else:
            print(f"\n✅ Optimisations appliquées")
            print(f"   Sauvegarde: {self.backup_dir}")
            
    def format_size(self, size_bytes):
        """Formate une taille en bytes"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 cloud_optimizer.py <cloud_directory>")
        print("Examples:")
        print("  python3 cloud_optimizer.py ~/Library/Mobile\\ Documents/com~apple~CloudDocs")
        print("  python3 cloud_optimizer.py ~/OneDrive")
        print("  python3 cloud_optimizer.py ~/Dropbox")
        sys.exit(1)
        
    cloud_path = sys.argv[1]
    if not os.path.exists(cloud_path):
        print(f"❌ Répertoire cloud inexistant: {cloud_path}")
        sys.exit(1)
        
    optimizer = CloudOptimizer(cloud_path)
    
    print("🔒 MODE SIMULATION ACTIVÉ")
    print("   Les optimisations seront simulées sans modifications réelles")
    print()
    
    if optimizer.optimize_cloud_storage():
        print(f"\n🎉 Optimisation terminée!")
        if optimizer.stats['space_recoverable'] > 0:
            print(f"💾 Espace total récupérable: {optimizer.format_size(optimizer.stats['space_recoverable'])}")
    else:
        print("❌ Erreur durant l'optimisation")
        sys.exit(1)

if __name__ == "__main__":
    main()