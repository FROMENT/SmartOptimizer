#!/usr/bin/env python3
"""
Code Review Complet - SmartOptimizer v1.2.0
Analyse complète du code, documentation et cohérence

Auteur: Pascal Froment <pascal.froment@gmail.com>
GitHub: https://github.com/FROMENT/SmartOptimizer
"""

import os
import sys
import ast
import re
from pathlib import Path
import subprocess

class CompleteCodeReview:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.issues = {
            'critical': [],
            'major': [],
            'minor': [],
            'suggestions': []
        }
        self.stats = {
            'python_files': 0,
            'total_lines': 0,
            'functions': 0,
            'classes': 0,
            'docstrings': 0
        }
        
    def review_complete(self):
        """Revue complète du projet"""
        print("🔍 REVUE COMPLÈTE SMARTOPTIMIZER v1.2.0")
        print("=" * 45)
        print("👤 Auteur: Pascal Froment <pascal.froment@gmail.com>")
        print("🌐 GitHub: https://github.com/FROMENT/SmartOptimizer")
        print()
        
        # Étapes de revue
        self.review_project_structure()
        self.review_python_code()
        self.review_documentation()
        self.review_configuration()
        self.review_git_setup()
        self.review_security()
        self.review_performance()
        self.review_cross_platform()
        
        # Rapport final
        self.generate_report()
        
    def review_project_structure(self):
        """Revue de la structure du projet"""
        print("📁 STRUCTURE DU PROJET")
        print("-" * 25)
        
        required_structure = {
            'files': [
                'README.md', 'LICENSE', 'CONTRIBUTING.md', '.gitignore',
                'smart.py', 'install_universal.py', 'CHANGELOG.md'
            ],
            'dirs': [
                'src', 'src/analyzers', 'src/optimizers', 'src/utils',
                'scripts', 'examples', 'docs', 'docker'
            ]
        }
        
        # Vérifier les fichiers requis
        missing_files = []
        for file_name in required_structure['files']:
            if not (self.project_root / file_name).exists():
                missing_files.append(file_name)
                
        # Vérifier les dossiers requis
        missing_dirs = []
        for dir_name in required_structure['dirs']:
            if not (self.project_root / dir_name).exists():
                missing_dirs.append(dir_name)
                
        if missing_files:
            self.issues['major'].append(f"Fichiers manquants: {', '.join(missing_files)}")
        
        if missing_dirs:
            self.issues['major'].append(f"Dossiers manquants: {', '.join(missing_dirs)}")
            
        print(f"✅ Fichiers essentiels: {len(required_structure['files']) - len(missing_files)}/{len(required_structure['files'])}")
        print(f"✅ Dossiers requis: {len(required_structure['dirs']) - len(missing_dirs)}/{len(required_structure['dirs'])}")
        print()
        
    def review_python_code(self):
        """Revue du code Python"""
        print("🐍 CODE PYTHON")
        print("-" * 15)
        
        # Filtrer uniquement les fichiers Python du projet SmartOptimizer
        python_files = []
        project_files = [
            'smart.py', 'install_universal.py', 'dedoublonner.py', 'dedoublons_rapide.py',
            'verify_project.py', 'code_review.py', 'prepare_github.py'
        ]
        
        # Ajouter les fichiers principaux
        for file_name in project_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                python_files.append(file_path)
                
        # Ajouter les fichiers du dossier src
        src_dir = self.project_root / 'src'
        if src_dir.exists():
            python_files.extend(src_dir.rglob("*.py"))
            
        self.stats['python_files'] = len(python_files)
        
        for py_file in python_files:
            self.analyze_python_file(py_file)
            
        print(f"📄 Fichiers Python: {self.stats['python_files']}")
        print(f"📝 Lignes totales: {self.stats['total_lines']}")
        print(f"🔧 Fonctions: {self.stats['functions']}")
        print(f"🏗️  Classes: {self.stats['classes']}")
        print(f"📚 Docstrings: {self.stats['docstrings']}")
        print()
        
    def analyze_python_file(self, file_path):
        """Analyse un fichier Python"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Compter les lignes
            lines = content.split('\n')
            self.stats['total_lines'] += len(lines)
            
            # Parser le code
            try:
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        self.stats['functions'] += 1
                        if ast.get_docstring(node):
                            self.stats['docstrings'] += 1
                        else:
                            self.issues['minor'].append(f"Fonction sans docstring: {node.name} dans {file_path.name}")
                            
                    elif isinstance(node, ast.ClassDef):
                        self.stats['classes'] += 1
                        if ast.get_docstring(node):
                            self.stats['docstrings'] += 1
                        else:
                            self.issues['minor'].append(f"Classe sans docstring: {node.name} dans {file_path.name}")
                            
            except SyntaxError as e:
                self.issues['critical'].append(f"Erreur syntaxe dans {file_path.name}: {e}")
                
            # Vérifier les informations d'auteur
            if 'pascal.froment@gmail.com' not in content:
                self.issues['suggestions'].append(f"Information auteur manquante dans {file_path.name}")
                
            # Vérifier les imports
            self.check_imports(content, file_path.name)
            
        except Exception as e:
            self.issues['major'].append(f"Erreur lecture {file_path.name}: {e}")
            
    def check_imports(self, content, filename):
        """Vérifie les imports"""
        lines = content.split('\n')
        has_shebang = lines[0].startswith('#!')
        
        if filename.endswith('.py') and not has_shebang and 'main' not in filename:
            self.issues['minor'].append(f"Shebang manquant dans {filename}")
            
        # Vérifier les imports OS-spécifiques
        if 'import winreg' in content and 'self.is_windows' not in content:
            self.issues['major'].append(f"Import winreg sans vérification OS dans {filename}")
            
    def review_documentation(self):
        """Revue de la documentation"""
        print("📚 DOCUMENTATION")
        print("-" * 17)
        
        doc_files = [
            'README.md', 'CHANGELOG.md', 'CONTRIBUTING.md',
            'MULTI_OS_GUIDE.md', 'ONEDRIVE_BUSINESS_GUIDE.md',
            'INSTALL_FACILE.md', 'GUIDE_DEDOUBLONNAGE.md'
        ]
        
        existing_docs = 0
        for doc_file in doc_files:
            doc_path = self.project_root / doc_file
            if doc_path.exists():
                existing_docs += 1
                self.check_documentation_content(doc_path)
            else:
                self.issues['major'].append(f"Documentation manquante: {doc_file}")
                
        print(f"📖 Guides disponibles: {existing_docs}/{len(doc_files)}")
        
        # Vérifier cohérence des versions
        self.check_version_consistency()
        print()
        
    def check_documentation_content(self, doc_path):
        """Vérifie le contenu d'un document"""
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifier la version
            if 'v1.2.0' not in content and 'VERSION' not in doc_path.name.upper():
                self.issues['minor'].append(f"Version manquante dans {doc_path.name}")
                
            # Vérifier l'auteur
            if 'Pascal Froment' not in content:
                self.issues['suggestions'].append(f"Information auteur manquante dans {doc_path.name}")
                
            # Vérifier les liens
            broken_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            for link_text, link_url in broken_links:
                if link_url.startswith('./') or link_url.endswith('.md'):
                    # Vérifier si le fichier local existe
                    link_path = self.project_root / link_url.lstrip('./')
                    if not link_path.exists():
                        self.issues['minor'].append(f"Lien brisé dans {doc_path.name}: {link_url}")
                        
        except Exception as e:
            self.issues['major'].append(f"Erreur lecture documentation {doc_path.name}: {e}")
            
    def check_version_consistency(self):
        """Vérifie la cohérence des versions"""
        version_files = {
            'CHANGELOG.md': r'## \[(\d+\.\d+\.\d+)\]',
            'PROJECT_SUMMARY.md': r'v(\d+\.\d+\.\d+)',
            'smart.py': r'SmartOptimizer v(\d+\.\d+\.\d+)'
        }
        
        versions = {}
        for file_name, pattern in version_files.items():
            file_path = self.project_root / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    matches = re.findall(pattern, content)
                    if matches:
                        versions[file_name] = matches[0]
                except:
                    pass
                    
        # Vérifier que toutes les versions sont 1.2.0
        inconsistent_versions = [f for f, v in versions.items() if v != '1.2.0']
        if inconsistent_versions:
            self.issues['major'].append(f"Versions incohérentes: {inconsistent_versions}")
            
    def review_configuration(self):
        """Revue de la configuration"""
        print("⚙️  CONFIGURATION")
        print("-" * 15)
        
        config_path = self.project_root / 'smartoptimizer.conf'
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config_content = f.read()
                    
                required_settings = [
                    'SIMULATION_MODE', 'CLOUD_OPTIMIZATION', 
                    'ONEDRIVE_BUSINESS_SUPPORT', 'CROSS_PLATFORM_MODE'
                ]
                
                missing_settings = []
                for setting in required_settings:
                    if setting not in config_content:
                        missing_settings.append(setting)
                        
                if missing_settings:
                    self.issues['minor'].append(f"Paramètres manquants: {missing_settings}")
                    
                print(f"✅ Configuration présente: {len(required_settings) - len(missing_settings)}/{len(required_settings)}")
                
            except Exception as e:
                self.issues['major'].append(f"Erreur lecture configuration: {e}")
        else:
            self.issues['major'].append("Fichier de configuration manquant")
            
        print()
        
    def review_git_setup(self):
        """Revue de la configuration Git"""
        print("🌐 CONFIGURATION GIT")
        print("-" * 20)
        
        git_dir = self.project_root / '.git'
        if git_dir.exists():
            print("✅ Repository Git initialisé")
            
            # Vérifier .gitignore
            gitignore_path = self.project_root / '.gitignore'
            if gitignore_path.exists():
                print("✅ .gitignore présent")
            else:
                self.issues['major'].append(".gitignore manquant")
                
            # Vérifier LICENSE
            license_path = self.project_root / 'LICENSE'
            if license_path.exists():
                print("✅ LICENSE présent")
            else:
                self.issues['major'].append("LICENSE manquant")
                
        else:
            self.issues['critical'].append("Repository Git non initialisé")
            
        print()
        
    def review_security(self):
        """Revue de sécurité"""
        print("🛡️  SÉCURITÉ")
        print("-" * 10)
        
        security_checks = {
            'Mode simulation par défaut': False,
            'Confirmations pour suppressions': False,
            'Gestion des permissions': False,
            'Protection timeouts': False
        }
        
        # Vérifier smart.py pour les mesures de sécurité
        smart_path = self.project_root / 'smart.py'
        if smart_path.exists():
            with open(smart_path, 'r') as f:
                content = f.read()
                
            if 'simulation_mode = True' in content or 'SIMULATION_MODE=true' in content:
                security_checks['Mode simulation par défaut'] = True
                
            if 'OUI DANGER' in content or 'SUPPRIMER' in content:
                security_checks['Confirmations pour suppressions'] = True
                
            if 'timeout' in content.lower():
                security_checks['Protection timeouts'] = True
                
        security_score = sum(security_checks.values())
        print(f"🔒 Score sécurité: {security_score}/{len(security_checks)}")
        
        for check, passed in security_checks.items():
            if not passed:
                self.issues['major'].append(f"Mesure sécurité manquante: {check}")
                
        print()
        
    def review_performance(self):
        """Revue des performances"""
        print("⚡ PERFORMANCE")
        print("-" * 13)
        
        performance_indicators = {
            'Limitations de profondeur': False,
            'Timeouts configurés': False,
            'Échantillonnage fichiers': False,
            'Hash optimisé': False
        }
        
        # Chercher dans les fichiers Python du projet uniquement
        python_files = []
        project_files = [
            'smart.py', 'install_universal.py', 'dedoublonner.py', 'dedoublons_rapide.py',
            'verify_project.py', 'code_review.py', 'prepare_github.py'
        ]
        
        for file_name in project_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                python_files.append(file_path)
                
        src_dir = self.project_root / 'src'
        if src_dir.exists():
            python_files.extend(src_dir.rglob("*.py"))
        
        for py_file in python_files:
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    
                if 'max_depth' in content or 'level >' in content:
                    performance_indicators['Limitations de profondeur'] = True
                    
                if 'timeout' in content:
                    performance_indicators['Timeouts configurés'] = True
                    
                if 'files[:' in content or 'range(' in content:
                    performance_indicators['Échantillonnage fichiers'] = True
                    
                if 'hashlib' in content or 'md5' in content:
                    performance_indicators['Hash optimisé'] = True
                    
            except:
                continue
                
        perf_score = sum(performance_indicators.values())
        print(f"🚀 Score performance: {perf_score}/{len(performance_indicators)}")
        print()
        
    def review_cross_platform(self):
        """Revue du support cross-platform"""
        print("🌍 SUPPORT MULTI-OS")
        print("-" * 19)
        
        platform_features = {
            'Détection OS automatique': False,
            'Chemins spécifiques par OS': False,
            'OneDrive Business multi-OS': False,
            'Installation universelle': False
        }
        
        # Vérifier platform_detector.py
        platform_detector_path = self.project_root / 'src/utils/platform_detector.py'
        if platform_detector_path.exists():
            platform_features['Détection OS automatique'] = True
            platform_features['Chemins spécifiques par OS'] = True
            
        # Vérifier universal_cloud_detector.py
        universal_detector_path = self.project_root / 'src/analyzers/universal_cloud_detector.py'
        if universal_detector_path.exists():
            platform_features['OneDrive Business multi-OS'] = True
            
        # Vérifier install_universal.py
        install_universal_path = self.project_root / 'install_universal.py'
        if install_universal_path.exists():
            platform_features['Installation universelle'] = True
            
        platform_score = sum(platform_features.values())
        print(f"🌐 Score multi-OS: {platform_score}/{len(platform_features)}")
        print()
        
    def generate_report(self):
        """Génère le rapport final"""
        print("📊 RAPPORT FINAL DE REVUE")
        print("=" * 25)
        
        total_issues = sum(len(issues) for issues in self.issues.values())
        
        if self.issues['critical']:
            print(f"\n🔴 CRITIQUE ({len(self.issues['critical'])}):")
            for issue in self.issues['critical']:
                print(f"   • {issue}")
                
        if self.issues['major']:
            print(f"\n🟠 MAJEUR ({len(self.issues['major'])}):")
            for issue in self.issues['major'][:5]:  # Limiter à 5
                print(f"   • {issue}")
            if len(self.issues['major']) > 5:
                print(f"   ... et {len(self.issues['major']) - 5} autres")
                
        if self.issues['minor']:
            print(f"\n🟡 MINEUR ({len(self.issues['minor'])}):")
            for issue in self.issues['minor'][:3]:  # Limiter à 3
                print(f"   • {issue}")
            if len(self.issues['minor']) > 3:
                print(f"   ... et {len(self.issues['minor']) - 3} autres")
                
        if self.issues['suggestions']:
            print(f"\n💡 SUGGESTIONS ({len(self.issues['suggestions'])}):")
            for suggestion in self.issues['suggestions'][:3]:
                print(f"   • {suggestion}")
            if len(self.issues['suggestions']) > 3:
                print(f"   ... et {len(self.issues['suggestions']) - 3} autres")
                
        # Score global ajusté pour la réalité du projet
        critical_weight = len(self.issues['critical']) * 15
        major_weight = len(self.issues['major']) * 8
        minor_weight = min(len(self.issues['minor']), 20) * 1  # Limiter l'impact des mineurs
        suggestion_weight = min(len(self.issues['suggestions']), 10) * 0.5  # Impact minimal
        
        total_weight = critical_weight + major_weight + minor_weight + suggestion_weight
        
        # Score de base selon les fonctionnalités principales
        base_score = 85  # Score de base pour un projet fonctionnel
        
        if total_weight == 0:
            score = 100
        else:
            score = max(20, base_score - total_weight)  # Score minimum de 20
            
        print(f"\n🎯 SCORE GLOBAL: {score}/100")
        
        if score >= 90:
            print("🏆 EXCELLENT - Projet de qualité exceptionnelle")
        elif score >= 80:
            print("✅ TRÈS BON - Projet de bonne qualité avec améliorations mineures")
        elif score >= 70:
            print("⚠️  BON - Projet fonctionnel nécessitant quelques corrections")
        elif score >= 60:
            print("🔧 MOYEN - Corrections importantes nécessaires")
        else:
            print("❌ INSUFFISANT - Refactoring majeur requis")
            
        print(f"\n📈 STATISTIQUES:")
        print(f"   📄 Fichiers Python: {self.stats['python_files']}")
        print(f"   📝 Lignes de code: {self.stats['total_lines']}")
        print(f"   🔧 Fonctions: {self.stats['functions']}")
        print(f"   🏗️  Classes: {self.stats['classes']}")
        print(f"   📚 Documentation: {self.stats['docstrings']}/{self.stats['functions'] + self.stats['classes']}")
        
        return score >= 80

def main():
    reviewer = CompleteCodeReview()
    is_quality = reviewer.review_complete()
    
    if is_quality:
        print("\n🎉 SmartOptimizer v1.2.0 - QUALITÉ CONFIRMÉE")
        return 0
    else:
        print("\n🔧 SmartOptimizer v1.2.0 - AMÉLIORATIONS NÉCESSAIRES")
        return 1

if __name__ == "__main__":
    sys.exit(main())