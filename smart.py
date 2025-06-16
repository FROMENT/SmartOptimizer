#!/usr/bin/env python3
"""
SmartOptimizer v1.2.0 - Interface Universelle Simple
Un seul fichier pour tout faire : installation, détection, optimisation

Auteur: Pascal Froment <pascal.froment@gmail.com>
GitHub: https://github.com/FROMENT/SmartOptimizer
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
import json

class SmartOptimizerUniversal:
    def __init__(self):
        self.system = platform.system().lower()
        self.home = Path.home()
        self.is_windows = self.system == 'windows'
        self.is_macos = self.system == 'darwin'
        self.is_linux = self.system == 'linux'
        
        # Gestion du mode simulation
        self.simulation_mode = self.load_simulation_mode()
        
        # Gestion des thèmes
        self.theme = self.load_theme()
        self.setup_colors()
        
    def setup_colors(self):
        """Configure les couleurs selon le thème"""
        # Couleurs de base
        base_colors = {
            'reset': '\033[0m',
            'bold': '\033[1m',
            'dim': '\033[2m',
            'underline': '\033[4m'
        }
        
        if self.theme == 'dark':
            # Thème sombre - couleurs vives
            theme_colors = {
                'primary': '\033[96m',      # Cyan vif
                'success': '\033[92m',      # Vert vif
                'warning': '\033[93m',      # Jaune vif
                'danger': '\033[91m',       # Rouge vif
                'danger_bg': '\033[41m',    # Fond rouge vif
                'success_bg': '\033[42m',   # Fond vert vif
                'info': '\033[94m',         # Bleu vif
                'text': '\033[97m',         # Blanc
                'muted': '\033[90m',        # Gris foncé
                'accent': '\033[95m'        # Magenta
            }
        elif self.theme == 'light':
            # Thème clair - couleurs plus sombres
            theme_colors = {
                'primary': '\033[36m',      # Cyan foncé
                'success': '\033[32m',      # Vert foncé
                'warning': '\033[33m',      # Jaune foncé
                'danger': '\033[31m',       # Rouge foncé
                'danger_bg': '\033[101m',   # Fond rouge clair
                'success_bg': '\033[102m',  # Fond vert clair
                'info': '\033[34m',         # Bleu foncé
                'text': '\033[30m',         # Noir
                'muted': '\033[37m',        # Gris clair
                'accent': '\033[35m'        # Magenta foncé
            }
        else:  # auto/système
            # Détection automatique du thème système
            system_dark = self.detect_system_dark_mode()
            if system_dark:
                theme_colors = {
                    'primary': '\033[96m',
                    'success': '\033[92m',
                    'warning': '\033[93m',
                    'danger': '\033[91m',
                    'danger_bg': '\033[41m',
                    'success_bg': '\033[42m',
                    'info': '\033[94m',
                    'text': '\033[97m',
                    'muted': '\033[90m',
                    'accent': '\033[95m'
                }
            else:
                theme_colors = {
                    'primary': '\033[36m',
                    'success': '\033[32m',
                    'warning': '\033[33m',
                    'danger': '\033[31m',
                    'danger_bg': '\033[101m',
                    'success_bg': '\033[102m',
                    'info': '\033[34m',
                    'text': '\033[30m',
                    'muted': '\033[37m',
                    'accent': '\033[35m'
                }
        
        # Couleurs spéciales pour le mode réel (toujours rouge vif)
        danger_real_colors = {
            'real_danger': '\033[1m\033[91m',        # Rouge vif + gras
            'real_danger_bg': '\033[1m\033[41m\033[97m',  # Fond rouge vif + texte blanc + gras
            'real_warning': '\033[1m\033[93m',       # Jaune vif + gras pour avertissements
            'blink': '\033[5m'                       # Clignotant (si supporté)
        }
        
        # Combiner toutes les couleurs
        self.colors = {**base_colors, **theme_colors, **danger_real_colors}
        
    def detect_system_dark_mode(self):
        """Détecte si le système utilise le mode sombre"""
        try:
            if self.is_macos:
                result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], 
                                      capture_output=True, text=True)
                return 'Dark' in result.stdout
            elif self.is_windows:
                # Sur Windows, vérifier le registre
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                       r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                    value = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
                    winreg.CloseKey(key)
                    return value == 0  # 0 = mode sombre
                except:
                    return False
            elif self.is_linux:
                # Sur Linux, vérifier les variables d'environnement
                color_scheme = os.getenv('GTK_THEME', '').lower()
                return 'dark' in color_scheme
        except:
            pass
        return False  # Par défaut, mode clair
        
    def load_theme(self):
        """Charge le thème depuis la configuration"""
        config_path = Path("smartoptimizer.conf")
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    content = f.read()
                    if "THEME=dark" in content:
                        return 'dark'
                    elif "THEME=light" in content:
                        return 'light'
                    elif "THEME=auto" in content:
                        return 'auto'
            except:
                pass
        return 'auto'  # Thème automatique par défaut
        
    def save_theme(self, theme):
        """Sauvegarde le thème dans la configuration"""
        config_path = Path("smartoptimizer.conf")
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    content = f.read()
                
                # Remplacer ou ajouter la ligne THEME
                lines = content.split('\n')
                theme_found = False
                new_lines = []
                
                for line in lines:
                    if line.startswith('THEME='):
                        new_lines.append(f"THEME={theme}")
                        theme_found = True
                    else:
                        new_lines.append(line)
                
                if not theme_found:
                    new_lines.append(f"THEME={theme}")
                
                with open(config_path, 'w') as f:
                    f.write('\n'.join(new_lines))
                    
            except Exception as e:
                print(f"⚠️  Erreur sauvegarde thème: {e}")
        else:
            self.create_config()
        
    def main_menu(self):
        """Menu principal avec gestion du mode simulation/réel et thèmes"""
        # Couleur selon le mode avec rouge vif pour mode réel
        if self.simulation_mode:
            mode_color = self.colors['success']
            mode_text = "🟢 MODE SIMULATION (Sécurisé)"
            bg_color = self.colors['success_bg']
        else:
            mode_color = self.colors['real_danger']
            mode_text = "🔴 MODE RÉEL (DANGER!)"
            bg_color = self.colors['real_danger_bg']
            
        # Affichage du thème actuel
        theme_info = {
            'auto': f"🌓 Auto ({self.get_current_theme_name()})",
            'dark': "🌙 Sombre", 
            'light': "☀️  Clair"
        }
        current_theme = theme_info.get(self.theme, self.theme)
            
        print(f"{self.colors['primary']}{self.colors['bold']}🚀 SmartOptimizer v1.2.0 - Interface Universelle{self.colors['reset']}")
        print("=" * 57)
        print(f"{self.colors['info']}🖥️  OS: {platform.system()} | Utilisateur: {os.getenv('USER', os.getenv('USERNAME'))}{self.colors['reset']}")
        print(f"{self.colors['muted']}👤 Auteur: Pascal Froment <pascal.froment@gmail.com>{self.colors['reset']}")
        print(f"{self.colors['muted']}🎨 Thème: {current_theme}{self.colors['reset']}")
        print()
        print(f"{bg_color} {mode_text} {self.colors['reset']}")
        print()
        print(f"{self.colors['text']}Que voulez-vous faire ?{self.colors['reset']}")
        print()
        print(f"{self.colors['text']}1️⃣  📊 Détecter mes services cloud{self.colors['reset']}")
        print(f"{self.colors['text']}2️⃣  🏢 Analyser OneDrive Business/Enterprise{self.colors['reset']}") 
        print(f"{self.colors['text']}3️⃣  🔍 Vue d'ensemble rapide{self.colors['reset']}")
        print(f"{self.colors['text']}4️⃣  🧹 Optimiser un dossier{self.colors['reset']}")
        print(f"{self.colors['text']}5️⃣  ⚙️  Installer/configurer SmartOptimizer{self.colors['reset']}")
        print(f"{self.colors['text']}6️⃣  📚 Afficher l'aide{self.colors['reset']}")
        print(f"{mode_color}7️⃣  🔄 Changer le mode (actuellement: {'SIMULATION' if self.simulation_mode else 'RÉEL'}){self.colors['reset']}")
        print(f"{self.colors['accent']}8️⃣  🎨 Changer le thème (actuellement: {current_theme}){self.colors['reset']}")
        print(f"{self.colors['muted']}0️⃣  ❌ Quitter{self.colors['reset']}")
        print()
        
        try:
            choice = input(f"{self.colors['primary']}Votre choix (1-8, 0 pour quitter) : {self.colors['reset']}").strip()
            
            if choice == "1":
                self.detect_cloud_services()
            elif choice == "2":
                self.analyze_onedrive_business()
            elif choice == "3":
                self.quick_overview()
            elif choice == "4":
                self.optimize_folder()
            elif choice == "5":
                self.install_configure()
            elif choice == "6":
                self.show_help()
            elif choice == "7":
                self.toggle_simulation_mode()
            elif choice == "8":
                self.change_theme()
            elif choice == "0":
                print(f"{self.colors['success']}👋 Au revoir !{self.colors['reset']}")
                return
            else:
                print(f"{self.colors['warning']}❌ Choix invalide{self.colors['reset']}")
                
        except KeyboardInterrupt:
            print("\n👋 Au revoir !")
            return
            
        # Revenir au menu
        input(f"\n{self.colors['muted']}Appuyez sur Entrée pour continuer...{self.colors['reset']}")
        self.main_menu()
        
    def get_current_theme_name(self):
        """Retourne le nom du thème actuellement appliqué"""
        if self.theme == 'auto':
            if self.detect_system_dark_mode():
                return "Sombre détecté"
            else:
                return "Clair détecté"
        return self.theme.title()
        
    def change_theme(self):
        """Interface pour changer le thème"""
        print(f"\n{self.colors['accent']}🎨 CHANGEMENT DE THÈME{self.colors['reset']}")
        print("=" * 25)
        
        current_theme_name = self.get_current_theme_name()
        print(f"{self.colors['text']}Thème actuel: {self.colors['info']}{self.theme} ({current_theme_name}){self.colors['reset']}")
        print()
        
        print(f"{self.colors['text']}Thèmes disponibles :{self.colors['reset']}")
        print(f"{self.colors['accent']}1{self.colors['reset']} - {self.colors['text']}🌓 Auto (s'adapte au système){self.colors['reset']}")
        print(f"{self.colors['accent']}2{self.colors['reset']} - {self.colors['text']}🌙 Sombre (couleurs vives){self.colors['reset']}")
        print(f"{self.colors['accent']}3{self.colors['reset']} - {self.colors['text']}☀️  Clair (couleurs sombres){self.colors['reset']}")
        print()
        
        if self.theme == 'auto':
            system_dark = self.detect_system_dark_mode()
            print(f"{self.colors['info']}ℹ️  Système détecté: {'🌙 Mode sombre' if system_dark else '☀️  Mode clair'}{self.colors['reset']}")
            print()
        
        try:
            choice = input(f"{self.colors['primary']}Votre choix (1-3) : {self.colors['reset']}").strip()
            
            if choice == "1":
                new_theme = "auto"
                theme_name = "🌓 Auto"
            elif choice == "2":
                new_theme = "dark" 
                theme_name = "🌙 Sombre"
            elif choice == "3":
                new_theme = "light"
                theme_name = "☀️  Clair"
            else:
                print(f"{self.colors['warning']}❌ Choix invalide{self.colors['reset']}")
                return
                
            # Appliquer le nouveau thème
            old_theme = self.theme
            self.theme = new_theme
            self.save_theme(new_theme)
            self.setup_colors()  # Reconfigurer les couleurs
            
            print(f"\n{self.colors['success']}✅ Thème changé: {theme_name}{self.colors['reset']}")
            
            if old_theme != new_theme:
                print(f"{self.colors['info']}ℹ️  Les nouvelles couleurs seront visibles au prochain menu{self.colors['reset']}")
                
        except KeyboardInterrupt:
            print(f"\n{self.colors['muted']}❌ Changement de thème annulé{self.colors['reset']}")
        
    def load_simulation_mode(self):
        """Charge le mode simulation depuis la configuration"""
        config_path = Path("smartoptimizer.conf")
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    content = f.read()
                    if "SIMULATION_MODE=true" in content:
                        return True
                    elif "SIMULATION_MODE=false" in content:
                        return False
            except:
                pass
        return True  # Mode simulation par défaut
        
    def save_simulation_mode(self, mode):
        """Sauvegarde le mode simulation dans la configuration"""
        config_path = Path("smartoptimizer.conf")
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    content = f.read()
                
                # Remplacer la ligne SIMULATION_MODE
                new_content = ""
                for line in content.split('\n'):
                    if line.startswith('SIMULATION_MODE='):
                        new_content += f"SIMULATION_MODE={'true' if mode else 'false'}\n"
                    else:
                        new_content += line + '\n'
                
                with open(config_path, 'w') as f:
                    f.write(new_content.rstrip() + '\n')
                    
            except Exception as e:
                print(f"⚠️  Erreur sauvegarde configuration: {e}")
        else:
            # Créer une configuration de base
            self.create_config()
            
    def toggle_simulation_mode(self):
        """Bascule entre mode simulation et mode réel"""
        print(f"\n{self.colors['primary']}🔄 CHANGEMENT DE MODE{self.colors['reset']}")
        print("=" * 25)
        
        current_mode = "SIMULATION" if self.simulation_mode else "RÉEL"
        new_mode = "RÉEL" if self.simulation_mode else "SIMULATION"
        
        print(f"{self.colors['text']}Mode actuel: {self.colors['success'] if self.simulation_mode else self.colors['real_danger']}{current_mode}{self.colors['reset']}")
        print(f"{self.colors['text']}Nouveau mode: {self.colors['real_danger'] if self.simulation_mode else self.colors['success']}{new_mode}{self.colors['reset']}")
        print()
        
        if self.simulation_mode:
            # Passage en mode réel - Avertissement renforcé
            print(f"{self.colors['real_danger_bg']} ⚠️  ATTENTION - MODE RÉEL DANGEREUX ⚠️  {self.colors['reset']}")
            print()
            print(f"{self.colors['text']}En mode réel, SmartOptimizer peut :{self.colors['reset']}")
            print(f"{self.colors['real_danger']}• Supprimer définitivement des fichiers{self.colors['reset']}")
            print(f"{self.colors['real_danger']}• Modifier la structure de vos dossiers{self.colors['reset']}")
            print(f"{self.colors['real_danger']}• Déplacer des documents importants{self.colors['reset']}")
            print(f"{self.colors['real_danger']}• Causer des pertes de données irréversibles{self.colors['reset']}")
            print()
            print(f"{self.colors['warning']}{self.colors['bold']}🛡️  Recommandations OBLIGATOIRES :{self.colors['reset']}")
            print(f"{self.colors['text']}   • Faire une sauvegarde Time Machine AVANT{self.colors['reset']}")
            print(f"{self.colors['text']}   • Tester sur un petit dossier d'abord{self.colors['reset']}")
            print(f"{self.colors['text']}   • Vérifier que vos clouds ne synchronisent pas{self.colors['reset']}")
            print(f"{self.colors['text']}   • Avoir des sauvegardes récentes{self.colors['reset']}")
            print()
            
            confirm = input(f"{self.colors['real_danger']}{self.colors['bold']}Êtes-vous CERTAIN de vouloir activer le mode réel ? (tapez 'OUI DANGER' en majuscules) : {self.colors['reset']}")
            
            if confirm == "OUI DANGER":
                self.simulation_mode = False
                self.save_simulation_mode(False)
                print(f"\n{self.colors['real_danger_bg']} 🔴 MODE RÉEL ACTIVÉ - DANGER ! {self.colors['reset']}")
                print(f"{self.colors['real_warning']}⚠️  Soyez EXTRÊMEMENT prudent avec vos actions !{self.colors['reset']}")
                print(f"{self.colors['real_danger']}⚠️  Toute suppression sera DÉFINITIVE !{self.colors['reset']}")
            else:
                print(f"\n{self.colors['success']}✅ Mode simulation conservé (sage décision){self.colors['reset']}")
        else:
            # Passage en mode simulation - Plus simple
            print(f"{self.colors['success']}Retour au mode simulation sécurisé ?{self.colors['reset']}")
            confirm = input(f"{self.colors['text']}Confirmer (o/n) : {self.colors['reset']}").lower()
            
            if confirm in ['o', 'oui', 'y', 'yes']:
                self.simulation_mode = True
                self.save_simulation_mode(True)
                print(f"\n{self.colors['success']}🟢 MODE SIMULATION ACTIVÉ{self.colors['reset']}")
                print(f"{self.colors['text']}✅ Vos fichiers sont maintenant protégés{self.colors['reset']}")
            else:
                print(f"\n{self.colors['real_danger']}🔴 Mode réel conservé{self.colors['reset']}")
                
    def optimize_folder(self):
        """Optimisation avec respect du mode simulation/réel"""
        mode_text = "SIMULATION" if self.simulation_mode else "RÉEL"
        mode_color = self.colors['green'] if self.simulation_mode else self.colors['red']
        
        print(f"\n🧹 OPTIMISATION DE DOSSIER - MODE {mode_color}{mode_text}{self.colors['reset']}")
        print("=" * 40)
        
        if not self.simulation_mode:
            print(f"{self.colors['bg_red']}{self.colors['white']} ⚠️  MODE RÉEL ACTIF - MODIFICATIONS PERMANENTES ⚠️  {self.colors['reset']}")
            print()
        
        print("💡 Dossiers suggérés :")
        print("   • Desktop (ou Entrée)")
        print("   • Downloads")
        print("   • Documents")
        print("   • Pictures")
        print("   • ou chemin complet comme /Users/nom/dossier")
        print()
        
        folder_path = input("📁 Chemin du dossier à analyser : ").strip()
        
        # Gérer les chemins courts et complets
        if not folder_path or folder_path.lower() == "desktop":
            if self.is_windows:
                folder_path = f"{self.home}\\Desktop"
            else:
                folder_path = f"{self.home}/Desktop"
        elif folder_path.lower() == "downloads":
            folder_path = f"{self.home}/Downloads"
        elif folder_path.lower() == "documents":
            folder_path = f"{self.home}/Documents"
        elif folder_path.lower() == "pictures":
            folder_path = f"{self.home}/Pictures"
        elif not folder_path.startswith('/') and not folder_path.startswith('C:'):
            folder_path = f"{self.home}/{folder_path}"
                
        path = Path(folder_path)
        
        if not path.exists():
            print(f"❌ Dossier introuvable: {path}")
            return
            
        print(f"🔍 Analyse de: {path}")
        print()
        
        # Recherche de doublons
        files_by_size = {}
        duplicates_found = 0
        space_recoverable = 0
        
        try:
            for file_path in path.rglob("*"):
                if file_path.is_file():
                    try:
                        size = file_path.stat().st_size
                        if size > 0:
                            if size not in files_by_size:
                                files_by_size[size] = []
                            files_by_size[size].append(file_path)
                    except:
                        continue
                        
            doublons_groupes = []
            for size, files in files_by_size.items():
                if len(files) > 1:
                    doublons_groupes.append(files)
                    duplicates_found += len(files) - 1
                    space_recoverable += size * (len(files) - 1)
                    
            print(f"📊 Résultats ({'SIMULATION' if self.simulation_mode else 'MODE RÉEL'}):")
            print(f"   🔍 Doublons potentiels: {duplicates_found}")
            print(f"   💾 Espace récupérable: {self.format_size(space_recoverable)}")
            print()
            
            if self.simulation_mode:
                print(f"{self.colors['green']}ℹ️  Mode simulation - Aucun fichier supprimé{self.colors['reset']}")
            else:
                if doublons_groupes:
                    print(f"{self.colors['red']}⚠️  MODE RÉEL - Suppression possible{self.colors['reset']}")
                    confirm = input(f"{self.colors['red']}Voulez-vous VRAIMENT supprimer {duplicates_found} doublons ? (tapez 'SUPPRIMER') : {self.colors['reset']}")
                    
                    if confirm == "SUPPRIMER":
                        files_deleted = 0
                        space_freed = 0
                        
                        for groupe in doublons_groupes:
                            # Garder le premier, supprimer les autres
                            for fichier in groupe[1:]:
                                try:
                                    size = fichier.stat().st_size
                                    fichier.unlink()
                                    files_deleted += 1
                                    space_freed += size
                                    print(f"{self.colors['red']}🗑️  Supprimé: {fichier.name}{self.colors['reset']}")
                                except Exception as e:
                                    print(f"❌ Erreur: {e}")
                                    
                        print(f"\n{self.colors['red']}✅ Suppression terminée !{self.colors['reset']}")
                        print(f"   📁 {files_deleted} fichiers supprimés")
                        print(f"   💾 {self.format_size(space_freed)} libérés")
                    else:
                        print("❌ Suppression annulée")
                else:
                    print("✅ Aucun doublon à supprimer")
                
        except Exception as e:
            print(f"⚠️  Erreur d'analyse: {e}")
        
    def detect_cloud_services(self):
        """Détection simple des services cloud"""
        print("\n☁️  DÉTECTION DES SERVICES CLOUD")
        print("=" * 35)
        
        services_found = []
        total_size = 0
        
        # Chemins cloud selon l'OS
        cloud_paths = self.get_cloud_paths()
        
        for service, paths in cloud_paths.items():
            for path_str in paths:
                path = Path(path_str)
                if path.exists() and path.is_dir():
                    try:
                        size = self.get_folder_size(path)
                        files = self.count_files(path)
                        
                        services_found.append({
                            'name': service,
                            'path': str(path),
                            'size': size,
                            'files': files
                        })
                        
                        total_size += size
                        
                        print(f"✅ {service}")
                        print(f"   📁 {path}")
                        print(f"   💾 {self.format_size(size)}")
                        print(f"   📄 {files:,} fichiers")
                        print()
                        
                    except Exception as e:
                        print(f"⚠️  {service} - Erreur: {e}")
                        
        if services_found:
            print(f"📊 RÉSUMÉ:")
            print(f"   Services détectés: {len(services_found)}")
            print(f"   Espace total: {self.format_size(total_size)}")
        else:
            print("ℹ️  Aucun service cloud détecté")
            
    def analyze_onedrive_business(self):
        """Analyse OneDrive Business simplifiée"""
        print("\n🏢 ANALYSE ONEDRIVE BUSINESS/ENTERPRISE")
        print("=" * 40)
        
        business_paths = []
        
        if self.is_windows:
            # Windows - chercher dans les dossiers utilisateur
            user_path = Path(f"C:\\Users\\{os.getenv('USERNAME', 'user')}")
            for item in user_path.glob("OneDrive - *"):
                if item.is_dir():
                    business_paths.append(item)
                    
        elif self.is_macos:
            # macOS - chercher dans CloudStorage
            cloudstorage = self.home / "Library/CloudStorage"
            for item in cloudstorage.glob("OneDrive-*"):
                if item.is_dir() and "Personal" not in item.name:
                    business_paths.append(item)
                    
        elif self.is_linux:
            # Linux - chercher les configurations OneDrive
            for pattern in ["OneDrive-*", ".onedrive*", "onedrive*"]:
                for item in self.home.glob(pattern):
                    if item.is_dir():
                        business_paths.append(item)
                        
        if business_paths:
            for path in business_paths:
                tenant_name = path.name.replace("OneDrive-", "").replace("OneDrive - ", "")
                size = self.get_folder_size(path)
                files = self.count_files(path)
                
                print(f"✅ Tenant: {tenant_name}")
                print(f"   📁 {path}")
                print(f"   💾 {self.format_size(size)}")
                print(f"   📄 {files:,} fichiers")
                print(f"   🔄 Type: Business/Enterprise")
                print()
        else:
            print("ℹ️  Aucun tenant OneDrive Business détecté")
            print("💡 Vérifiez que OneDrive Business est configuré")
            
    def quick_overview(self):
        """Vue d'ensemble rapide du système"""
        print("\n🔍 VUE D'ENSEMBLE RAPIDE")
        print("=" * 25)
        
        # Analyser le dossier home
        print(f"📁 Analyse de: {self.home}")
        print()
        
        # Trouver les plus gros dossiers
        large_folders = []
        
        try:
            for item in self.home.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    try:
                        size = self.get_folder_size(item, max_depth=2)
                        if size > 100 * 1024 * 1024:  # Plus de 100MB
                            large_folders.append((item.name, size))
                    except:
                        continue
                        
            # Trier par taille
            large_folders.sort(key=lambda x: x[1], reverse=True)
            
            print("📊 Plus gros dossiers:")
            for name, size in large_folders[:10]:
                print(f"   📁 {name:20} {self.format_size(size):>10}")
                
        except Exception as e:
            print(f"⚠️  Erreur d'analyse: {e}")
            
    def OLD_simulate_optimization(self):
        """Simulation d'optimisation"""
        print("\n🧹 SIMULATION D'OPTIMISATION")
        print("=" * 30)
        
        print("💡 Dossiers suggérés :")
        print("   • Desktop (ou Entrée)")
        print("   • Downloads")
        print("   • Documents")
        print("   • Pictures")
        print("   • ou chemin complet comme /Users/nom/dossier")
        print()
        
        folder_path = input("📁 Chemin du dossier à analyser : ").strip()
        
        # Gérer les chemins courts et complets
        if not folder_path or folder_path.lower() == "desktop":
            if self.is_windows:
                folder_path = f"{self.home}\\Desktop"
            else:
                folder_path = f"{self.home}/Desktop"
        elif folder_path.lower() == "downloads":
            folder_path = f"{self.home}/Downloads"
        elif folder_path.lower() == "documents":
            folder_path = f"{self.home}/Documents"
        elif folder_path.lower() == "pictures":
            folder_path = f"{self.home}/Pictures"
        elif not folder_path.startswith('/') and not folder_path.startswith('C:'):
            # Chemin relatif, l'ajouter au home
            folder_path = f"{self.home}/{folder_path}"
                
        path = Path(folder_path)
        
        if not path.exists():
            print(f"❌ Dossier introuvable: {path}")
            return
            
        print(f"🔍 Analyse de: {path}")
        print()
        
        # Recherche de doublons simples
        files_by_size = {}
        duplicates_found = 0
        space_recoverable = 0
        
        try:
            for file_path in path.rglob("*"):
                if file_path.is_file():
                    try:
                        size = file_path.stat().st_size
                        if size > 0:
                            if size not in files_by_size:
                                files_by_size[size] = []
                            files_by_size[size].append(file_path)
                    except:
                        continue
                        
            for size, files in files_by_size.items():
                if len(files) > 1:
                    duplicates_found += len(files) - 1
                    space_recoverable += size * (len(files) - 1)
                    
            print(f"📊 Résultats (SIMULATION SEULEMENT):")
            print(f"   🔍 Doublons potentiels: {duplicates_found}")
            print(f"   💾 Espace récupérable: {self.format_size(space_recoverable)}")
            print()
            print("ℹ️  Mode simulation - Aucun fichier supprimé")
            
        except Exception as e:
            print(f"⚠️  Erreur d'analyse: {e}")
            
    def install_configure(self):
        """Installation et configuration"""
        print("\n⚙️  INSTALLATION ET CONFIGURATION")
        print("=" * 35)
        
        print("🔍 Vérification de l'environnement...")
        
        # Vérifier Python
        python_version = sys.version_info
        if python_version >= (3, 7):
            print(f"✅ Python {platform.python_version()}")
        else:
            print(f"❌ Python {platform.python_version()} - Version 3.7+ requise")
            return
            
        # Créer la configuration
        config_path = Path("smartoptimizer.conf")
        if config_path.exists():
            print(f"✅ Configuration existante: {config_path}")
        else:
            self.create_config()
            print(f"✅ Configuration créée: {config_path}")
            
        # Rendre exécutables (Unix)
        if not self.is_windows:
            try:
                os.chmod(__file__, 0o755)
                print("✅ Permissions d'exécution configurées")
            except:
                pass
                
        print()
        print("🎉 SmartOptimizer est configuré et prêt à utiliser !")
        print()
        print("💡 Commandes rapides:")
        if self.is_windows:
            print(f"   python {__file__}")
        else:
            print(f"   python3 {__file__}")
            print(f"   ./{Path(__file__).name}")
            
    def show_help(self):
        """Affichage de l'aide"""
        print("\n📚 AIDE SMARTOPTIMIZER")
        print("=" * 23)
        print()
        print("🎯 FONCTIONNALITÉS:")
        print("• Détection automatique des services cloud")
        print("• Support OneDrive Business/Enterprise")
        print("• Optimisation multi-OS (Windows/macOS/Linux)")
        print("• Mode simulation sécurisé")
        print()
        print("🔧 UTILISATION:")
        if self.is_windows:
            print("   python smart.py")
        else:
            print("   python3 smart.py")
            print("   ./smart.py")
        print()
        print("🆘 SUPPORT:")
        print("• Mode simulation activé par défaut")
        print("• Aucune suppression sans confirmation")
        print("• Sauvegardes recommandées avant optimisation")
        print()
        print("🌍 COMPATIBILITÉ:")
        print("• Windows 10/11")
        print("• macOS 12+")
        print("• Linux (Ubuntu/Debian/Fedora/Arch)")
        
    def get_cloud_paths(self):
        """Chemins cloud selon l'OS"""
        username = os.getenv('USER') or os.getenv('USERNAME') or 'user'
        
        if self.is_windows:
            return {
                "iCloud Drive": [f"C:\\Users\\{username}\\iCloudDrive"],
                "Google Drive": [f"C:\\Users\\{username}\\Google Drive"],
                "OneDrive": [f"C:\\Users\\{username}\\OneDrive"],
                "Dropbox": [f"C:\\Users\\{username}\\Dropbox"]
            }
        elif self.is_macos:
            return {
                "iCloud Drive": [f"{self.home}/Library/Mobile Documents/com~apple~CloudDocs"],
                "Google Drive": [f"{self.home}/Google Drive", f"{self.home}/Library/CloudStorage/GoogleDrive-{username}@gmail.com"],
                "OneDrive": [f"{self.home}/OneDrive", f"{self.home}/Library/CloudStorage/OneDrive-Personal"],
                "Dropbox": [f"{self.home}/Dropbox"]
            }
        else:  # Linux
            return {
                "Google Drive": [f"{self.home}/GoogleDrive", f"{self.home}/Google Drive"],
                "OneDrive": [f"{self.home}/OneDrive", f"{self.home}/.onedrive"],
                "Dropbox": [f"{self.home}/Dropbox", f"{self.home}/.dropbox"]
            }
            
    def get_folder_size(self, path, max_depth=3):
        """Calcule la taille d'un dossier"""
        total_size = 0
        try:
            for root, dirs, files in os.walk(path):
                # Limiter la profondeur
                level = len(Path(root).relative_to(path).parts)
                if level >= max_depth:
                    dirs.clear()
                    
                for file in files[:100]:  # Limiter pour la performance
                    try:
                        file_path = Path(root) / file
                        total_size += file_path.stat().st_size
                    except:
                        continue
                        
                # Limiter pour éviter les timeouts
                if total_size > 50 * 1024**3:  # 50GB max
                    break
        except:
            pass
        return total_size
        
    def count_files(self, path, max_count=1000):
        """Compte les fichiers dans un dossier"""
        count = 0
        try:
            for root, dirs, files in os.walk(path):
                count += len(files)
                if count > max_count:
                    break
                # Limiter la profondeur
                level = len(Path(root).relative_to(path).parts)
                if level >= 3:
                    dirs.clear()
        except:
            pass
        return min(count, max_count)
        
    def format_size(self, size_bytes):
        """Formate une taille en bytes"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} PB"
        
    def create_config(self):
        """Crée le fichier de configuration"""
        config = f"""# SmartOptimizer Configuration
# Génération automatique: {platform.system()}

# Mode simulation (sécurisé)
SIMULATION_MODE=true

# Seuils de confiance
CONFIDENCE_THRESHOLD=70

# Optimisations cloud
CLOUD_OPTIMIZATION=true
ONEDRIVE_BUSINESS_SUPPORT=true

# Performance  
MAX_FILE_SCAN=5000
TIMEOUT_SECONDS=60
"""
        with open("smartoptimizer.conf", "w") as f:
            f.write(config)

def main():
    import argparse
    
    app = SmartOptimizerUniversal()
    
    # Permettre l'usage en ligne de commande
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description='SmartOptimizer Simple')
        parser.add_argument('--detect', action='store_true', help='Détecter les services cloud')
        parser.add_argument('--business', action='store_true', help='Analyser OneDrive Business')
        parser.add_argument('--overview', action='store_true', help='Vue d\'ensemble rapide')
        parser.add_argument('--install', action='store_true', help='Installer/configurer')
        
        args = parser.parse_args()
        
        if args.detect:
            app.detect_cloud_services()
        elif args.business:
            app.analyze_onedrive_business()
        elif args.overview:
            app.quick_overview()
        elif args.install:
            app.install_configure()
        else:
            app.show_help()
    else:
        # Interface interactive
        try:
            app.main_menu()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Au revoir !")

if __name__ == "__main__":
    main()