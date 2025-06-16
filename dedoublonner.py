#!/usr/bin/env python3
"""
Dédoublonneur Simple - Analyse et nettoyage des doublons
Usage : python3 dedoublonner.py [dossier]
"""

import os
import sys
import hashlib
from pathlib import Path
from collections import defaultdict

class DedoublonneurSimple:
    def __init__(self):
        self.simulation_mode = True
        
    def analyser_dossier(self, dossier_path):
        """Analyse un dossier pour trouver les doublons"""
        print(f"🔍 ANALYSE DES DOUBLONS : {dossier_path}")
        print("=" * 50)
        
        path = Path(dossier_path)
        if not path.exists():
            print(f"❌ Dossier introuvable: {path}")
            return
            
        print("🕐 Calcul des empreintes des fichiers...")
        
        # Regrouper les fichiers par hash
        fichiers_par_hash = defaultdict(list)
        total_fichiers = 0
        
        try:
            for fichier in path.rglob("*"):
                if fichier.is_file() and not fichier.name.startswith('.'):
                    try:
                        # Calculer le hash MD5
                        hash_md5 = self.calculer_hash(fichier)
                        if hash_md5:
                            fichiers_par_hash[hash_md5].append(fichier)
                            total_fichiers += 1
                            
                        # Afficher le progrès
                        if total_fichiers % 100 == 0:
                            print(f"   📄 {total_fichiers} fichiers analysés...")
                            
                    except Exception as e:
                        continue
                        
        except KeyboardInterrupt:
            print("\n⏹️  Analyse interrompue par l'utilisateur")
            return
            
        # Identifier les doublons
        doublons_groupes = []
        espace_total_doublons = 0
        
        for hash_md5, fichiers in fichiers_par_hash.items():
            if len(fichiers) > 1:
                doublons_groupes.append(fichiers)
                # Calculer l'espace des doublons (garder 1, supprimer les autres)
                taille_fichier = fichiers[0].stat().st_size
                espace_total_doublons += taille_fichier * (len(fichiers) - 1)
                
        # Afficher les résultats
        print(f"\n📊 RÉSULTATS DE L'ANALYSE")
        print("=" * 30)
        print(f"📄 Fichiers analysés: {total_fichiers}")
        print(f"🔍 Groupes de doublons: {len(doublons_groupes)}")
        
        total_doublons = sum(len(groupe) - 1 for groupe in doublons_groupes)
        print(f"📁 Fichiers doublons: {total_doublons}")
        print(f"💾 Espace récupérable: {self.formater_taille(espace_total_doublons)}")
        
        if doublons_groupes:
            print(f"\n🔍 DÉTAIL DES DOUBLONS (premiers 10 groupes):")
            print("-" * 50)
            
            for i, groupe in enumerate(doublons_groupes[:10]):
                taille = self.formater_taille(groupe[0].stat().st_size)
                print(f"\n📂 Groupe {i+1} - {len(groupe)} fichiers identiques ({taille}):")
                
                for j, fichier in enumerate(groupe):
                    statut = "🟢 GARDER" if j == 0 else "🔴 DOUBLON"
                    print(f"   {statut} {fichier}")
                    
            if len(doublons_groupes) > 10:
                print(f"\n... et {len(doublons_groupes) - 10} autres groupes")
                
        if self.simulation_mode:
            print(f"\n⚠️  MODE SIMULATION - Aucun fichier supprimé")
            print("💡 Pour supprimer réellement, utilisez --nettoyer")
        else:
            self.proposer_nettoyage(doublons_groupes)
            
    def calculer_hash(self, fichier):
        """Calcule le hash MD5 d'un fichier"""
        try:
            hash_md5 = hashlib.md5()
            with open(fichier, "rb") as f:
                # Lire par chunks pour les gros fichiers
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None
            
    def proposer_nettoyage(self, doublons_groupes):
        """Propose de nettoyer les doublons"""
        if not doublons_groupes:
            print("✅ Aucun doublon à nettoyer !")
            return
            
        print(f"\n🧹 NETTOYAGE DES DOUBLONS")
        print("=" * 30)
        
        reponse = input(f"Supprimer {sum(len(groupe) - 1 for groupe in doublons_groupes)} doublons ? (oui/non): ")
        
        if reponse.lower() in ['oui', 'o', 'yes', 'y']:
            fichiers_supprimes = 0
            espace_libere = 0
            
            for groupe in doublons_groupes:
                # Garder le premier, supprimer les autres
                for fichier in groupe[1:]:
                    try:
                        taille = fichier.stat().st_size
                        fichier.unlink()
                        fichiers_supprimes += 1
                        espace_libere += taille
                        print(f"🗑️  Supprimé: {fichier}")
                    except Exception as e:
                        print(f"❌ Erreur suppression {fichier}: {e}")
                        
            print(f"\n✅ Nettoyage terminé !")
            print(f"   📁 {fichiers_supprimes} fichiers supprimés")
            print(f"   💾 {self.formater_taille(espace_libere)} libérés")
        else:
            print("❌ Nettoyage annulé")
            
    def formater_taille(self, taille_bytes):
        """Formate une taille en bytes"""
        for unite in ['B', 'KB', 'MB', 'GB', 'TB']:
            if taille_bytes < 1024:
                return f"{taille_bytes:.1f} {unite}"
            taille_bytes /= 1024
        return f"{taille_bytes:.1f} PB"

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Dédoublonneur Simple')
    parser.add_argument('dossier', nargs='?', default=None, help='Dossier à analyser')
    parser.add_argument('--nettoyer', action='store_true', help='Mode nettoyage réel (supprime les doublons)')
    
    args = parser.parse_args()
    
    # Déterminer le dossier à analyser
    if args.dossier:
        dossier = args.dossier
    else:
        print("🚀 Dédoublonneur Simple")
        print("=" * 25)
        print("💡 Dossiers suggérés :")
        print("   • Downloads")
        print("   • Desktop") 
        print("   • Documents")
        print("   • Pictures")
        print()
        
        nom_dossier = input("📁 Nom du dossier à analyser: ").strip()
        
        if not nom_dossier:
            print("❌ Aucun dossier spécifié")
            return
            
        # Convertir les noms courts en chemins complets
        home = Path.home()
        dossiers_courants = {
            'downloads': home / 'Downloads',
            'desktop': home / 'Desktop', 
            'documents': home / 'Documents',
            'pictures': home / 'Pictures'
        }
        
        if nom_dossier.lower() in dossiers_courants:
            dossier = dossiers_courants[nom_dossier.lower()]
        else:
            dossier = Path(nom_dossier)
    
    # Créer le dédoublonneur
    dedoublonneur = DedoublonneurSimple()
    
    if args.nettoyer:
        dedoublonneur.simulation_mode = False
        print("⚠️  MODE NETTOYAGE RÉEL ACTIVÉ")
        print("⚠️  Assurez-vous d'avoir une sauvegarde !")
        print()
        
    # Analyser le dossier
    dedoublonneur.analyser_dossier(dossier)

if __name__ == "__main__":
    main()