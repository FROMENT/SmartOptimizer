#!/usr/bin/env python3
"""
Quick Smart Optimizer - Version rapide sans dépendances
Analyse intelligente: logique, contenu, date, taille pour garder le meilleur
"""

import os
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import json
import sys
import mimetypes

class QuickSmartOptimizer:
    def __init__(self, target_path):
        self.target_path = Path(target_path)
        self.output_path = Path(f"{target_path}_OPTIMIZED_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.stats = {
            'files_analyzed': 0,
            'duplicates_found': 0,
            'space_saved': 0,
            'groups_found': 0
        }
        
    def log(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        
    def quick_analyze(self, filepath):
        """Analyse rapide et efficace"""
        try:
            stat = filepath.stat()
            
            # Info de base
            info = {
                'path': str(filepath),
                'name': filepath.name,
                'stem': filepath.stem,
                'extension': filepath.suffix.lower(),
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'created': stat.st_ctime,
                'quality_score': 0
            }
            
            # Type de fichier
            info['file_type'] = self.detect_type(filepath)
            
            # Hash pour petits fichiers seulement
            if stat.st_size < 10 * 1024 * 1024:  # < 10MB
                info['hash'] = self.quick_hash(filepath)
            
            # Score intelligent
            info['quality_score'] = self.smart_score(info)
            
            self.stats['files_analyzed'] += 1
            return info
            
        except Exception as e:
            self.log(f"❌ Erreur {filepath}: {e}")
            return None
            
    def detect_type(self, filepath):
        """Détection rapide du type"""
        ext = filepath.suffix.lower()
        
        if ext in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.heic', '.webp'}:
            return 'image'
        elif ext in {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.webm'}:
            return 'video'
        elif ext in {'.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg'}:
            return 'audio'
        elif ext in {'.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx'}:
            return 'document'
        else:
            return 'other'
            
    def quick_hash(self, filepath):
        """Hash rapide des premiers et derniers Ko"""
        try:
            with open(filepath, 'rb') as f:
                # Lire début et fin pour hash rapide
                start = f.read(1024)
                f.seek(-min(1024, filepath.stat().st_size), 2)
                end = f.read(1024)
                
            return hashlib.md5(start + end).hexdigest()[:12]
        except:
            return None
            
    def smart_score(self, info):
        """Score intelligent basé sur logique métier"""
        score = 0
        
        # 1. FRAÎCHEUR (35 points max)
        days_old = (datetime.now().timestamp() - info['modified']) / 86400
        if days_old < 1:
            score += 35      # Très récent
        elif days_old < 7:
            score += 30      # Cette semaine
        elif days_old < 30:
            score += 20      # Ce mois
        elif days_old < 365:
            score += 10      # Cette année
        else:
            score += 2       # Ancien
            
        # 2. QUALITÉ ESTIMÉE PAR TYPE (30 points max)
        size_mb = info['size'] / (1024 * 1024)
        file_type = info['file_type']
        
        if file_type == 'image':
            if 1 <= size_mb <= 25:     # Taille raisonnable
                score += 25
            elif size_mb > 50:         # Très gros = probable haute qualité
                score += 30
            elif size_mb < 0.1:        # Très petit = probable miniature
                score += 5
            else:
                score += 15
                
        elif file_type == 'video':
            if 50 <= size_mb <= 2000:  # Taille raisonnable
                score += 25
            elif size_mb > 2000:       # Très gros = haute qualité
                score += 30
            elif size_mb < 5:          # Très petit = basse qualité
                score += 5
            else:
                score += 15
                
        elif file_type == 'audio':
            if 3 <= size_mb <= 100:    # Taille raisonnable
                score += 25
            elif info['extension'] == '.flac':  # Lossless
                score += 30
            elif size_mb < 1:          # Très petit = basse qualité
                score += 5
            else:
                score += 15
                
        elif file_type == 'document':
            if 0.01 <= size_mb <= 50:  # Taille raisonnable
                score += 20
            else:
                score += 10
        else:
            score += 10
            
        # 3. QUALITÉ DU NOM (20 points max)
        name_lower = info['name'].lower()
        
        # Malus pour noms temporaires
        penalties = [
            ('copy', -8), ('copie', -8), ('temp', -10), ('tmp', -10),
            ('nouveau', -6), ('untitled', -8), ('sans nom', -8),
            (' (1)', -5), (' (2)', -7), (' (3)', -10),
            ('(1)', -5), ('(2)', -7), ('(3)', -10),
            ('~$', -15)  # Fichiers Office temporaires
        ]
        
        name_score = 20
        for penalty_text, penalty_points in penalties:
            if penalty_text in name_lower:
                name_score += penalty_points
                
        # Bonus pour noms avec dates
        if any(char.isdigit() for char in info['stem'][:10]):
            name_score += 3
            
        score += max(0, name_score)
        
        # 4. EXTENSION DE QUALITÉ (15 points max)
        quality_exts = {
            # Images
            '.png': 12, '.tiff': 15, '.heic': 10,
            # Vidéos  
            '.mkv': 12, '.mp4': 10,
            # Audio
            '.flac': 15, '.wav': 12, '.m4a': 8,
            # Documents
            '.pdf': 10, '.docx': 8
        }
        
        score += quality_exts.get(info['extension'], 0)
        
        return min(100, max(0, score))
        
    def find_optimization_groups(self, files):
        """Groupement intelligent pour optimisation"""
        groups = []
        
        # 1. DOUBLONS EXACTS (même hash)
        by_hash = defaultdict(list)
        for file_info in files:
            if file_info.get('hash'):
                by_hash[file_info['hash']].append(file_info)
                
        for hash_files in by_hash.values():
            if len(hash_files) > 1:
                groups.append({
                    'type': 'exact_duplicate',
                    'reason': 'Contenu identique',
                    'files': hash_files,
                    'confidence': 100
                })
        
        # 2. NOMS SIMILAIRES + MÊME TYPE
        by_clean_name = defaultdict(list)
        for file_info in files:
            clean_name = self.normalize_filename(file_info['stem'])
            if len(clean_name) > 3:  # Ignorer noms trop courts
                key = (clean_name, file_info['file_type'])
                by_clean_name[key].append(file_info)
                
        for (clean_name, ftype), name_files in by_clean_name.items():
            if len(name_files) > 1:
                # Exclure déjà traités dans doublons exacts
                non_exact = [f for f in name_files 
                           if not any(f in g['files'] for g in groups 
                                    if g['type'] == 'exact_duplicate')]
                
                if len(non_exact) > 1:
                    groups.append({
                        'type': 'name_similar',
                        'reason': f'Nom similaire "{clean_name}" ({ftype})',
                        'files': non_exact,
                        'confidence': 85
                    })
        
        # 3. LOTS DE MÊME TYPE + TAILLE SIMILAIRE
        by_type_size = defaultdict(list)
        for file_info in files:
            size_bracket = self.get_size_bracket(file_info['size'])
            key = (file_info['file_type'], size_bracket)
            by_type_size[key].append(file_info)
            
        for (ftype, size_bracket), type_files in by_type_size.items():
            if len(type_files) > 4:  # Au moins 5 fichiers
                # Vérifier si beaucoup de noms similaires
                clean_names = [self.normalize_filename(f['stem']) for f in type_files]
                unique_names = set(clean_names)
                
                if len(unique_names) <= len(type_files) * 0.6:  # 60% de noms différents max
                    non_processed = [f for f in type_files
                                   if not any(f in g['files'] for g in groups)]
                    
                    if len(non_processed) > 3:
                        groups.append({
                            'type': 'bulk_similar',
                            'reason': f'Lot {ftype} taille {size_bracket}',
                            'files': non_processed,
                            'confidence': 65
                        })
        
        return groups
        
    def normalize_filename(self, filename):
        """Normalise le nom pour détecter les similarités"""
        import re
        
        name = filename.lower().strip()
        
        # Enlever timestamps et dates
        name = re.sub(r'\d{4}[-_]\d{2}[-_]\d{2}', '', name)
        name = re.sub(r'\d{2}[-_]\d{2}[-_]\d{4}', '', name)
        name = re.sub(r'\d{8}[-_]\d{6}', '', name)
        
        # Enlever numérotations
        name = re.sub(r'\s*\(\d+\)\s*$', '', name)
        name = re.sub(r'\s*[-_]\s*\d+\s*$', '', name)
        
        # Enlever mots temporaires
        temp_words = ['copy', 'copie', 'temp', 'tmp', 'nouveau', 'new']
        for word in temp_words:
            name = re.sub(rf'\b{word}\b', '', name)
            
        # Nettoyer espaces et caractères
        name = re.sub(r'[_\-\s]+', ' ', name).strip()
        
        return name
        
    def get_size_bracket(self, size):
        """Catégorise par taille"""
        mb = size / (1024 * 1024)
        
        if mb < 0.1:
            return 'tiny'
        elif mb < 1:
            return 'small'
        elif mb < 10:
            return 'medium'
        elif mb < 100:
            return 'large'
        else:
            return 'huge'
            
    def select_best_from_group(self, files):
        """Sélectionne le meilleur fichier intelligemment"""
        if len(files) <= 1:
            return files[0] if files else None, []
            
        # Tri multi-critères intelligent
        def sort_key(f):
            return (
                f['quality_score'],           # Score principal
                f['size'],                    # Taille (plus gros = potentiellement meilleur)
                f['modified'],                # Plus récent
                len(f['name'])                # Nom plus descriptif
            )
            
        sorted_files = sorted(files, key=sort_key, reverse=True)
        
        # Protection: ne pas supprimer fichier très récent même si score plus bas
        best = sorted_files[0]
        candidates = sorted_files[1:]
        
        final_to_remove = []
        for candidate in candidates:
            # Protection fichier de moins de 24h
            hours_old = (datetime.now().timestamp() - candidate['modified']) / 3600
            score_diff = best['quality_score'] - candidate['quality_score']
            
            if hours_old < 24 and score_diff < 15:
                self.log(f"⚠️  Protection fichier récent: {candidate['name']}")
                continue
                
            final_to_remove.append(candidate)
            
        return best, final_to_remove
        
    def optimize(self):
        """Processus d'optimisation principal"""
        self.log("🚀 OPTIMISATION INTELLIGENTE RAPIDE")
        
        if not self.target_path.exists():
            self.log(f"❌ Répertoire inexistant: {self.target_path}")
            return
            
        # Scanner rapidement
        all_files = []
        self.log("📊 Analyse des fichiers...")
        
        for filepath in self.target_path.rglob('*'):
            if (filepath.is_file() and 
                not filepath.name.startswith('.') and
                filepath.stat().st_size > 0):
                
                file_info = self.quick_analyze(filepath)
                if file_info:
                    all_files.append(file_info)
                    
        self.log(f"📈 {len(all_files)} fichiers analysés")
        
        # Grouper par type pour optimisation ciblée
        files_by_type = defaultdict(list)
        for file_info in all_files:
            files_by_type[file_info['file_type']].append(file_info)
            
        # Statistiques par type
        for ftype, files in files_by_type.items():
            self.log(f"  {ftype}: {len(files)} fichiers")
            
        # Trouver les groupes d'optimisation
        self.log("🔍 Recherche des optimisations...")
        all_groups = self.find_optimization_groups(all_files)
        
        optimization_plan = []
        for group in all_groups:
            best, to_remove = self.select_best_from_group(group['files'])
            if to_remove:
                space_saved = sum(f['size'] for f in to_remove)
                self.stats['space_saved'] += space_saved
                self.stats['duplicates_found'] += len(to_remove)
                self.stats['groups_found'] += 1
                
                optimization_plan.append({
                    'type': group['type'],
                    'reason': group['reason'],
                    'confidence': group['confidence'],
                    'best': best,
                    'remove': to_remove,
                    'space_saved': space_saved
                })
        
        # Générer les résultats
        self.save_optimization_plan(optimization_plan)
        
    def save_optimization_plan(self, plan):
        """Sauvegarde le plan d'optimisation"""
        self.output_path.mkdir(exist_ok=True)
        
        # Script de nettoyage
        script_path = self.output_path / "smart_cleanup.sh"
        with open(script_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Smart Cleanup - Généré automatiquement\n")
            f.write("# LOGIQUE: Contenu + Date + Qualité + Taille\n\n")
            
            f.write(f"BACKUP_DIR='{self.output_path}/backup'\n")
            f.write("mkdir -p \"$BACKUP_DIR\"\n\n")
            
            # Grouper par confiance
            high_conf = [p for p in plan if p['confidence'] >= 90]
            med_conf = [p for p in plan if 70 <= p['confidence'] < 90]
            low_conf = [p for p in plan if p['confidence'] < 70]
            
            sections = [
                ("HAUTE CONFIANCE (90%+)", high_conf, False),
                ("CONFIANCE MOYENNE (70-89%)", med_conf, True),
                ("FAIBLE CONFIANCE (<70%)", low_conf, True)
            ]
            
            for title, section_plan, commented in sections:
                f.write(f"echo \"=== {title} ===\"\n")
                prefix = "# " if commented else ""
                
                for i, item in enumerate(section_plan, 1):
                    f.write(f"echo \"Groupe {i}: {item['reason']} (Confiance: {item['confidence']}%)\"\n")
                    f.write(f"echo \"  ✅ GARDER: {item['best']['name']} (Score: {item['best']['quality_score']})\"\n")
                    f.write(f"echo \"  💾 Économie: {item['space_saved']:,} bytes\"\n")
                    
                    for file_info in item['remove']:
                        rel_path = Path(file_info['path']).relative_to(self.target_path)
                        f.write(f"echo \"    ❌ Supprimer: {file_info['name']} (Score: {file_info['quality_score']})\"\n")
                        f.write(f"{prefix}mkdir -p \"$BACKUP_DIR/$(dirname '{rel_path}')\"\n")
                        f.write(f"{prefix}cp \"{file_info['path']}\" \"$BACKUP_DIR/{rel_path}\"\n")
                        f.write(f"{prefix}rm \"{file_info['path']}\"\n")
                    f.write("echo\n")
                f.write("\n")
                
        os.chmod(script_path, 0o755)
        
        # Rapport JSON
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'target_directory': str(self.target_path),
            'statistics': self.stats,
            'optimization_plan': plan,
            'summary': {
                'high_confidence_groups': len([p for p in plan if p['confidence'] >= 90]),
                'medium_confidence_groups': len([p for p in plan if 70 <= p['confidence'] < 90]),
                'low_confidence_groups': len([p for p in plan if p['confidence'] < 70]),
                'total_space_gb': self.stats['space_saved'] / (1024**3)
            }
        }
        
        with open(self.output_path / "report.json", 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
            
        # Résumé lisible
        with open(self.output_path / "summary.txt", 'w') as f:
            f.write("QUICK SMART OPTIMIZER - RÉSUMÉ\n")
            f.write("=" * 35 + "\n")
            f.write(f"Répertoire analysé: {self.target_path}\n")
            f.write(f"Fichiers analysés: {self.stats['files_analyzed']:,}\n")
            f.write(f"Groupes d'optimisation: {self.stats['groups_found']:,}\n")
            f.write(f"Fichiers redondants: {self.stats['duplicates_found']:,}\n")
            f.write(f"Espace récupérable: {self.stats['space_saved']/(1024**3):.2f} GB\n\n")
            
            f.write("RÉPARTITION PAR CONFIANCE:\n")
            f.write(f"  Haute (90%+): {len([p for p in plan if p['confidence'] >= 90])} groupes\n")
            f.write(f"  Moyenne (70-89%): {len([p for p in plan if 70 <= p['confidence'] < 90])} groupes\n")
            f.write(f"  Faible (<70%): {len([p for p in plan if p['confidence'] < 70])} groupes\n\n")
            
            f.write("CRITÈRES D'OPTIMISATION:\n")
            f.write("✓ Fraîcheur des fichiers (35%)\n")
            f.write("✓ Qualité estimée par type et taille (30%)\n")
            f.write("✓ Intelligence du nommage (20%)\n")
            f.write("✓ Extension de qualité (15%)\n")
            f.write("✓ Protection des fichiers récents (<24h)\n")
            
        # Affichage final
        self.log("✅ OPTIMISATION TERMINÉE!")
        self.log(f"📊 {self.stats['files_analyzed']:,} fichiers → {self.stats['groups_found']} groupes optimisés")
        self.log(f"💾 {self.stats['space_saved']/(1024**3):.2f} GB récupérables")
        self.log(f"📁 Résultats: {self.output_path}")
        self.log(f"🚀 Script: {script_path}")
        
        print(f"\n{'='*60}")
        print("🎯 OPTIMISATION INTELLIGENTE TERMINÉE!")
        print(f"📈 Statistiques:")
        print(f"   • {self.stats['files_analyzed']:,} fichiers analysés")
        print(f"   • {self.stats['groups_found']} groupes d'optimisation")
        print(f"   • {self.stats['duplicates_found']} fichiers redondants")
        print(f"   • {self.stats['space_saved']/(1024**3):.2f} GB récupérables")
        print(f"📁 Résultats: {self.output_path}")
        print("⚠️  Vérifiez smart_cleanup.sh avant exécution!")
        print("="*60)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 quick_smart_optimizer.py <directory>")
        print("Exemple: python3 quick_smart_optimizer.py ~/Desktop/TUNETOO")
        sys.exit(1)
        
    target = sys.argv[1]
    if not os.path.exists(target):
        print(f"❌ Répertoire inexistant: {target}")
        sys.exit(1)
        
    optimizer = QuickSmartOptimizer(target)
    optimizer.optimize()

if __name__ == "__main__":
    main()