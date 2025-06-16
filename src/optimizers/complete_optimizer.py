#!/usr/bin/env python3
"""
Complete Smart Optimizer - Version complète avec métadonnées
Optimisation intelligente avec analyse EXIF, vidéo et audio
"""

import os
import sys
import hashlib
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import json
import subprocess

# Tentative d'import des dépendances optionnelles
DEPENDENCIES = {
    'pillow': False,
    'moviepy': False, 
    'mutagen': False
}

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    DEPENDENCIES['pillow'] = True
except ImportError:
    pass

try:
    from moviepy.editor import VideoFileClip
    DEPENDENCIES['moviepy'] = True
except ImportError:
    pass

try:
    from mutagen import File as MutagenFile
    DEPENDENCIES['mutagen'] = True
except ImportError:
    pass

class CompleteOptimizer:
    def __init__(self, target_directory):
        self.target_dir = Path(target_directory)
        self.backup_dir = Path.home() / "SmartOptimizer_Backups" / datetime.now().strftime('%Y%m%d_%H%M%S')
        self.simulation_mode = True
        self.confidence_threshold = 70
        self.file_analysis = {}
        self.duplicates = {}
        self.optimization_stats = {
            'analyzed': 0,
            'duplicates_found': 0,
            'space_saved': 0,
            'files_moved': 0,
            'files_removed': 0
        }
        
    def analyze_directory(self):
        """Analyse complète d'un répertoire"""
        print(f"🔍 ANALYSE COMPLÈTE: {self.target_dir}")
        print("=" * 50)
        
        if not self.target_dir.exists():
            print(f"❌ Répertoire inexistant: {self.target_dir}")
            return False
            
        print(f"📊 Dépendances disponibles:")
        for dep, available in DEPENDENCIES.items():
            status = "✅" if available else "❌"
            print(f"  {status} {dep}")
            
        # 1. Scanner tous les fichiers
        all_files = self.scan_all_files()
        
        # 2. Analyser chaque fichier
        for file_path in all_files:
            self.analyze_file(file_path)
            
        # 3. Détecter les doublons
        self.detect_duplicates()
        
        # 4. Générer les recommandations
        self.generate_recommendations()
        
        return True
        
    def scan_all_files(self):
        """Scanner tous les fichiers du répertoire"""
        print(f"📁 Scan des fichiers...")
        files = []
        
        for root, dirs, filenames in os.walk(self.target_dir):
            # Ignorer certains dossiers
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            
            for filename in filenames:
                if not filename.startswith('.'):
                    file_path = Path(root) / filename
                    if file_path.is_file():
                        files.append(file_path)
        
        print(f"  📋 {len(files)} fichiers trouvés")
        self.optimization_stats['analyzed'] = len(files)
        return files
        
    def analyze_file(self, file_path):
        """Analyse complète d'un fichier"""
        try:
            stat = file_path.stat()
            
            analysis = {
                'path': str(file_path),
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'created': stat.st_ctime,
                'extension': file_path.suffix.lower(),
                'hash': self.calculate_hash(file_path),
                'quality_score': 0,
                'metadata': {},
                'recommendations': []
            }
            
            # Analyse par type de fichier
            if analysis['extension'] in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']:
                analysis['metadata'] = self.analyze_image(file_path)
            elif analysis['extension'] in ['.mp4', '.avi', '.mov', '.mkv']:
                analysis['metadata'] = self.analyze_video(file_path)
            elif analysis['extension'] in ['.mp3', '.wav', '.flac', '.m4a']:
                analysis['metadata'] = self.analyze_audio(file_path)
                
            # Calculer le score de qualité
            analysis['quality_score'] = self.calculate_quality_score(analysis)
            
            self.file_analysis[str(file_path)] = analysis
            
        except Exception as e:
            print(f"  ⚠️  Erreur analyse {file_path.name}: {e}")
            
    def calculate_hash(self, file_path):
        """Calcul du hash MD5 d'un fichier"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None
            
    def analyze_image(self, file_path):
        """Analyse spécifique des images"""
        metadata = {'type': 'image'}
        
        if DEPENDENCIES['pillow']:
            try:
                with Image.open(file_path) as img:
                    metadata.update({
                        'dimensions': img.size,
                        'mode': img.mode,
                        'format': img.format
                    })
                    
                    # Extraire EXIF
                    if hasattr(img, '_getexif') and img._getexif():
                        exif = img._getexif()
                        if exif:
                            for tag_id, value in exif.items():
                                tag = TAGS.get(tag_id, tag_id)
                                if tag in ['DateTime', 'Make', 'Model', 'ExifImageWidth', 'ExifImageHeight']:
                                    metadata[f'exif_{tag}'] = str(value)
                                    
            except Exception as e:
                metadata['error'] = str(e)
        else:
            # Fallback basique avec file command
            try:
                result = subprocess.run(['file', str(file_path)], capture_output=True, text=True)
                if 'image' in result.stdout.lower():
                    metadata['basic_info'] = result.stdout.strip()
            except:
                pass
                
        return metadata
        
    def analyze_video(self, file_path):
        """Analyse spécifique des vidéos"""
        metadata = {'type': 'video'}
        
        if DEPENDENCIES['moviepy']:
            try:
                with VideoFileClip(str(file_path)) as clip:
                    metadata.update({
                        'duration': clip.duration,
                        'fps': clip.fps,
                        'size': clip.size,
                        'audio': clip.audio is not None
                    })
            except Exception as e:
                metadata['error'] = str(e)
        else:
            # Fallback avec ffprobe si disponible
            try:
                result = subprocess.run([
                    'ffprobe', '-v', 'quiet', '-print_format', 'json', 
                    '-show_format', '-show_streams', str(file_path)
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    if 'format' in data:
                        metadata['duration'] = float(data['format'].get('duration', 0))
                        metadata['bitrate'] = int(data['format'].get('bit_rate', 0))
                        
            except:
                pass
                
        return metadata
        
    def analyze_audio(self, file_path):
        """Analyse spécifique des fichiers audio"""
        metadata = {'type': 'audio'}
        
        if DEPENDENCIES['mutagen']:
            try:
                audio_file = MutagenFile(str(file_path))
                if audio_file:
                    info = audio_file.info
                    metadata.update({
                        'duration': getattr(info, 'length', 0),
                        'bitrate': getattr(info, 'bitrate', 0),
                        'sample_rate': getattr(info, 'sample_rate', 0)
                    })
                    
                    # Tags communs
                    tags = audio_file.tags
                    if tags:
                        for key in ['TIT2', 'TPE1', 'TALB', 'TDRC']:  # Title, Artist, Album, Year
                            if key in tags:
                                metadata[f'tag_{key}'] = str(tags[key][0])
                                
            except Exception as e:
                metadata['error'] = str(e)
                
        return metadata
        
    def calculate_quality_score(self, analysis):
        """Calcule un score de qualité pour un fichier"""
        score = 0
        
        # 1. Score de fraîcheur (35 points max)
        age_days = (datetime.now().timestamp() - analysis['modified']) / 86400
        if age_days < 1:
            score += 35
        elif age_days < 7:
            score += 30
        elif age_days < 30:
            score += 20
        elif age_days < 180:
            score += 10
            
        # 2. Score de qualité technique (30 points max)
        metadata = analysis['metadata']
        
        if metadata.get('type') == 'image':
            if 'dimensions' in metadata:
                width, height = metadata['dimensions']
                megapixels = (width * height) / 1000000
                if megapixels >= 12:
                    score += 30
                elif megapixels >= 8:
                    score += 25
                elif megapixels >= 5:
                    score += 20
                elif megapixels >= 2:
                    score += 15
                    
        elif metadata.get('type') == 'video':
            if 'size' in metadata:
                width, height = metadata['size']
                if height >= 1080:
                    score += 30
                elif height >= 720:
                    score += 25
                elif height >= 480:
                    score += 20
                    
        elif metadata.get('type') == 'audio':
            bitrate = metadata.get('bitrate', 0)
            if bitrate >= 320:
                score += 30
            elif bitrate >= 256:
                score += 25
            elif bitrate >= 192:
                score += 20
            elif bitrate >= 128:
                score += 15
                
        # 3. Score de taille optimale (20 points max)
        size_mb = analysis['size'] / (1024 * 1024)
        if analysis['extension'] in ['.jpg', '.jpeg', '.png']:
            if 1 <= size_mb <= 10:
                score += 20
            elif size_mb <= 20:
                score += 15
            elif size_mb <= 50:
                score += 10
        elif analysis['extension'] in ['.mp4', '.avi', '.mov']:
            if 100 <= size_mb <= 2000:
                score += 20
            elif size_mb <= 5000:
                score += 15
                
        # 4. Score de nom intelligent (15 points max)
        filename = Path(analysis['path']).name
        if any(word in filename.lower() for word in ['final', 'best', 'hq', 'hd', '4k']):
            score += 15
        elif any(word in filename.lower() for word in ['good', 'ok', 'clean']):
            score += 10
        elif any(word in filename.lower() for word in ['tmp', 'temp', 'old', 'backup']):
            score -= 10
            
        return min(100, max(0, score))
        
    def detect_duplicates(self):
        """Détecte les fichiers dupliqués"""
        print(f"🔍 Détection des doublons...")
        
        hash_groups = {}
        
        # Grouper par hash
        for path, analysis in self.file_analysis.items():
            file_hash = analysis.get('hash')
            if file_hash:
                if file_hash not in hash_groups:
                    hash_groups[file_hash] = []
                hash_groups[file_hash].append(analysis)
                
        # Identifier les vrais doublons
        for file_hash, files in hash_groups.items():
            if len(files) > 1:
                # Trier par score de qualité
                files.sort(key=lambda x: x['quality_score'], reverse=True)
                
                best_file = files[0]
                duplicates = files[1:]
                
                self.duplicates[file_hash] = {
                    'best': best_file,
                    'duplicates': duplicates,
                    'space_saving': sum(f['size'] for f in duplicates)
                }
                
        print(f"  📊 {len(self.duplicates)} groupes de doublons trouvés")
        self.optimization_stats['duplicates_found'] = len(self.duplicates)
        
    def generate_recommendations(self):
        """Génère les recommandations d'optimisation"""
        print(f"\n💡 RECOMMANDATIONS D'OPTIMISATION:")
        print("=" * 40)
        
        total_space_saving = 0
        actions = []
        
        for file_hash, dup_info in self.duplicates.items():
            best = dup_info['best']
            duplicates = dup_info['duplicates']
            space_saving = dup_info['space_saving']
            total_space_saving += space_saving
            
            print(f"\n📋 Groupe de doublons ({len(duplicates)+1} fichiers):")
            print(f"  ✅ GARDER: {Path(best['path']).name} (score: {best['quality_score']})")
            
            for dup in duplicates:
                confidence = self.calculate_confidence(best, dup)
                action = "SUPPRIMER" if confidence >= self.confidence_threshold else "VÉRIFIER"
                status = "🔴" if action == "SUPPRIMER" else "🟡"
                
                print(f"  {status} {action}: {Path(dup['path']).name} (score: {dup['quality_score']}, confiance: {confidence}%)")
                
                actions.append({
                    'action': action,
                    'file': dup['path'],
                    'confidence': confidence,
                    'space_saving': dup['size']
                })
                
        print(f"\n📊 STATISTIQUES D'OPTIMISATION:")
        print(f"  📁 Fichiers analysés: {self.optimization_stats['analyzed']}")
        print(f"  🔄 Groupes de doublons: {len(self.duplicates)}")
        print(f"  💾 Espace récupérable: {self.format_size(total_space_saving)}")
        
        safe_actions = [a for a in actions if a['confidence'] >= 90]
        manual_actions = [a for a in actions if a['confidence'] < 70]
        
        print(f"  ✅ Actions sûres (90%+): {len(safe_actions)}")
        print(f"  🟡 Actions à vérifier (<70%): {len(manual_actions)}")
        
        if safe_actions and not self.simulation_mode:
            self.execute_optimizations(safe_actions)
            
    def calculate_confidence(self, best_file, duplicate_file):
        """Calcule la confiance pour supprimer un doublon"""
        confidence = 50  # Base
        
        # Différence de score de qualité
        score_diff = best_file['quality_score'] - duplicate_file['quality_score']
        confidence += min(30, max(0, score_diff))
        
        # Différence d'âge
        age_diff = best_file['modified'] - duplicate_file['modified']
        if age_diff > 86400:  # Plus d'un jour
            confidence += 15
        elif age_diff > 0:
            confidence += 5
            
        # Analyse du nom
        best_name = Path(best_file['path']).name.lower()
        dup_name = Path(duplicate_file['path']).name.lower()
        
        if 'copy' in dup_name or '(1)' in dup_name or '(2)' in dup_name:
            confidence += 20
        elif 'tmp' in dup_name or 'temp' in dup_name:
            confidence += 15
            
        return min(100, max(0, confidence))
        
    def execute_optimizations(self, actions):
        """Exécute les optimisations approuvées"""
        if not self.simulation_mode:
            # Créer le répertoire de sauvegarde
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            
        executed = 0
        space_saved = 0
        
        for action in actions:
            if action['confidence'] >= self.confidence_threshold:
                file_path = Path(action['file'])
                
                if not self.simulation_mode:
                    # Sauvegarder avant suppression
                    backup_path = self.backup_dir / file_path.name
                    shutil.copy2(file_path, backup_path)
                    
                    # Supprimer l'original
                    file_path.unlink()
                    
                executed += 1
                space_saved += action['space_saving']
                
        print(f"\n✅ OPTIMISATION TERMINÉE:")
        print(f"  🗑️  Fichiers supprimés: {executed}")
        print(f"  💾 Espace libéré: {self.format_size(space_saved)}")
        
        if not self.simulation_mode:
            print(f"  🔒 Sauvegarde: {self.backup_dir}")
            
    def format_size(self, size_bytes):
        """Formate une taille en bytes"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 complete_optimizer.py <directory>")
        print("Example: python3 complete_optimizer.py ~/Pictures")
        sys.exit(1)
        
    target = sys.argv[1]
    if not os.path.exists(target):
        print(f"❌ Directory not found: {target}")
        sys.exit(1)
        
    optimizer = CompleteOptimizer(target)
    
    print("🔒 MODE SIMULATION ACTIVÉ (aucune suppression)")
    print("   Pour exécuter réellement: modifier simulation_mode = False")
    print()
    
    if optimizer.analyze_directory():
        print(f"\n🎯 Analyse terminée - Consultez les recommandations ci-dessus")
    else:
        print("❌ Erreur durant l'analyse")
        sys.exit(1)

if __name__ == "__main__":
    main()