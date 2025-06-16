#!/usr/bin/env python3
"""
Comprehensive Home Directory Analyzer
Analyse complète : projets dev, utilitaires, Docker, structure existante
"""

import os
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys

class ComprehensiveAnalyzer:
    def __init__(self, home_path):
        self.home_path = Path(home_path)
        self.analysis = {
            'development_projects': [],
            'docker_projects': [],
            'utilities_scripts': [],
            'ai_ml_tools': [],
            'virtual_environments': [],
            'node_projects': [],
            'existing_structure': {},
            'optimization_opportunities': [],
            'proposed_improvements': []
        }
        
    def analyze_development_projects(self):
        """Analyse les projets de développement"""
        self.log("🔍 Analyse des projets de développement...")
        
        dev_indicators = {
            'git_repos': [],
            'node_projects': [],
            'python_projects': [],
            'docker_projects': [],
            'web_projects': [],
            'ai_ml_projects': []
        }
        
        # Scanner pour projets de dev
        for root, dirs, files in os.walk(self.home_path):
            root_path = Path(root)
            
            # Ignorer les dossiers système et caches
            if self.should_skip_directory(root_path):
                dirs.clear()  # Ne pas descendre dans ces dossiers
                continue
                
            # Détecter les types de projets
            project_info = {
                'path': str(root_path),
                'relative_path': str(root_path.relative_to(self.home_path)),
                'type': [],
                'technologies': [],
                'size_mb': self.get_directory_size(root_path),
                'last_modified': self.get_last_modified(root_path),
                'file_count': len(files)
            }
            
            # Git repository
            if '.git' in dirs:
                project_info['type'].append('git_repo')
                dev_indicators['git_repos'].append(project_info.copy())
                
            # Node.js project
            if 'package.json' in files:
                project_info['type'].append('node_project')
                project_info['technologies'].append('nodejs')
                dev_indicators['node_projects'].append(project_info.copy())
                
                # Analyser package.json
                try:
                    with open(root_path / 'package.json', 'r') as f:
                        package_data = json.load(f)
                        project_info['package_name'] = package_data.get('name', 'unknown')
                        project_info['dependencies'] = list(package_data.get('dependencies', {}).keys())
                except:
                    pass
                    
            # Python project
            python_indicators = ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile', 'environment.yml']
            if any(indicator in files for indicator in python_indicators):
                project_info['type'].append('python_project')
                project_info['technologies'].append('python')
                dev_indicators['python_projects'].append(project_info.copy())
                
            # Docker project
            docker_indicators = ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml', '.dockerignore']
            if any(indicator in files for indicator in docker_indicators):
                project_info['type'].append('docker_project')
                project_info['technologies'].append('docker')
                dev_indicators['docker_projects'].append(project_info.copy())
                
            # Web project
            web_indicators = ['index.html', 'index.htm', 'webpack.config.js', 'gulpfile.js', 'vite.config.js']
            if any(indicator in files for indicator in web_indicators):
                project_info['type'].append('web_project')
                project_info['technologies'].append('web')
                dev_indicators['web_projects'].append(project_info.copy())
                
            # AI/ML project
            ai_indicators = ['model.py', 'train.py', 'neural', 'tensorflow', 'pytorch', 'sklearn']
            ai_files = [f for f in files if any(indicator in f.lower() for indicator in ai_indicators)]
            if ai_files or 'models' in dirs or 'datasets' in dirs:
                project_info['type'].append('ai_ml_project')
                project_info['technologies'].append('ai_ml')
                project_info['ai_files'] = ai_files
                dev_indicators['ai_ml_projects'].append(project_info.copy())
                
            # Sauvegarder si c'est un projet
            if project_info['type']:
                self.analysis['development_projects'].append(project_info)
                
        # Statistiques
        for category, projects in dev_indicators.items():
            self.log(f"  {category}: {len(projects)} projets")
            
        return dev_indicators
        
    def analyze_utilities_and_tools(self):
        """Analyse les utilitaires et outils"""
        self.log("🔧 Analyse des utilitaires et outils...")
        
        tools_found = {
            'scripts': [],
            'executables': [],
            'configurations': [],
            'virtual_environments': [],
            'package_managers': []
        }
        
        # Scripts et exécutables
        script_extensions = {'.sh', '.py', '.js', '.pl', '.rb', '.ps1', '.bat'}
        config_extensions = {'.conf', '.config', '.json', '.yaml', '.yml', '.toml', '.ini'}
        
        for root, dirs, files in os.walk(self.home_path):
            root_path = Path(root)
            
            if self.should_skip_directory(root_path):
                continue
                
            for file in files:
                file_path = root_path / file
                extension = file_path.suffix.lower()
                
                # Scripts
                if extension in script_extensions:
                    tools_found['scripts'].append({
                        'path': str(file_path),
                        'name': file,
                        'type': extension[1:],  # Sans le point
                        'size': file_path.stat().st_size,
                        'executable': os.access(file_path, os.X_OK)
                    })
                    
                # Configurations
                elif extension in config_extensions:
                    tools_found['configurations'].append({
                        'path': str(file_path),
                        'name': file,
                        'type': extension[1:],
                        'size': file_path.stat().st_size
                    })
                    
            # Environnements virtuels
            venv_indicators = ['venv', '.venv', 'env', '.env', 'virtualenv']
            for venv_name in venv_indicators:
                if venv_name in dirs:
                    venv_path = root_path / venv_name
                    if (venv_path / 'bin' / 'python').exists() or (venv_path / 'Scripts' / 'python.exe').exists():
                        tools_found['virtual_environments'].append({
                            'path': str(venv_path),
                            'name': venv_name,
                            'size_mb': self.get_directory_size(venv_path),
                            'python_version': self.get_python_version(venv_path)
                        })
                        
            # Package managers
            package_managers = {
                'node_modules': 'npm',
                '__pycache__': 'python',
                '.next': 'nextjs',
                'build': 'build_output',
                'dist': 'distribution'
            }
            
            for pm_dir, pm_type in package_managers.items():
                if pm_dir in dirs:
                    pm_path = root_path / pm_dir
                    tools_found['package_managers'].append({
                        'path': str(pm_path),
                        'type': pm_type,
                        'size_mb': self.get_directory_size(pm_path)
                    })
                    
        # Statistiques
        for category, items in tools_found.items():
            self.log(f"  {category}: {len(items)} éléments")
            
        self.analysis['utilities_scripts'] = tools_found['scripts']
        self.analysis['virtual_environments'] = tools_found['virtual_environments']
        
        return tools_found
        
    def analyze_docker_ecosystem(self):
        """Analyse spécifique de l'écosystème Docker"""
        self.log("🐳 Analyse de l'écosystème Docker...")
        
        docker_analysis = {
            'docker_projects': [],
            'docker_compose_projects': [],
            'dockerfiles': [],
            'docker_volumes': [],
            'container_data': []
        }
        
        for root, dirs, files in os.walk(self.home_path):
            root_path = Path(root)
            
            if self.should_skip_directory(root_path):
                continue
                
            # Projets Docker
            docker_files = [f for f in files if f.lower().startswith('docker')]
            if docker_files:
                project_info = {
                    'path': str(root_path),
                    'docker_files': docker_files,
                    'has_dockerfile': 'Dockerfile' in files,
                    'has_compose': any('docker-compose' in f for f in files),
                    'has_dockerignore': '.dockerignore' in files,
                    'size_mb': self.get_directory_size(root_path)
                }
                
                # Analyser le Dockerfile
                if 'Dockerfile' in files:
                    dockerfile_info = self.analyze_dockerfile(root_path / 'Dockerfile')
                    project_info.update(dockerfile_info)
                    
                # Analyser docker-compose
                compose_files = [f for f in files if 'docker-compose' in f and f.endswith(('.yml', '.yaml'))]
                if compose_files:
                    compose_info = self.analyze_docker_compose(root_path / compose_files[0])
                    project_info.update(compose_info)
                    
                docker_analysis['docker_projects'].append(project_info)
                
        self.analysis['docker_projects'] = docker_analysis['docker_projects']
        self.log(f"  Projets Docker: {len(docker_analysis['docker_projects'])}")
        
        return docker_analysis
        
    def analyze_ai_ml_ecosystem(self):
        """Analyse spécifique de l'écosystème AI/ML"""
        self.log("🤖 Analyse de l'écosystème AI/ML...")
        
        ai_tools = {
            'model_directories': [],
            'datasets': [],
            'notebooks': [],
            'ai_frameworks': [],
            'large_models': []
        }
        
        # Chercher les outils AI spécifiques détectés
        ai_directories = ['pinokio', 'ollama', 'stable-diffusion', 'comfyui', 'automatic1111']
        
        for ai_dir in ai_directories:
            ai_path = self.home_path / ai_dir
            if ai_path.exists():
                ai_info = {
                    'name': ai_dir,
                    'path': str(ai_path),
                    'size_mb': self.get_directory_size(ai_path),
                    'type': self.classify_ai_tool(ai_dir),
                    'models_found': self.find_models_in_directory(ai_path)
                }
                ai_tools['ai_frameworks'].append(ai_info)
                
        # Chercher les notebooks Jupyter
        for root, dirs, files in os.walk(self.home_path):
            if self.should_skip_directory(Path(root)):
                continue
                
            notebooks = [f for f in files if f.endswith('.ipynb')]
            if notebooks:
                ai_tools['notebooks'].extend([{
                    'path': str(Path(root) / nb),
                    'name': nb,
                    'directory': str(Path(root).relative_to(self.home_path))
                } for nb in notebooks])
                
        self.analysis['ai_ml_tools'] = ai_tools
        
        # Statistiques
        total_ai_size = sum(tool['size_mb'] for tool in ai_tools['ai_frameworks'])
        self.log(f"  Outils AI/ML: {len(ai_tools['ai_frameworks'])} ({total_ai_size:.1f} GB)")
        self.log(f"  Notebooks Jupyter: {len(ai_tools['notebooks'])}")
        
        return ai_tools
        
    def propose_optimization_strategy(self):
        """Propose une stratégie d'optimisation globale"""
        self.log("💡 Proposition de stratégie d'optimisation...")
        
        opportunities = []
        
        # 1. Consolidation des projets de développement
        dev_projects = self.analysis['development_projects']
        scattered_projects = [p for p in dev_projects if not p['relative_path'].startswith('Projects/')]
        
        if scattered_projects:
            opportunities.append({
                'type': 'dev_consolidation',
                'priority': 'high',
                'description': f'{len(scattered_projects)} projets de dev dispersés',
                'action': 'Consolider dans ~/Projects/ avec sous-dossiers par technologie',
                'affected_projects': scattered_projects[:5]  # Top 5
            })
            
        # 2. Nettoyage des environnements virtuels
        venvs = self.analysis['virtual_environments']
        large_venvs = [v for v in venvs if v['size_mb'] > 500]
        
        if large_venvs:
            opportunities.append({
                'type': 'venv_cleanup',
                'priority': 'medium',
                'description': f'{len(large_venvs)} environnements virtuels volumineux',
                'action': 'Nettoyer ou archiver les venvs inutilisés',
                'space_recoverable_gb': sum(v['size_mb'] for v in large_venvs) / 1024,
                'affected_venvs': large_venvs
            })
            
        # 3. Optimisation Docker
        docker_projects = self.analysis['docker_projects']
        if docker_projects:
            opportunities.append({
                'type': 'docker_optimization',
                'priority': 'medium',
                'description': f'{len(docker_projects)} projets Docker à organiser',
                'action': 'Centraliser dans ~/Docker/ avec structure par projet',
                'affected_projects': docker_projects
            })
            
        # 4. Gestion des outils AI/ML
        ai_tools = self.analysis['ai_ml_tools']['ai_frameworks']
        large_ai_tools = [t for t in ai_tools if t['size_mb'] > 5000]  # > 5GB
        
        if large_ai_tools:
            total_size = sum(t['size_mb'] for t in large_ai_tools) / 1024
            opportunities.append({
                'type': 'ai_tools_management',
                'priority': 'high' if total_size > 50 else 'medium',
                'description': f'{len(large_ai_tools)} outils AI volumineux ({total_size:.1f} GB)',
                'action': 'Déplacer vers stockage externe ou optimiser',
                'space_used_gb': total_size,
                'affected_tools': large_ai_tools
            })
            
        # 5. Structure proposée améliorée
        improved_structure = self.design_improved_structure()
        opportunities.append({
            'type': 'structure_improvement',
            'priority': 'low',
            'description': 'Structure d\'arborescence optimisée',
            'action': 'Implémenter la nouvelle structure proposée',
            'new_structure': improved_structure
        })
        
        self.analysis['optimization_opportunities'] = opportunities
        
        return opportunities
        
    def design_improved_structure(self):
        """Conçoit une structure améliorée basée sur l'analyse"""
        return {
            'Projects': {
                'Active': {
                    'Web_Development': 'Projets web actifs',
                    'AI_ML_Research': 'Recherche et expérimentation IA',
                    'Mobile_Apps': 'Applications mobiles',
                    'Scripts_Automation': 'Scripts et automatisation'
                },
                'Archive': {
                    'Completed': 'Projets terminés',
                    'Learning': 'Projets d\'apprentissage',
                    'Experiments': 'Expérimentations'
                }
            },
            'Development_Tools': {
                'Docker': {
                    'Projects': 'Projets Docker',
                    'Configs': 'Configurations Docker',
                    'Scripts': 'Scripts de gestion'
                },
                'Virtual_Environments': {
                    'Python': 'Environnements Python',
                    'Node': 'Environnements Node.js',
                    'Others': 'Autres environnements'
                },
                'Configurations': {
                    'IDE_Settings': 'Configurations IDE',
                    'System_Configs': 'Configurations système',
                    'Project_Templates': 'Templates de projets'
                }
            },
            'AI_ML_Ecosystem': {
                'Tools': {
                    'Stable_Diffusion': 'Outils de génération d\'images',
                    'LLM_Tools': 'Outils de modèles de langage',
                    'Training_Tools': 'Outils d\'entraînement'
                },
                'Models': {
                    'Downloaded_Models': 'Modèles téléchargés',
                    'Custom_Models': 'Modèles personnalisés',
                    'Model_Configs': 'Configurations de modèles'
                },
                'Datasets': 'Jeux de données',
                'Experiments': 'Expérimentations et résultats'
            },
            'Utilities': {
                'Scripts': {
                    'System_Administration': 'Administration système',
                    'File_Management': 'Gestion de fichiers',
                    'Automation': 'Automatisation'
                },
                'Software': {
                    'Installers': 'Installateurs (.dmg, .pkg)',
                    'Portable_Apps': 'Applications portables',
                    'Tools': 'Outils divers'
                }
            }
        }
        
    def generate_comprehensive_report(self):
        """Génère un rapport complet"""
        output_dir = self.home_path / f"COMPREHENSIVE_ANALYSIS_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_dir.mkdir(exist_ok=True)
        
        # Rapport JSON complet
        with open(output_dir / "comprehensive_analysis.json", 'w') as f:
            json.dump(self.analysis, f, indent=2, default=str)
            
        # Rapport texte lisible
        with open(output_dir / "analysis_summary.txt", 'w') as f:
            f.write("ANALYSE COMPLÈTE DU RÉPERTOIRE HOME\n")
            f.write("=" * 50 + "\n")
            f.write(f"Répertoire: {self.home_path}\n")
            f.write(f"Date: {datetime.now()}\n\n")
            
            # Statistiques générales
            f.write("STATISTIQUES GÉNÉRALES:\n")
            f.write(f"  Projets de développement: {len(self.analysis['development_projects'])}\n")
            f.write(f"  Projets Docker: {len(self.analysis['docker_projects'])}\n")
            f.write(f"  Scripts/utilitaires: {len(self.analysis['utilities_scripts'])}\n")
            f.write(f"  Environnements virtuels: {len(self.analysis['virtual_environments'])}\n")
            f.write(f"  Outils AI/ML: {len(self.analysis['ai_ml_tools']['ai_frameworks'])}\n\n")
            
            # Opportunités d'optimisation
            f.write("OPPORTUNITÉS D'OPTIMISATION:\n")
            for opp in self.analysis['optimization_opportunities']:
                f.write(f"  [{opp['priority'].upper()}] {opp['description']}\n")
                f.write(f"    Action: {opp['action']}\n\n")
                
            # Projets par technologie
            f.write("PROJETS PAR TECHNOLOGIE:\n")
            tech_count = defaultdict(int)
            for project in self.analysis['development_projects']:
                for tech in project['technologies']:
                    tech_count[tech] += 1
                    
            for tech, count in sorted(tech_count.items()):
                f.write(f"  {tech}: {count} projets\n")
                
        # Script d'optimisation
        self.generate_optimization_script(output_dir)
        
        self.log(f"📋 Rapport complet généré: {output_dir}")
        return output_dir
        
    def generate_optimization_script(self, output_dir):
        """Génère un script d'optimisation personnalisé"""
        script_path = output_dir / "optimize_home.sh"
        
        with open(script_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Script d'optimisation personnalisé pour votre environnement\n\n")
            
            f.write("echo \"🚀 OPTIMISATION PERSONNALISÉE DU HOME\"\n")
            f.write("echo \"======================================\"\n\n")
            
            # Section projets de dev
            scattered_projects = [p for p in self.analysis['development_projects'] 
                                if not p['relative_path'].startswith('Projects/')]
            
            if scattered_projects:
                f.write("echo \"📁 CONSOLIDATION DES PROJETS DE DÉVELOPPEMENT\"\n")
                f.write("mkdir -p ~/Projects/{Web,AI_ML,Mobile,Scripts,Docker,Archive}\n\n")
                
                for project in scattered_projects[:10]:  # Top 10
                    rel_path = project['relative_path']
                    if 'docker' in project['technologies']:
                        target = "~/Projects/Docker/"
                    elif 'ai_ml' in project['technologies']:
                        target = "~/Projects/AI_ML/"
                    elif 'web' in project['technologies']:
                        target = "~/Projects/Web/"
                    else:
                        target = "~/Projects/Scripts/"
                        
                    f.write(f"echo \"  Déplacement suggéré: {rel_path} → {target}\"\n")
                    f.write(f"# mv \"{project['path']}\" \"{target}\"\n\n")
                    
            # Section nettoyage venvs
            large_venvs = [v for v in self.analysis['virtual_environments'] if v['size_mb'] > 500]
            if large_venvs:
                f.write("echo \"🧹 NETTOYAGE DES ENVIRONNEMENTS VIRTUELS\"\n")
                for venv in large_venvs:
                    f.write(f"echo \"  Env volumineux: {venv['path']} ({venv['size_mb']:.0f} MB)\"\n")
                    f.write(f"# Vérifiez si nécessaire, sinon: rm -rf \"{venv['path']}\"\n")
                f.write("\n")
                
            # Section outils AI
            ai_tools = self.analysis['ai_ml_tools']['ai_frameworks']
            if ai_tools:
                f.write("echo \"🤖 ORGANISATION DES OUTILS AI/ML\"\n")
                f.write("mkdir -p ~/AI_Tools/{Models,Tools,Datasets,Experiments}\n")
                for tool in ai_tools:
                    f.write(f"echo \"  Outil AI: {tool['name']} ({tool['size_mb']/1024:.1f} GB)\"\n")
                f.write("\n")
                
        os.chmod(script_path, 0o755)
        
    # Méthodes utilitaires
    def should_skip_directory(self, path):
        """Détermine si un dossier doit être ignoré"""
        skip_patterns = [
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            'Library/Caches', 'Library/Application Support',
            '.npm', '.cache', '.local/share', '.config',
            'Pictures/Photos Library.photoslibrary'
        ]
        
        path_str = str(path)
        return any(pattern in path_str for pattern in skip_patterns)
        
    def get_directory_size(self, path):
        """Calcule la taille d'un dossier en MB"""
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
            return total_size / (1024 * 1024)  # MB
        except:
            return 0
            
    def get_last_modified(self, path):
        """Obtient la date de dernière modification"""
        try:
            return datetime.fromtimestamp(path.stat().st_mtime)
        except:
            return datetime.now()
            
    def get_python_version(self, venv_path):
        """Détermine la version Python d'un venv"""
        try:
            python_exe = venv_path / 'bin' / 'python'
            if not python_exe.exists():
                python_exe = venv_path / 'Scripts' / 'python.exe'
                
            if python_exe.exists():
                import subprocess
                result = subprocess.run([str(python_exe), '--version'], 
                                      capture_output=True, text=True, timeout=5)
                return result.stdout.strip()
        except:
            pass
        return 'unknown'
        
    def analyze_dockerfile(self, dockerfile_path):
        """Analyse un Dockerfile"""
        try:
            with open(dockerfile_path, 'r') as f:
                content = f.read()
                
            return {
                'base_image': self.extract_base_image(content),
                'exposed_ports': self.extract_exposed_ports(content),
                'has_volumes': 'VOLUME' in content,
                'dockerfile_size': len(content)
            }
        except:
            return {}
            
    def analyze_docker_compose(self, compose_path):
        """Analyse un docker-compose.yml"""
        try:
            import yaml
            with open(compose_path, 'r') as f:
                compose_data = yaml.safe_load(f)
                
            services = compose_data.get('services', {})
            return {
                'service_count': len(services),
                'service_names': list(services.keys()),
                'has_volumes': 'volumes' in compose_data,
                'has_networks': 'networks' in compose_data
            }
        except:
            return {'service_count': 0}
            
    def extract_base_image(self, dockerfile_content):
        """Extrait l'image de base d'un Dockerfile"""
        for line in dockerfile_content.split('\n'):
            if line.strip().startswith('FROM'):
                return line.split()[1] if len(line.split()) > 1 else 'unknown'
        return 'unknown'
        
    def extract_exposed_ports(self, dockerfile_content):
        """Extrait les ports exposés d'un Dockerfile"""
        ports = []
        for line in dockerfile_content.split('\n'):
            if line.strip().startswith('EXPOSE'):
                ports.extend(line.split()[1:])
        return ports
        
    def classify_ai_tool(self, tool_name):
        """Classifie un outil AI"""
        classifications = {
            'pinokio': 'AI Tool Manager',
            'ollama': 'Local LLM Runner',
            'stable-diffusion': 'Image Generation',
            'comfyui': 'Node-based AI Interface',
            'automatic1111': 'Stable Diffusion WebUI'
        }
        return classifications.get(tool_name.lower(), 'AI Tool')
        
    def find_models_in_directory(self, ai_path):
        """Trouve les modèles dans un dossier AI"""
        model_extensions = {'.safetensors', '.ckpt', '.pth', '.bin', '.gguf'}
        models = []
        
        try:
            for root, dirs, files in os.walk(ai_path):
                if len(models) > 50:  # Limiter pour éviter les listes trop longues
                    break
                    
                for file in files:
                    if Path(file).suffix.lower() in model_extensions:
                        file_path = Path(root) / file
                        try:
                            size_mb = file_path.stat().st_size / (1024 * 1024)
                            models.append({
                                'name': file,
                                'size_mb': size_mb,
                                'path': str(file_path.relative_to(ai_path))
                            })
                        except:
                            continue
        except:
            pass
            
        return models[:20]  # Top 20 modèles
        
    def log(self, message):
        """Log avec timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        
    def run_comprehensive_analysis(self):
        """Lance l'analyse complète"""
        self.log("🚀 ANALYSE COMPLÈTE DU RÉPERTOIRE HOME")
        
        if not self.home_path.exists():
            self.log(f"❌ Répertoire inexistant: {self.home_path}")
            return
            
        # Exécuter toutes les analyses
        self.analyze_development_projects()
        self.analyze_utilities_and_tools()
        self.analyze_docker_ecosystem()
        self.analyze_ai_ml_ecosystem()
        self.propose_optimization_strategy()
        
        # Générer le rapport
        report_dir = self.generate_comprehensive_report()
        
        # Résumé final
        print(f"\n{'='*60}")
        print("🎯 ANALYSE COMPLÈTE TERMINÉE!")
        print(f"📊 Résumé:")
        print(f"   • {len(self.analysis['development_projects'])} projets de développement")
        print(f"   • {len(self.analysis['docker_projects'])} projets Docker")
        print(f"   • {len(self.analysis['utilities_scripts'])} scripts/utilitaires")
        print(f"   • {len(self.analysis['virtual_environments'])} environnements virtuels")
        print(f"   • {len(self.analysis['ai_ml_tools']['ai_frameworks'])} outils AI/ML")
        print(f"   • {len(self.analysis['optimization_opportunities'])} opportunités d'optimisation")
        print(f"📁 Rapport complet: {report_dir}")
        print("="*60)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 comprehensive_analyzer.py <home_directory>")
        print("Exemple: python3 comprehensive_analyzer.py ~/")
        sys.exit(1)
        
    home_dir = sys.argv[1]
    if not os.path.exists(home_dir):
        print(f"❌ Répertoire inexistant: {home_dir}")
        sys.exit(1)
        
    analyzer = ComprehensiveAnalyzer(home_dir)
    analyzer.run_comprehensive_analysis()

if __name__ == "__main__":
    main()