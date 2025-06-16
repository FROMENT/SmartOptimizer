#!/usr/bin/env python3
"""
Cloud Sync Status Checker
Vérifie l'état de synchronisation des services cloud avant optimisation
"""

import os
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import sys

class CloudSyncChecker:
    def __init__(self):
        self.cloud_paths = {
            'Google Drive': [
                '/Users/pascalfroment/Library/CloudStorage/GoogleDrive-pascal.froment@gmail.com',
                '/Users/pascalfroment/Google Drive'
            ],
            'iCloud Drive': [
                '/Users/pascalfroment/Library/Mobile Documents/com~apple~CloudDocs',
                '/Users/pascalfroment/iCloud Drive'
            ],
            'Dropbox': [
                '/Users/pascalfroment/Dropbox'
            ],
            'OneDrive': [
                '/Users/pascalfroment/OneDrive',
                '/Users/pascalfroment/Library/CloudStorage/OneDrive-Personal'
            ]
        }
        
        self.sync_status = {}
        
    def check_all_cloud_services(self):
        """Vérifie tous les services cloud détectés"""
        print("🔍 VÉRIFICATION DE L'ÉTAT DE SYNCHRONISATION CLOUD")
        print("=" * 55)
        
        found_services = []
        
        for service_name, possible_paths in self.cloud_paths.items():
            for path in possible_paths:
                if os.path.exists(path):
                    print(f"\n📁 {service_name} détecté: {path}")
                    status = self.check_service_sync_status(service_name, path)
                    self.sync_status[service_name] = status
                    found_services.append(service_name)
                    break
                    
        if not found_services:
            print("✅ Aucun service cloud détecté - Optimisation sûre")
            return True
            
        return self.evaluate_overall_safety()
        
    def check_service_sync_status(self, service_name, path):
        """Vérifie l'état de sync d'un service spécifique"""
        status = {
            'path': path,
            'is_syncing': False,
            'recent_changes': False,
            'sync_conflicts': False,
            'last_activity': None,
            'recommendations': []
        }
        
        # 1. Vérifier les fichiers de sync en cours
        status['is_syncing'] = self.check_active_sync(path, service_name)
        
        # 2. Vérifier les modifications récentes
        status['recent_changes'] = self.check_recent_file_changes(path)
        
        # 3. Vérifier les conflits de sync
        status['sync_conflicts'] = self.check_sync_conflicts(path)
        
        # 4. Obtenir la dernière activité
        status['last_activity'] = self.get_last_activity(path)
        
        # 5. Générer des recommandations
        status['recommendations'] = self.generate_recommendations(status, service_name)
        
        self.display_service_status(service_name, status)
        
        return status
        
    def check_active_sync(self, path, service_name):
        """Détecte si une synchronisation est en cours"""
        sync_indicators = {
            'Google Drive': ['.tmp', '.gdownload', 'desktop.ini'],
            'iCloud Drive': ['.icloud', '.download'],
            'Dropbox': ['.dropbox', '.dropbox.cache'],
            'OneDrive': ['.tmp', '.lock']
        }
        
        indicators = sync_indicators.get(service_name, [])
        
        try:
            for root, dirs, files in os.walk(path):
                # Limiter la profondeur pour éviter la lenteur
                level = len(Path(root).relative_to(path).parts)
                if level > 3:
                    dirs.clear()
                    continue
                    
                # Chercher les indicateurs de sync
                for file in files:
                    for indicator in indicators:
                        if indicator in file.lower():
                            print(f"  ⚠️  Fichier de sync détecté: {file}")
                            return True
                            
                # Vérifier les dossiers spéciaux
                for dir_name in dirs:
                    if any(indicator in dir_name.lower() for indicator in indicators):
                        print(f"  ⚠️  Dossier de sync détecté: {dir_name}")
                        return True
                        
        except (PermissionError, OSError):
            pass
            
        return False
        
    def check_recent_file_changes(self, path, minutes=10):
        """Vérifie s'il y a eu des modifications récentes"""
        recent_threshold = datetime.now() - timedelta(minutes=minutes)
        recent_files = []
        
        try:
            for root, dirs, files in os.walk(path):
                level = len(Path(root).relative_to(path).parts)
                if level > 2:  # Limiter la profondeur
                    dirs.clear()
                    continue
                    
                for file in files[:50]:  # Limiter le nombre de fichiers vérifiés
                    file_path = Path(root) / file
                    try:
                        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if mtime > recent_threshold:
                            recent_files.append((str(file_path), mtime))
                            
                        if len(recent_files) > 10:  # Arrêter si trop de fichiers récents
                            break
                    except:
                        continue
                        
                if len(recent_files) > 10:
                    break
                    
        except (PermissionError, OSError):
            pass
            
        if recent_files:
            print(f"  📝 {len(recent_files)} fichiers modifiés récemment (< {minutes}min)")
            for file_path, mtime in recent_files[:3]:
                rel_path = str(Path(file_path).relative_to(path))
                print(f"     • {rel_path} ({mtime.strftime('%H:%M:%S')})")
            if len(recent_files) > 3:
                print(f"     • ... et {len(recent_files) - 3} autres")
                
        return len(recent_files) > 0
        
    def check_sync_conflicts(self, path):
        """Détecte les conflits de synchronisation"""
        conflict_patterns = [
            'conflict', 'conflicted', 'duplicate', 
            'copy)', '(1)', '(2)', 'version'
        ]
        
        conflicts = []
        
        try:
            for root, dirs, files in os.walk(path):
                level = len(Path(root).relative_to(path).parts)
                if level > 2:
                    dirs.clear()
                    continue
                    
                for file in files:
                    file_lower = file.lower()
                    if any(pattern in file_lower for pattern in conflict_patterns):
                        conflicts.append(str(Path(root) / file))
                        
                    if len(conflicts) > 20:  # Limiter
                        break
                        
        except (PermissionError, OSError):
            pass
            
        if conflicts:
            print(f"  ⚠️  {len(conflicts)} conflits potentiels détectés:")
            for conflict in conflicts[:3]:
                rel_path = str(Path(conflict).relative_to(path))
                print(f"     • {rel_path}")
            if len(conflicts) > 3:
                print(f"     • ... et {len(conflicts) - 3} autres")
                
        return len(conflicts) > 0
        
    def get_last_activity(self, path):
        """Obtient la timestamp de la dernière activité"""
        try:
            # Vérifier quelques fichiers récents
            latest = None
            for root, dirs, files in os.walk(path):
                level = len(Path(root).relative_to(path).parts)
                if level > 1:
                    dirs.clear()
                    continue
                    
                for file in files[:20]:  # Limiter
                    try:
                        file_path = Path(root) / file
                        mtime = file_path.stat().st_mtime
                        if latest is None or mtime > latest:
                            latest = mtime
                    except:
                        continue
                        
            if latest:
                return datetime.fromtimestamp(latest)
        except:
            pass
            
        return None
        
    def generate_recommendations(self, status, service_name):
        """Génère des recommandations basées sur l'état"""
        recommendations = []
        
        if status['is_syncing']:
            recommendations.append("🔴 ATTENDRE - Synchronisation en cours")
            recommendations.append("   → Patienter que la sync se termine")
            
        if status['recent_changes']:
            recommendations.append("🟡 PRUDENCE - Modifications récentes détectées")
            recommendations.append("   → Vérifier que les changements sont synchronisés")
            
        if status['sync_conflicts']:
            recommendations.append("🟠 ATTENTION - Conflits de sync présents")
            recommendations.append("   → Résoudre les conflits avant optimisation")
            
        if status['last_activity']:
            time_since = datetime.now() - status['last_activity']
            if time_since.total_seconds() < 300:  # < 5 minutes
                recommendations.append("🟡 RÉCENT - Activité très récente")
                recommendations.append("   → Attendre 5-10 minutes pour stabilisation")
                
        if not any([status['is_syncing'], status['recent_changes'], status['sync_conflicts']]):
            recommendations.append("✅ SÛRE - Optimisation peut procéder")
            
        return recommendations
        
    def display_service_status(self, service_name, status):
        """Affiche l'état d'un service"""
        print(f"  📊 État de {service_name}:")
        print(f"     Sync active: {'🔴 OUI' if status['is_syncing'] else '✅ NON'}")
        print(f"     Changements récents: {'🟡 OUI' if status['recent_changes'] else '✅ NON'}")
        print(f"     Conflits: {'🟠 OUI' if status['sync_conflicts'] else '✅ NON'}")
        
        if status['last_activity']:
            time_ago = datetime.now() - status['last_activity']
            if time_ago.total_seconds() < 60:
                time_str = f"{int(time_ago.total_seconds())}s"
            elif time_ago.total_seconds() < 3600:
                time_str = f"{int(time_ago.total_seconds()/60)}min"
            else:
                time_str = f"{int(time_ago.total_seconds()/3600)}h"
            print(f"     Dernière activité: il y a {time_str}")
            
        print("  📋 Recommandations:")
        for rec in status['recommendations']:
            print(f"     {rec}")
            
    def evaluate_overall_safety(self):
        """Évalue la sécurité globale pour l'optimisation"""
        print(f"\n🎯 ÉVALUATION GLOBALE DE SÉCURITÉ")
        print("=" * 40)
        
        total_services = len(self.sync_status)
        safe_services = 0
        warnings = []
        blockers = []
        
        for service_name, status in self.sync_status.items():
            if status['is_syncing']:
                blockers.append(f"{service_name}: Synchronisation active")
            elif status['recent_changes']:
                warnings.append(f"{service_name}: Modifications récentes")
            elif status['sync_conflicts']:
                warnings.append(f"{service_name}: Conflits détectés")
            else:
                safe_services += 1
                
        # Verdict final
        if blockers:
            print("🔴 OPTIMISATION DÉCONSEILLÉE")
            print("   Raisons bloquantes:")
            for blocker in blockers:
                print(f"   • {blocker}")
            print("\n   ⏳ Recommandation: Attendre la fin des synchronisations")
            return False
            
        elif warnings:
            print("🟡 OPTIMISATION AVEC PRUDENCE")
            print("   Avertissements:")
            for warning in warnings:
                print(f"   • {warning}")
            print("\n   ⚠️  Recommandation: Faire une sauvegarde supplémentaire")
            
        else:
            print("✅ OPTIMISATION SÛRE")
            print(f"   Tous les services cloud ({safe_services}/{total_services}) sont stables")
            
        return True
        
    def generate_safety_report(self):
        """Génère un rapport de sécurité"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = f"/Users/pascalfroment/cloud_sync_safety_report_{timestamp}.txt"
        
        with open(report_path, 'w') as f:
            f.write("RAPPORT DE SÉCURITÉ SYNCHRONISATION CLOUD\n")
            f.write("=" * 50 + "\n")
            f.write(f"Date: {datetime.now()}\n\n")
            
            for service_name, status in self.sync_status.items():
                f.write(f"{service_name}:\n")
                f.write(f"  Path: {status['path']}\n")
                f.write(f"  Sync active: {status['is_syncing']}\n")
                f.write(f"  Changements récents: {status['recent_changes']}\n")
                f.write(f"  Conflits: {status['sync_conflicts']}\n")
                f.write(f"  Recommandations:\n")
                for rec in status['recommendations']:
                    f.write(f"    {rec}\n")
                f.write("\n")
                
        print(f"\n📄 Rapport sauvegardé: {report_path}")
        return report_path

def main():
    print("🔒 VÉRIFICATEUR DE SÉCURITÉ CLOUD SYNC")
    print("Analyse l'état de synchronisation avant optimisation\n")
    
    checker = CloudSyncChecker()
    is_safe = checker.check_all_cloud_services()
    
    # Générer le rapport
    checker.generate_safety_report()
    
    print(f"\n{'='*60}")
    if is_safe:
        print("✅ FEUX VERTS - Optimisation peut procéder en sécurité")
    else:
        print("🔴 ARRÊT RECOMMANDÉ - Attendre stabilisation des services cloud")
    print("="*60)
    
    return 0 if is_safe else 1

if __name__ == "__main__":
    sys.exit(main())