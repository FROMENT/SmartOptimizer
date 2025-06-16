#!/usr/bin/env python3
"""
Smart Reorganizer - Réorganisation intelligente des fichiers isolés
Ventile automatiquement vers une arborescence logique sans casser l'existant
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json
import sys
import mimetypes
import re

class SmartReorganizer:
    def __init__(self, target_path):
        self.target_path = Path(target_path)
        self.proposed_structure = self.define_smart_structure()
        self.analysis_results = {
            'orphan_files': [],
            'safe_moves': [],
            'conflicts': [],
            'stats': {
                'total_files': 0,
                'orphans_found': 0,
                'moves_proposed': 0,
                'conflicts_detected': 0
            }
        }
        
    def define_smart_structure(self):
        """Structure intelligente proposée"""
        return {
            # Documents par type et importance
            'Documents': {
                'path': 'Documents',
                'Official_Papers': {
                    'Identity_Documents': ['passport*', 'carte*identite*', '*cni*', '*identity*'],
                    'Financial_Records': ['*bank*', '*finance*', '*compte*', '*releve*', '*facture*', '*invoice*'],
                    'Tax_Documents': ['*impot*', '*tax*', '*fiscal*', '*avis*'],
                    'Property_Documents': ['*propriete*', '*copropriete*', '*syndic*', '*immeuble*', '*ag_*'],
                    'Insurance': ['*assurance*', '*insurance*', '*attestation*'],
                    'Medical': ['*medical*', '*sante*', '*health*', '*ordonnance*']
                },
                'Work_Professional': {
                    'Contracts': ['*contrat*', '*contract*', '*emploi*'],
                    'Payslips': ['*bulletin*paie*', '*salaire*', '*payslip*'],
                    'CV_Resume': ['*cv*', '*resume*', '*curriculum*'],
                    'Certifications': ['*certification*', '*diplome*', '*certificate*']
                },
                'Personal': {
                    'Correspondence': ['*lettre*', '*courrier*', '*mail*'],
                    'Travel': ['*voyage*', '*travel*', '*ticket*', '*booking*', '*hotel*'],
                    'Education': ['*cours*', '*formation*', '*education*', '*lesson*']
                }
            },
            
            # Média organisé par type et date
            'Media': {
                'path': 'Media',
                'Photos': {
                    'Travel': ['*travel*', '*voyage*', '*vacation*', '*trip*', '*bali*', '*taiwan*'],
                    'Events': ['*event*', '*fete*', '*celebration*', '*party*'],
                    'Work': ['*work*', '*bureau*', '*meeting*', '*conference*'],
                    'Personal': ['*family*', '*famille*', '*perso*', '*home*'],
                    'Screenshots': ['*screenshot*', '*capture*', '*screen*']
                },
                'Videos': {
                    'Content_Creation': ['*youtube*', '*content*', '*creation*', '*tiktok*'],
                    'Travel_Videos': ['*travel*', '*voyage*', '*trip*'],
                    'Tutorials': ['*tutorial*', '*tuto*', '*how*to*', '*guide*'],
                    'Personal': ['*perso*', '*family*', '*home*']
                },
                'Audio': {
                    'Music': ['*music*', '*musique*', '*song*', '*chanson*'],
                    'Podcasts': ['*podcast*', '*interview*', '*radio*'],
                    'Recordings': ['*recording*', '*enregistrement*', '*voice*'],
                    'Effects': ['*effect*', '*sound*', '*fx*', '*meditation*']
                }
            },
            
            # Projets et développement
            'Projects': {
                'path': 'Projects',
                'Development': {
                    'Web_Projects': ['*web*', '*site*', '*html*', '*css*', '*js*'],
                    'AI_ML': ['*ai*', '*ml*', '*neural*', '*model*', '*gpt*'],
                    'Mobile_Apps': ['*app*', '*mobile*', '*android*', '*ios*'],
                    'Scripts': ['*script*', '*automation*', '*tool*']
                },
                'Creative': {
                    'Brand_TUNETOO': ['*tunetoo*', '*brand*', '*logo*', '*design*'],
                    'Content_Creation': ['*youtube*', '*social*', '*content*'],
                    'Graphics_Design': ['*design*', '*graphic*', '*logo*', '*art*']
                },
                'Business': {
                    'Consulting': ['*consulting*', '*client*', '*proposal*'],
                    'Presentations': ['*presentation*', '*slide*', '*pitch*']
                }
            },
            
            # Archives par année
            'Archives': {
                'path': 'Archives',
                'By_Year': {
                    '2024': ['*2024*'],
                    '2023': ['*2023*'],
                    '2022': ['*2022*'],
                    '2021': ['*2021*'],
                    'Older': ['*2020*', '*2019*', '*2018*', '*2017*', '*2016*']
                }
            },
            
            # Utilitaires et outils
            'Tools_Utilities': {
                'path': 'Tools',
                'Software': ['*.dmg', '*.pkg', '*.zip', '*.tar', '*.gz'],
                'Scripts': ['*.sh', '*.py', '*.js', '*.pl'],
                'Configurations': ['*.conf', '*.config', '*.json', '*.yaml', '*.yml'],
                'Documentation': ['*readme*', '*manual*', '*guide*', '*doc*']
            }
        }
        
    def analyze_current_structure(self):
        """Analyse la structure actuelle pour éviter les conflits"""
        self.log("🔍 Analyse de la structure existante...")
        
        existing_structure = set()
        protected_paths = set()
        
        # Scanner la structure existante
        for root, dirs, files in os.walk(self.target_path):
            rel_path = Path(root).relative_to(self.target_path)
            existing_structure.add(str(rel_path))
            
            # Marquer les dossiers avec beaucoup de fichiers comme protégés
            if len(files) > 10 or len(dirs) > 5:
                protected_paths.add(str(rel_path))
                
        self.existing_structure = existing_structure
        self.protected_paths = protected_paths
        
        self.log(f"📊 {len(existing_structure)} dossiers existants")
        self.log(f"🔒 {len(protected_paths)} dossiers protégés")
        
    def find_orphan_files(self):
        """Trouve les fichiers isolés qui pourraient être réorganisés"""
        self.log("🔎 Recherche des fichiers isolés...")
        
        orphans = []
        root_files = list(self.target_path.glob('*'))
        
        for item in root_files:
            if item.is_file() and not item.name.startswith('.'):
                orphans.append(item)
                
        # Fichiers dans des dossiers peu organisés
        shallow_dirs = ['Desktop', 'Downloads', 'Documents']
        for dir_name in shallow_dirs:
            dir_path = self.target_path / dir_name
            if dir_path.exists():
                for item in dir_path.rglob('*'):
                    if (item.is_file() and 
                        not item.name.startswith('.') and
                        not self.is_in_organized_structure(item)):
                        orphans.append(item)
                        
        self.analysis_results['orphan_files'] = orphans
        self.analysis_results['stats']['orphans_found'] = len(orphans)
        
        self.log(f"📄 {len(orphans)} fichiers isolés détectés")
        
    def is_in_organized_structure(self, filepath):
        """Vérifie si le fichier est déjà dans une structure organisée"""
        path_parts = filepath.parts
        
        # Ignorer les fichiers dans des structures projet connues
        organized_indicators = [
            '.git', 'node_modules', '__pycache__', '.venv', 'venv',
            'src', 'lib', 'build', 'dist', 'output'
        ]
        
        for part in path_parts:
            if part in organized_indicators:
                return True
                
        # Ignorer les fichiers dans des dossiers profonds (probablement organisés)
        relative_to_target = filepath.relative_to(self.target_path)
        if len(relative_to_target.parts) > 3:
            return True
            
        return False
        
    def suggest_destination(self, filepath):
        """Suggère une destination intelligente pour un fichier"""
        filename = filepath.name.lower()
        extension = filepath.suffix.lower()
        content = self.analyze_file_content(filepath)
        
        # Scores pour chaque destination possible
        destination_scores = defaultdict(int)
        
        # 1. Analyse par extension
        extension_mapping = {
            # Documents
            '.pdf': [('Documents/Official_Papers', 20), ('Documents/Work_Professional', 15)],
            '.doc': [('Documents/Work_Professional', 25), ('Documents/Personal', 20)],
            '.docx': [('Documents/Work_Professional', 25), ('Documents/Personal', 20)],
            '.xls': [('Documents/Official_Papers/Financial_Records', 25)],
            '.xlsx': [('Documents/Official_Papers/Financial_Records', 25)],
            '.txt': [('Documents/Personal', 15), ('Tools_Utilities/Documentation', 10)],
            
            # Images
            '.jpg': [('Media/Photos', 25)],
            '.jpeg': [('Media/Photos', 25)],
            '.png': [('Media/Photos', 20), ('Projects/Creative', 15)],
            '.gif': [('Media/Photos', 15)],
            '.heic': [('Media/Photos/Personal', 25)],
            
            # Vidéos
            '.mp4': [('Media/Videos', 25)],
            '.mov': [('Media/Videos', 25)],
            '.avi': [('Media/Videos', 20)],
            
            # Audio
            '.mp3': [('Media/Audio', 25)],
            '.wav': [('Media/Audio', 20)],
            '.flac': [('Media/Audio/Music', 25)],
            
            # Code/Scripts
            '.py': [('Projects/Development/Scripts', 25)],
            '.js': [('Projects/Development/Web_Projects', 25)],
            '.html': [('Projects/Development/Web_Projects', 25)],
            '.css': [('Projects/Development/Web_Projects', 25)],
            '.sh': [('Tools_Utilities/Scripts', 25)],
            
            # Archives
            '.zip': [('Tools_Utilities/Software', 20), ('Archives', 10)],
            '.dmg': [('Tools_Utilities/Software', 25)],
            '.pkg': [('Tools_Utilities/Software', 25)]
        }
        
        if extension in extension_mapping:
            for dest, score in extension_mapping[extension]:
                destination_scores[dest] += score
                
        # 2. Analyse par patterns de nom
        name_patterns = {
            # Documents officiels
            'Documents/Official_Papers/Identity_Documents': [
                r'.*passport.*', r'.*carte.*identite.*', r'.*cni.*', r'.*identity.*'
            ],
            'Documents/Official_Papers/Financial_Records': [
                r'.*facture.*', r'.*invoice.*', r'.*bank.*', r'.*compte.*', r'.*releve.*'
            ],
            'Documents/Official_Papers/Tax_Documents': [
                r'.*impot.*', r'.*tax.*', r'.*fiscal.*', r'.*avis.*'
            ],
            'Documents/Official_Papers/Property_Documents': [
                r'.*copropriete.*', r'.*syndic.*', r'.*immeuble.*', r'.*ag.*'
            ],
            
            # Travail
            'Documents/Work_Professional/CV_Resume': [
                r'.*cv.*', r'.*resume.*', r'.*curriculum.*'
            ],
            'Documents/Work_Professional/Payslips': [
                r'.*bulletin.*paie.*', r'.*salaire.*', r'.*payslip.*'
            ],
            
            # Projets créatifs
            'Projects/Creative/Brand_TUNETOO': [
                r'.*tunetoo.*', r'.*logo.*', r'.*brand.*'
            ],
            'Projects/Creative/Content_Creation': [
                r'.*youtube.*', r'.*content.*', r'.*social.*'
            ],
            
            # Média par contexte
            'Media/Photos/Travel': [
                r'.*travel.*', r'.*voyage.*', r'.*bali.*', r'.*taiwan.*', r'.*trip.*'
            ],
            'Media/Photos/Screenshots': [
                r'.*screenshot.*', r'.*capture.*', r'.*screen.*'
            ],
            'Media/Audio/Music': [
                r'.*music.*', r'.*song.*', r'.*chanson.*'
            ],
            'Media/Audio/Effects': [
                r'.*meditation.*', r'.*frequency.*', r'.*hz.*'
            ]
        }
        
        for destination, patterns in name_patterns.items():
            for pattern in patterns:
                if re.match(pattern, filename):
                    destination_scores[destination] += 30
                    
        # 3. Analyse par date (pour archives)
        try:
            mod_time = datetime.fromtimestamp(filepath.stat().st_mtime)
            year = mod_time.year
            
            if year <= 2020:
                destination_scores['Archives/By_Year/Older'] += 20
            elif year == 2021:
                destination_scores['Archives/By_Year/2021'] += 15
            elif year == 2022:
                destination_scores['Archives/By_Year/2022'] += 15
            elif year == 2023:
                destination_scores['Archives/By_Year/2023'] += 10
            # Fichiers récents restent où ils sont
        except:
            pass
            
        # 4. Analyse de contenu pour documents
        if content:
            content_keywords = {
                'Documents/Official_Papers/Property_Documents': [
                    'copropriété', 'syndic', 'assemblée', 'tantième', 'sadi', 'carnot'
                ],
                'Documents/Work_Professional': [
                    'bnpp', 'cyber', 'sécurité', 'consulting', 'projet'
                ],
                'Projects/Creative/Brand_TUNETOO': [
                    'tunetoo', 'design', 'création', 'marque'
                ]
            }
            
            for destination, keywords in content_keywords.items():
                for keyword in keywords:
                    if keyword in content.lower():
                        destination_scores[destination] += 25
                        
        # Retourner la meilleure destination
        if destination_scores:
            best_dest = max(destination_scores.items(), key=lambda x: x[1])
            return best_dest[0], best_dest[1]
        else:
            # Destination par défaut selon le type
            if extension in ['.jpg', '.png', '.gif', '.heic']:
                return 'Media/Photos/Personal', 10
            elif extension in ['.mp4', '.mov', '.avi']:
                return 'Media/Videos/Personal', 10
            elif extension in ['.mp3', '.wav']:
                return 'Media/Audio/Personal', 10
            elif extension in ['.pdf', '.doc', '.docx']:
                return 'Documents/Personal', 10
            else:
                return 'Archives/Unsorted', 5
                
    def analyze_file_content(self, filepath):
        """Analyse le contenu d'un fichier pour améliorer la classification"""
        if filepath.suffix.lower() not in ['.txt', '.md', '.pdf']:
            return None
            
        try:
            if filepath.suffix.lower() == '.txt':
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read(500)  # Premiers 500 caractères
        except:
            pass
            
        return None
        
    def propose_reorganization(self):
        """Propose une réorganisation sans conflits"""
        self.log("🎯 Proposition de réorganisation...")
        
        safe_moves = []
        conflicts = []
        
        for orphan_file in self.analysis_results['orphan_files']:
            destination, confidence = self.suggest_destination(orphan_file)
            
            # Construire le chemin de destination complet
            dest_path = self.target_path / destination
            final_dest = dest_path / orphan_file.name
            
            # Vérifier les conflits
            conflict_info = self.check_conflicts(orphan_file, final_dest)
            
            move_info = {
                'source': str(orphan_file),
                'destination': str(final_dest),
                'destination_dir': destination,
                'confidence': confidence,
                'conflict': conflict_info
            }
            
            if conflict_info['has_conflict']:
                conflicts.append(move_info)
                self.analysis_results['stats']['conflicts_detected'] += 1
            else:
                safe_moves.append(move_info)
                self.analysis_results['stats']['moves_proposed'] += 1
                
        self.analysis_results['safe_moves'] = safe_moves
        self.analysis_results['conflicts'] = conflicts
        
        self.log(f"✅ {len(safe_moves)} déplacements sûrs proposés")
        self.log(f"⚠️  {len(conflicts)} conflits détectés")
        
    def check_conflicts(self, source_file, destination_path):
        """Vérifie les conflits potentiels"""
        conflict_info = {
            'has_conflict': False,
            'type': None,
            'description': None,
            'suggested_resolution': None
        }
        
        # 1. Fichier existant avec même nom
        if destination_path.exists():
            conflict_info['has_conflict'] = True
            conflict_info['type'] = 'file_exists'
            conflict_info['description'] = f"Fichier existant: {destination_path.name}"
            
            # Analyser les deux fichiers pour suggestion
            source_size = source_file.stat().st_size
            dest_size = destination_path.stat().st_size
            source_date = source_file.stat().st_mtime
            dest_date = destination_path.stat().st_mtime
            
            if source_date > dest_date and source_size >= dest_size:
                conflict_info['suggested_resolution'] = 'replace_with_source'
            elif abs(source_size - dest_size) < 1024:  # Tailles similaires
                conflict_info['suggested_resolution'] = 'possible_duplicate'
            else:
                conflict_info['suggested_resolution'] = 'rename_source'
                
        # 2. Chemin dans une zone protégée
        dest_relative = destination_path.relative_to(self.target_path)
        for protected in self.protected_paths:
            if str(dest_relative).startswith(protected):
                if not conflict_info['has_conflict']:  # Ne pas écraser un conflit plus important
                    conflict_info['has_conflict'] = True
                    conflict_info['type'] = 'protected_path'
                    conflict_info['description'] = f"Zone protégée: {protected}"
                    conflict_info['suggested_resolution'] = 'find_alternative'
                    
        return conflict_info
        
    def generate_reorganization_plan(self):
        """Génère le plan de réorganisation"""
        output_dir = self.target_path / f"REORGANIZATION_PLAN_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_dir.mkdir(exist_ok=True)
        
        # Script de réorganisation
        script_path = output_dir / "reorganize.sh"
        with open(script_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Smart Reorganization Plan\n")
            f.write("# Réorganisation intelligente sans casser l'existant\n\n")
            
            f.write("set -e\n")
            f.write(f"BACKUP_DIR='{output_dir}/backup'\n")
            f.write("mkdir -p \"$BACKUP_DIR\"\n\n")
            
            # Section des déplacements sûrs
            f.write("echo \"=== DÉPLACEMENTS SÛRS ===\"\n")
            for move in self.analysis_results['safe_moves']:
                dest_dir = Path(move['destination']).parent
                f.write(f"echo \"Déplacement: {Path(move['source']).name} → {move['destination_dir']}\"\n")
                f.write(f"mkdir -p \"{dest_dir}\"\n")
                f.write(f"mv \"{move['source']}\" \"{move['destination']}\"\n\n")
                
            # Section des conflits avec résolutions
            if self.analysis_results['conflicts']:
                f.write("echo \"=== CONFLITS DÉTECTÉS - VÉRIFICATION MANUELLE REQUISE ===\"\n")
                for conflict in self.analysis_results['conflicts']:
                    f.write(f"# CONFLIT: {conflict['conflict']['description']}\n")
                    f.write(f"# Source: {conflict['source']}\n")
                    f.write(f"# Destination: {conflict['destination']}\n")
                    f.write(f"# Résolution suggérée: {conflict['conflict']['suggested_resolution']}\n")
                    
                    if conflict['conflict']['suggested_resolution'] == 'rename_source':
                        base_name = Path(conflict['source']).stem
                        extension = Path(conflict['source']).suffix
                        new_name = f"{base_name}_moved_{datetime.now().strftime('%Y%m%d')}{extension}"
                        dest_dir = Path(conflict['destination']).parent
                        f.write(f"# mkdir -p \"{dest_dir}\"\n")
                        f.write(f"# mv \"{conflict['source']}\" \"{dest_dir}/{new_name}\"\n")
                    elif conflict['conflict']['suggested_resolution'] == 'replace_with_source':
                        f.write(f"# cp \"{conflict['destination']}\" \"$BACKUP_DIR/\"\n")
                        f.write(f"# mv \"{conflict['source']}\" \"{conflict['destination']}\"\n")
                    
                    f.write("echo\n")
                    
        os.chmod(script_path, 0o755)
        
        # Rapport détaillé JSON
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'target_directory': str(self.target_path),
            'proposed_structure': self.proposed_structure,
            'analysis_results': {
                'stats': self.analysis_results['stats'],
                'safe_moves': self.analysis_results['safe_moves'],
                'conflicts': self.analysis_results['conflicts']
            }
        }
        
        with open(output_dir / "reorganization_report.json", 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
            
        # Résumé lisible
        summary_path = output_dir / "summary.txt"
        with open(summary_path, 'w') as f:
            f.write("PLAN DE RÉORGANISATION INTELLIGENTE\n")
            f.write("=" * 40 + "\n")
            f.write(f"Répertoire: {self.target_path}\n")
            f.write(f"Date: {datetime.now()}\n\n")
            
            f.write("STATISTIQUES:\n")
            stats = self.analysis_results['stats']
            f.write(f"  Fichiers analysés: {stats['total_files']:,}\n")
            f.write(f"  Fichiers isolés: {stats['orphans_found']:,}\n")
            f.write(f"  Déplacements sûrs: {stats['moves_proposed']:,}\n")
            f.write(f"  Conflits détectés: {stats['conflicts_detected']:,}\n\n")
            
            f.write("STRUCTURE PROPOSÉE:\n")
            f.write("📁 Documents/\n")
            f.write("   ├── Official_Papers/ (papiers officiels)\n")
            f.write("   ├── Work_Professional/ (travail)\n")
            f.write("   └── Personal/ (personnel)\n")
            f.write("📁 Media/\n")
            f.write("   ├── Photos/ (par contexte)\n")
            f.write("   ├── Videos/ (par type)\n")
            f.write("   └── Audio/ (par genre)\n")
            f.write("📁 Projects/\n")
            f.write("   ├── Development/ (code)\n")
            f.write("   ├── Creative/ (création)\n")
            f.write("   └── Business/ (business)\n")
            f.write("📁 Archives/ (par année)\n")
            f.write("📁 Tools_Utilities/ (outils)\n\n")
            
            f.write("SÉCURITÉS:\n")
            f.write("✓ Aucun dossier existant ne sera écrasé\n")
            f.write("✓ Fichiers en conflit nécessitent validation manuelle\n")
            f.write("✓ Sauvegarde automatique des remplacements\n")
            f.write("✓ Zones protégées respectées\n\n")
            
            f.write("EXÉCUTION:\n")
            f.write(f"1. Vérifiez le plan: {script_path}\n")
            f.write("2. Résolvez les conflits manuellement\n")
            f.write("3. Exécutez: bash reorganize.sh\n")
            
        self.log(f"📋 Plan généré: {output_dir}")
        return output_dir
        
    def log(self, message):
        """Log avec timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        
    def reorganize(self):
        """Processus principal de réorganisation"""
        self.log("🚀 RÉORGANISATION INTELLIGENTE")
        
        if not self.target_path.exists():
            self.log(f"❌ Répertoire inexistant: {self.target_path}")
            return
            
        # Étape 1: Analyser l'existant
        self.analyze_current_structure()
        
        # Étape 2: Trouver les fichiers isolés
        self.find_orphan_files()
        
        # Étape 3: Proposer la réorganisation
        self.propose_reorganization()
        
        # Étape 4: Générer le plan
        plan_dir = self.generate_reorganization_plan()
        
        # Résumé final
        stats = self.analysis_results['stats']
        print(f"\n{'='*60}")
        print("🎯 PLAN DE RÉORGANISATION TERMINÉ!")
        print(f"📊 Statistiques:")
        print(f"   • {stats['orphans_found']:,} fichiers isolés détectés")
        print(f"   • {stats['moves_proposed']:,} déplacements sûrs proposés")
        print(f"   • {stats['conflicts_detected']:,} conflits nécessitant validation")
        print(f"📁 Plan complet: {plan_dir}")
        print("⚠️  IMPORTANT:")
        print("   1. Vérifiez le plan avant exécution")
        print("   2. Résolvez les conflits manuellement")
        print("   3. Testez sur quelques fichiers d'abord")
        print("="*60)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 smart_reorganizer.py <directory>")
        print("Exemple: python3 smart_reorganizer.py ~/")
        sys.exit(1)
        
    target = sys.argv[1]
    if not os.path.exists(target):
        print(f"❌ Répertoire inexistant: {target}")
        sys.exit(1)
        
    reorganizer = SmartReorganizer(target)
    reorganizer.reorganize()

if __name__ == "__main__":
    main()