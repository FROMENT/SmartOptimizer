#!/usr/bin/env python3
"""
Test Suite for SmartOptimizer Project Structure
Valide que tous les composants sont correctement organisés
"""

import os
import sys
from pathlib import Path

class SmartOptimizerTests:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.test_results = []
        
    def test_directory_structure(self):
        """Test que la structure de répertoires est correcte"""
        required_dirs = [
            'src',
            'src/analyzers',
            'src/optimizers', 
            'src/reorganizers',
            'src/utils',
            'scripts',
            'docker',
            'docs',
            'examples',
            'tests'
        ]
        
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if full_path.exists():
                self.test_results.append(f"✅ {dir_path}")
            else:
                self.test_results.append(f"❌ {dir_path} - MANQUANT")
                
    def test_core_files(self):
        """Test que les fichiers principaux existent"""
        required_files = [
            'README.md',
            'install.sh',
            
            # Analyzers
            'src/analyzers/ultra_quick_overview.py',
            'src/analyzers/comprehensive_analyzer.py',
            'src/analyzers/cloud_services_detector.py',
            'src/analyzers/cloud_nesting_analyzer.py',
            
            # Optimizers
            'src/optimizers/quick_smart_optimizer.py',
            'src/optimizers/complete_optimizer.py',
            'src/optimizers/cloud_optimizer.py',
            'src/optimizers/cloud_deduplication_optimizer.py',
            
            # Reorganizers
            'src/reorganizers/smart_reorganizer.py',
            
            # Utils
            'src/utils/check_cloud_sync_status.py',
            
            # Scripts
            'scripts/quick_cloud_safety_check.sh',
            'scripts/simple_safety_check.sh',
            'scripts/cleanup_doublons.sh',
            
            # Docker
            'docker/Dockerfile',
            'docker/docker-compose.yml',
            'docker/entrypoint.sh',
            
            # Documentation
            'docs/user-guide.md',
            'docs/security.md',
            
            # Examples
            'examples/weekend_cleanup.sh',
            'examples/developer_cleanup.sh',
            'examples/cloud_optimization_workflow.sh',
            'examples/cloud_deduplication_strategy.sh',
            
            # Upgrade
            'upgrade.sh'
        ]
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                self.test_results.append(f"✅ {file_path}")
            else:
                self.test_results.append(f"❌ {file_path} - MANQUANT")
                
    def test_file_permissions(self):
        """Test que les permissions sont correctes"""
        executable_files = [
            'install.sh',
            'upgrade.sh',
            'scripts/quick_cloud_safety_check.sh',
            'scripts/simple_safety_check.sh', 
            'scripts/cleanup_doublons.sh',
            'docker/entrypoint.sh',
            'examples/weekend_cleanup.sh',
            'examples/developer_cleanup.sh',
            'examples/cloud_optimization_workflow.sh',
            'examples/cloud_deduplication_strategy.sh',
            'src/analyzers/ultra_quick_overview.py',
            'src/analyzers/cloud_services_detector.py',
            'src/analyzers/cloud_nesting_analyzer.py',
            'src/optimizers/quick_smart_optimizer.py',
            'src/optimizers/cloud_optimizer.py',
            'src/optimizers/cloud_deduplication_optimizer.py',
            'src/reorganizers/smart_reorganizer.py'
        ]
        
        for file_path in executable_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                if os.access(full_path, os.X_OK):
                    self.test_results.append(f"✅ {file_path} - Exécutable")
                else:
                    self.test_results.append(f"🟡 {file_path} - Non exécutable")
            else:
                self.test_results.append(f"❌ {file_path} - Fichier manquant")
                
    def test_python_syntax(self):
        """Test que les fichiers Python ont une syntaxe valide"""
        python_files = [
            'src/analyzers/ultra_quick_overview.py',
            'src/analyzers/comprehensive_analyzer.py',
            'src/analyzers/cloud_services_detector.py',
            'src/analyzers/cloud_nesting_analyzer.py',
            'src/optimizers/quick_smart_optimizer.py',
            'src/optimizers/complete_optimizer.py',
            'src/optimizers/cloud_optimizer.py',
            'src/optimizers/cloud_deduplication_optimizer.py',
            'src/reorganizers/smart_reorganizer.py',
            'src/utils/check_cloud_sync_status.py'
        ]
        
        for file_path in python_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r') as f:
                        compile(f.read(), str(full_path), 'exec')
                    self.test_results.append(f"✅ {file_path} - Syntaxe OK")
                except SyntaxError as e:
                    self.test_results.append(f"❌ {file_path} - Erreur syntaxe: {e}")
                except Exception as e:
                    self.test_results.append(f"🟡 {file_path} - Avertissement: {e}")
            else:
                self.test_results.append(f"❌ {file_path} - Fichier manquant")
                
    def test_docker_files(self):
        """Test que les fichiers Docker sont valides"""
        docker_files = {
            'docker/Dockerfile': ['FROM python', 'COPY', 'RUN'],
            'docker/docker-compose.yml': ['version:', 'services:', 'smartoptimizer:'],
            'docker/entrypoint.sh': ['#!/bin/bash', 'case', 'overview']
        }
        
        for file_path, required_content in docker_files.items():
            full_path = self.project_root / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r') as f:
                        content = f.read()
                    
                    missing_content = []
                    for required in required_content:
                        if required not in content:
                            missing_content.append(required)
                    
                    if not missing_content:
                        self.test_results.append(f"✅ {file_path} - Contenu valide")
                    else:
                        self.test_results.append(f"🟡 {file_path} - Contenu manquant: {missing_content}")
                        
                except Exception as e:
                    self.test_results.append(f"❌ {file_path} - Erreur lecture: {e}")
            else:
                self.test_results.append(f"❌ {file_path} - Fichier manquant")
                
    def test_documentation_completeness(self):
        """Test que la documentation est complète"""
        doc_files = {
            'README.md': ['# SmartOptimizer', 'Installation', 'Usage'],
            'docs/user-guide.md': ['Guide Utilisateur', 'Installation', 'Workflow'],
            'docs/security.md': ['Sécurité', 'Cloud', 'Backup']
        }
        
        for file_path, required_sections in doc_files.items():
            full_path = self.project_root / file_path
            if full_path.exists():
                try:
                    with open(full_path, 'r') as f:
                        content = f.read()
                    
                    missing_sections = []
                    for section in required_sections:
                        if section not in content:
                            missing_sections.append(section)
                    
                    if not missing_sections:
                        self.test_results.append(f"✅ {file_path} - Documentation complète")
                    else:
                        self.test_results.append(f"🟡 {file_path} - Sections manquantes: {missing_sections}")
                        
                except Exception as e:
                    self.test_results.append(f"❌ {file_path} - Erreur lecture: {e}")
            else:
                self.test_results.append(f"❌ {file_path} - Fichier manquant")
                
    def run_all_tests(self):
        """Lance tous les tests"""
        print("🧪 TESTS DE VALIDATION SMARTOPTIMIZER")
        print("=" * 45)
        
        print("\n📁 Test de la structure de répertoires...")
        self.test_directory_structure()
        
        print("\n📄 Test des fichiers principaux...")
        self.test_core_files()
        
        print("\n🔒 Test des permissions...")
        self.test_file_permissions()
        
        print("\n🐍 Test de la syntaxe Python...")
        self.test_python_syntax()
        
        print("\n🐳 Test des fichiers Docker...")
        self.test_docker_files()
        
        print("\n📚 Test de la documentation...")
        self.test_documentation_completeness()
        
        # Résumé
        print(f"\n📊 RÉSULTATS DES TESTS")
        print("=" * 25)
        
        success_count = len([r for r in self.test_results if r.startswith('✅')])
        warning_count = len([r for r in self.test_results if r.startswith('🟡')])
        error_count = len([r for r in self.test_results if r.startswith('❌')])
        total_count = len(self.test_results)
        
        print(f"✅ Succès: {success_count}")
        print(f"🟡 Avertissements: {warning_count}")
        print(f"❌ Erreurs: {error_count}")
        print(f"📊 Total: {total_count}")
        
        # Affichage détaillé des résultats
        if warning_count > 0 or error_count > 0:
            print(f"\n📋 DÉTAILS DES TESTS:")
            for result in self.test_results:
                if not result.startswith('✅'):
                    print(f"  {result}")
                    
        # Verdict final
        success_rate = (success_count / total_count) * 100
        print(f"\n🎯 TAUX DE RÉUSSITE: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT - Projet prêt pour utilisation")
            return True
        elif success_rate >= 75:
            print("🟡 ACCEPTABLE - Quelques améliorations recommandées")
            return True
        else:
            print("❌ INSUFFISANT - Corrections nécessaires")
            return False

def main():
    tester = SmartOptimizerTests()
    success = tester.run_all_tests()
    
    print(f"\n🚀 SMARTOPTIMIZER v1.1.0")
    print("   Suite complète d'optimisation intelligente")
    print("   Développé avec Claude Code")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())