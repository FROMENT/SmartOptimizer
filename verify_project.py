#!/usr/bin/env python3
"""
Script de Vérification de Cohérence SmartOptimizer v1.2.0
Vérifie la structure, les références et la cohérence du projet
"""

import os
import sys
from pathlib import Path
import re

class ProjectVerifier:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.errors = []
        self.warnings = []
        self.info = []
        
    def verify_all(self):
        """Vérification complète du projet"""
        print("🔍 VÉRIFICATION DE COHÉRENCE SmartOptimizer v1.2.0")
        print("=" * 55)
        
        self.verify_structure()
        self.verify_versions()
        self.verify_file_references()
        self.verify_scripts_executable()
        self.verify_imports()
        
        self.display_results()
        
    def verify_structure(self):
        """Vérifie la structure des dossiers et fichiers essentiels"""
        print("📁 Vérification de la structure...")
        
        required_files = [
            'README.md',
            'smart.py', 
            'install_universal.py',
            'quick_install.sh',
            'dedoublons_rapide.py',
            'smartoptimizer.conf',
            'CHANGELOG.md',
            'PROJECT_SUMMARY.md',
            'WHATS_NEW_v1.2.0.md'
        ]
        
        required_dirs = [
            'src',
            'src/analyzers',
            'src/optimizers', 
            'src/utils',
            'scripts',
            'examples',
            'docs',
            'docker'
        ]
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                self.info.append(f"✅ {file_path}")
            else:
                self.errors.append(f"❌ Fichier manquant: {file_path}")
                
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if full_path.exists():
                self.info.append(f"✅ {dir_path}/")
            else:
                self.errors.append(f"❌ Dossier manquant: {dir_path}/")
                
    def verify_versions(self):
        """Vérifie la cohérence des versions"""
        print("🔢 Vérification des versions...")
        
        version_files = {
            'CHANGELOG.md': r'## \[(\d+\.\d+\.\d+)\]',
            'PROJECT_SUMMARY.md': r'SmartOptimizer v(\d+\.\d+\.\d+)',
            'smartoptimizer.conf': r'# SmartOptimizer v(\d+\.\d+\.\d+)',
            'WHATS_NEW_v1.2.0.md': r'SmartOptimizer v(\d+\.\d+\.\d+)'
        }
        
        versions_found = {}
        
        for file_name, pattern in version_files.items():
            file_path = self.project_root / file_name
            if file_path.exists():
                try:
                    content = file_path.read_text()
                    matches = re.findall(pattern, content)
                    if matches:
                        version = matches[0]
                        versions_found[file_name] = version
                        if version == "1.2.0":
                            self.info.append(f"✅ {file_name}: v{version}")
                        else:
                            self.warnings.append(f"⚠️  {file_name}: v{version} (attendu v1.2.0)")
                    else:
                        self.warnings.append(f"⚠️  {file_name}: version non trouvée")
                except Exception as e:
                    self.errors.append(f"❌ Erreur lecture {file_name}: {e}")
            else:
                self.warnings.append(f"⚠️  {file_name}: fichier non trouvé")
                
    def verify_file_references(self):
        """Vérifie que les fichiers référencés existent"""
        print("🔗 Vérification des références de fichiers...")
        
        # Fichiers à vérifier pour les références
        docs_to_check = [
            'README.md',
            'MULTI_OS_GUIDE.md',
            'INSTALL_FACILE.md',
            'GUIDE_DEDOUBLONNAGE.md',
            'QUICK_START.md'
        ]
        
        # Patterns de références de fichiers
        file_ref_patterns = [
            r'`([^`]+\.py)`',
            r'`([^`]+\.sh)`',
            r'`([^`]+\.md)`',
            r'\[([^\]]+\.md)\]',
            r'python3? ([^\s]+\.py)',
            r'\.\/([^\s]+\.sh)'
        ]
        
        for doc_file in docs_to_check:
            doc_path = self.project_root / doc_file
            if doc_path.exists():
                try:
                    content = doc_path.read_text()
                    
                    for pattern in file_ref_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            # Nettoyer le chemin
                            clean_path = match.strip()
                            if clean_path.startswith('./'):
                                clean_path = clean_path[2:]
                            if clean_path.startswith('src/'):
                                referenced_file = self.project_root / clean_path
                            else:
                                referenced_file = self.project_root / clean_path
                                
                            if referenced_file.exists():
                                self.info.append(f"✅ {doc_file} → {clean_path}")
                            else:
                                # Vérifier si c'est un fichier optionnel
                                if any(opt in clean_path for opt in ['example', 'optional', 'future']):
                                    self.warnings.append(f"⚠️  {doc_file} → {clean_path} (optionnel)")
                                else:
                                    self.errors.append(f"❌ {doc_file} → {clean_path} (introuvable)")
                                    
                except Exception as e:
                    self.errors.append(f"❌ Erreur lecture {doc_file}: {e}")
                    
    def verify_scripts_executable(self):
        """Vérifie que les scripts sont exécutables"""
        print("🔐 Vérification des permissions...")
        
        executable_files = [
            'smart.py',
            'dedoublons_rapide.py', 
            'dedoublonner.py',
            'quick_install.sh',
            'install.sh',
            'upgrade.sh'
        ]
        
        for script in executable_files:
            script_path = self.project_root / script
            if script_path.exists():
                if os.access(script_path, os.X_OK):
                    self.info.append(f"✅ {script} (exécutable)")
                else:
                    self.warnings.append(f"⚠️  {script} (non exécutable)")
            else:
                if script in ['install.sh', 'upgrade.sh']:
                    self.warnings.append(f"⚠️  {script} (optionnel, non trouvé)")
                else:
                    self.errors.append(f"❌ {script} (requis, non trouvé)")
                    
    def verify_imports(self):
        """Vérifie que les imports Python fonctionnent"""
        print("🐍 Vérification des imports Python...")
        
        python_files = [
            'smart.py',
            'install_universal.py',
            'dedoublons_rapide.py',
            'src/analyzers/universal_cloud_detector.py',
            'src/utils/platform_detector.py'
        ]
        
        for py_file in python_files:
            py_path = self.project_root / py_file
            if py_path.exists():
                try:
                    # Vérification syntaxe de base
                    with open(py_path, 'r') as f:
                        content = f.read()
                        compile(content, py_path, 'exec')
                    self.info.append(f"✅ {py_file} (syntaxe OK)")
                except SyntaxError as e:
                    self.errors.append(f"❌ {py_file}: Erreur syntaxe - {e}")
                except Exception as e:
                    self.warnings.append(f"⚠️  {py_file}: {e}")
            else:
                self.errors.append(f"❌ {py_file} (requis, non trouvé)")
                
    def display_results(self):
        """Affiche les résultats de vérification"""
        print(f"\n📊 RÉSULTATS DE VÉRIFICATION")
        print("=" * 35)
        
        if self.errors:
            print(f"\n❌ ERREURS ({len(self.errors)}):")
            for error in self.errors[:10]:  # Limiter l'affichage
                print(f"   {error}")
            if len(self.errors) > 10:
                print(f"   ... et {len(self.errors) - 10} autres erreurs")
                
        if self.warnings:
            print(f"\n⚠️  AVERTISSEMENTS ({len(self.warnings)}):")
            for warning in self.warnings[:10]:
                print(f"   {warning}")
            if len(self.warnings) > 10:
                print(f"   ... et {len(self.warnings) - 10} autres avertissements")
                
        if self.info:
            print(f"\n✅ VALIDATIONS ({len(self.info)}):")
            for info in self.info[:10]:
                print(f"   {info}")
            if len(self.info) > 10:
                print(f"   ... et {len(self.info) - 10} autres validations")
                
        # Score global
        total_checks = len(self.errors) + len(self.warnings) + len(self.info)
        success_rate = (len(self.info) / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\n🎯 SCORE GLOBAL: {success_rate:.1f}%")
        
        if len(self.errors) == 0:
            print("🎉 PROJET COHÉRENT - Prêt pour utilisation !")
        elif len(self.errors) <= 3:
            print("⚠️  PROJET FONCTIONNEL - Quelques corrections mineures")
        else:
            print("❌ CORRECTIONS REQUISES - Problèmes de cohérence détectés")
            
        return len(self.errors) == 0

def main():
    verifier = ProjectVerifier()
    is_coherent = verifier.verify_all()
    
    if is_coherent:
        print(f"\n✅ SmartOptimizer v1.2.0 est cohérent et prêt !")
        return 0
    else:
        print(f"\n❌ Corrections nécessaires avant utilisation")
        return 1

if __name__ == "__main__":
    sys.exit(main())