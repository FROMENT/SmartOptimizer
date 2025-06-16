#!/usr/bin/env python3
"""
Ultra Quick Home Overview - Vue d'ensemble ultra-rapide
Analyse uniquement le premier niveau + calculs approximatifs
"""

import os
from pathlib import Path
from datetime import datetime
import subprocess
import sys

class UltraQuickOverview:
    def __init__(self, home_path):
        self.home_path = Path(home_path)
        self.findings = {}
        
    def ultra_quick_scan(self):
        """Scan ultra-rapide - premier niveau uniquement"""
        print(f"🚀 OVERVIEW ULTRA-RAPIDE: {self.home_path}")
        print("=" * 50)
        
        # 1. Scan du premier niveau avec du -h
        self.scan_top_level_sizes()
        
        # 2. Détection rapide des types de contenu
        self.detect_content_types()
        
        # 3. Suggestions immédiates
        self.immediate_suggestions()
        
    def scan_top_level_sizes(self):
        """Utilise 'du -h' pour les tailles rapides"""
        print("📊 Tailles des dossiers principaux:")
        
        try:
            # Utiliser du pour obtenir les tailles rapidement
            result = subprocess.run(['du', '-h', '-d', '1', str(self.home_path)], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                sizes = []
                
                for line in lines[:-1]:  # Exclure la ligne totale
                    parts = line.split('\t')
                    if len(parts) == 2:
                        size_str, path = parts
                        dir_name = Path(path).name
                        if dir_name and not dir_name.startswith('.'):
                            sizes.append((size_str, dir_name, path))
                            
                # Trier par taille (approximatif)
                def size_sort_key(item):
                    size_str = item[0]
                    if size_str.endswith('G'):
                        return float(size_str[:-1]) * 1000
                    elif size_str.endswith('M'):
                        return float(size_str[:-1])
                    elif size_str.endswith('K'):
                        return float(size_str[:-1]) / 1000
                    else:
                        return 0
                        
                sizes.sort(key=size_sort_key, reverse=True)
                
                # Afficher top 15
                for i, (size, name, path) in enumerate(sizes[:15], 1):
                    content_type = self.guess_content_type(name, path)
                    print(f"  {i:2d}. {size:>6s}  {name:25s} [{content_type}]")
                    
                self.findings['large_directories'] = sizes[:10]
                
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            print("  ⚠️  Impossible d'obtenir les tailles rapidement")
            # Fallback manuel
            self.manual_quick_scan()
            
    def manual_quick_scan(self):
        """Scan manuel de fallback"""
        dirs = []
        for item in self.home_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Estimation très rapide
                try:
                    # Compter juste quelques fichiers pour estimer
                    file_count = len(list(item.iterdir())[:100])
                    estimated_size = "~" + str(file_count * 10) + "M"
                    dirs.append((estimated_size, item.name, str(item)))
                except:
                    dirs.append(("?", item.name, str(item)))
                    
        for i, (size, name, path) in enumerate(dirs[:15], 1):
            content_type = self.guess_content_type(name, path)
            print(f"  {i:2d}. {size:>6s}  {name:25s} [{content_type}]")
            
    def detect_content_types(self):
        """Détection rapide des types de contenu"""
        print("\n🔍 Types de contenu détectés:")
        
        detected = {
            'development': [],
            'ai_ml': [],
            'media': [],
            'documents': [],
            'utilities': [],
            'other': []
        }
        
        for item in self.home_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                content_type = self.guess_content_type(item.name, str(item))
                detected[content_type].append(item.name)
                
        # Afficher par catégorie
        icons = {
            'development': '💻',
            'ai_ml': '🤖', 
            'media': '📸',
            'documents': '📄',
            'utilities': '🔧',
            'other': '📁'
        }
        
        for category, items in detected.items():
            if items:
                icon = icons.get(category, '📁')
                print(f"  {icon} {category.replace('_', ' ').title()}: {len(items)} dossiers")
                if len(items) <= 5:
                    print(f"     {', '.join(items)}")
                else:
                    print(f"     {', '.join(items[:5])} et {len(items)-5} autres...")
                    
        self.findings['content_types'] = detected
        
    def guess_content_type(self, name, path):
        """Devine le type de contenu d'un dossier"""
        name_lower = name.lower()
        
        # Développement
        dev_keywords = ['project', 'code', 'dev', 'src', 'github', 'git', 'script']
        if any(kw in name_lower for kw in dev_keywords):
            return 'development'
            
        # IA/ML
        ai_keywords = ['ai', 'ml', 'pinokio', 'ollama', 'stable', 'diffusion', 'model', 'gpt']
        if any(kw in name_lower for kw in ai_keywords):
            return 'ai_ml'
            
        # Média
        media_keywords = ['photo', 'picture', 'video', 'music', 'movie', 'image', 'media']
        if any(kw in name_lower for kw in media_keywords):
            return 'media'
            
        # Documents
        doc_keywords = ['document', 'doc', 'paper', 'file', 'archive']
        if any(kw in name_lower for kw in doc_keywords):
            return 'documents'
            
        # Utilitaires
        util_keywords = ['tool', 'util', 'app', 'software', 'install']
        if any(kw in name_lower for kw in util_keywords):
            return 'utilities'
            
        # Noms spéciaux
        special_names = {
            'desktop': 'documents',
            'downloads': 'utilities', 
            'applications': 'utilities',
            'library': 'utilities',
            'public': 'documents',
            'movies': 'media',
            'pictures': 'media',
            'music': 'media'
        }
        
        return special_names.get(name_lower, 'other')
        
    def immediate_suggestions(self):
        """Suggestions immédiates basées sur l'analyse rapide"""
        print("\n💡 Suggestions immédiates d'optimisation:")
        
        suggestions = []
        
        # Analyser les gros dossiers
        if 'large_directories' in self.findings:
            large_dirs = self.findings['large_directories']
            
            # Gros consommateurs d'espace
            very_large = [d for d in large_dirs[:5] if 'G' in d[0]]
            if very_large:
                suggestions.append(f"🔴 {len(very_large)} dossiers très volumineux détectés")
                for size, name, _ in very_large:
                    suggestions.append(f"    • {name} ({size}) - vérifier le contenu")
                    
        # Analyser les types de contenu
        if 'content_types' in self.findings:
            content = self.findings['content_types']
            
            # Trop de projets de dev dispersés
            if len(content['development']) > 3:
                suggestions.append(f"🟡 {len(content['development'])} dossiers de développement dispersés")
                suggestions.append("    → Consolider dans ~/Projects/")
                
            # Outils IA/ML présents
            if content['ai_ml']:
                suggestions.append(f"🟡 {len(content['ai_ml'])} outils IA/ML détectés")
                suggestions.append("    → Vérifier l'espace utilisé par les modèles")
                
            # Beaucoup de dossiers divers
            if len(content['other']) > 10:
                suggestions.append(f"🟡 {len(content['other'])} dossiers non classifiés")
                suggestions.append("    → Organiser avec une structure claire")
                
        # Détections spécifiques
        self.detect_specific_issues()
        
        # Afficher les suggestions
        if not suggestions:
            suggestions.append("✅ Structure relativement bien organisée")
            
        for suggestion in suggestions:
            print(f"  {suggestion}")
            
    def detect_specific_issues(self):
        """Détecte des problèmes spécifiques courants"""
        
        # Vérifier Desktop encombré
        desktop = self.home_path / 'Desktop'
        if desktop.exists():
            try:
                items = list(desktop.iterdir())
                if len(items) > 20:
                    print(f"  🟡 Desktop encombré ({len(items)} éléments)")
                    print("    → Organiser et archiver les fichiers anciens")
            except:
                pass
                
        # Vérifier Downloads volumineux
        downloads = self.home_path / 'Downloads'
        if downloads.exists():
            try:
                items = list(downloads.iterdir())
                if len(items) > 50:
                    print(f"  🟡 Downloads encombré ({len(items)} éléments)")
                    print("    → Nettoyer les fichiers anciens")
            except:
                pass
                
        # Vérifier présence d'outils de dev connus
        known_tools = {
            'pinokio': 'Gestionnaire d\'outils IA',
            'ollama': 'Runner de LLM local', 
            'docker': 'Conteneurs Docker',
            'node_modules': 'Dépendances Node.js',
            '.npm': 'Cache NPM',
            '.cache': 'Fichiers de cache'
        }
        
        for tool_name, description in known_tools.items():
            tool_path = self.home_path / tool_name
            if tool_path.exists():
                print(f"  ℹ️  {description} détecté: {tool_name}")
                
    def generate_action_plan(self):
        """Génère un plan d'action rapide"""
        print(f"\n📋 PLAN D'ACTION RECOMMANDÉ:")
        print("=" * 30)
        
        actions = [
            "1. 🔍 Analyse détaillée des gros dossiers:",
            "   python3 quick_smart_optimizer.py ~/[dossier_volumineux]",
            "",
            "2. 🗂️  Réorganisation intelligente:",
            "   python3 smart_reorganizer.py ~/",
            "",
            "3. 🧹 Nettoyage des doublons:",
            "   python3 cleanup_doublons.sh",
            "",
            "4. 📊 Analyse complète (si nécessaire):",
            "   python3 comprehensive_analyzer.py ~/Projects",
            "",
            "5. 🎯 Optimisation ciblée:",
            "   - Nettoyer Desktop et Downloads",
            "   - Archiver les projets anciens", 
            "   - Vérifier les outils IA/ML volumineux"
        ]
        
        for action in actions:
            print(f"  {action}")
            
        print(f"\n⏱️  Temps d'analyse: ~2 minutes")
        print(f"📁 Répertoire analysé: {self.home_path}")
        print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 ultra_quick_home_overview.py <directory>")
        print("Exemple: python3 ultra_quick_home_overview.py ~/")
        sys.exit(1)
        
    target = sys.argv[1]
    if not os.path.exists(target):
        print(f"❌ Répertoire inexistant: {target}")
        sys.exit(1)
        
    overview = UltraQuickOverview(target)
    overview.ultra_quick_scan()
    overview.generate_action_plan()

if __name__ == "__main__":
    main()