#!/usr/bin/env python3
"""
Détection Rapide des Doublons - Version Optimisée
Usage : python3 dedoublons_rapide.py [dossier]
"""

import os
import sys
from pathlib import Path
from collections import defaultdict
import hashlib

def taille_readable(taille_bytes):
    """Formate une taille en bytes"""
    for unite in ['B', 'KB', 'MB', 'GB']:
        if taille_bytes < 1024:
            return f"{taille_bytes:.1f} {unite}"
        taille_bytes /= 1024
    return f"{taille_bytes:.1f} TB"

def hash_rapide(fichier):
    """Hash rapide basé sur la taille et le début du fichier"""
    try:
        stat = fichier.stat()
        taille = stat.st_size
        
        if taille == 0:
            return f"empty_{fichier.name}"
            
        # Pour les petits fichiers, hash complet
        if taille < 1024 * 1024:  # 1MB
            with open(fichier, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        
        # Pour les gros fichiers, hash des premiers et derniers Ko
        with open(fichier, 'rb') as f:
            debut = f.read(1024)
            f.seek(-1024, 2)  # Aller à la fin
            fin = f.read(1024)
            
        return hashlib.md5(f"{taille}_{debut}_{fin}".encode()).hexdigest()
        
    except Exception:
        return None

def analyser_doublons_rapide(dossier_path, max_fichiers=2000):
    """Analyse rapide des doublons"""
    print(f"🔍 ANALYSE RAPIDE DES DOUBLONS")
    print(f"📁 Dossier: {dossier_path}")
    print("=" * 50)
    
    path = Path(dossier_path)
    if not path.exists():
        print(f"❌ Dossier introuvable: {path}")
        return
    
    # Grouper d'abord par taille (rapide)
    fichiers_par_taille = defaultdict(list)
    total_fichiers = 0
    
    print("🕐 Analyse par taille...")
    
    try:
        for fichier in path.rglob("*"):
            if fichier.is_file() and not fichier.name.startswith('.'):
                try:
                    taille = fichier.stat().st_size
                    fichiers_par_taille[taille].append(fichier)
                    total_fichiers += 1
                    
                    if total_fichiers >= max_fichiers:
                        print(f"⚠️  Limite de {max_fichiers} fichiers atteinte")
                        break
                        
                except Exception:
                    continue
                    
    except KeyboardInterrupt:
        print("\n⏹️  Analyse interrompue")
        return
    
    # Identifier les doublons potentiels (même taille)
    candidats_doublons = []
    for taille, fichiers in fichiers_par_taille.items():
        if len(fichiers) > 1 and taille > 0:
            candidats_doublons.extend(fichiers)
    
    print(f"📄 {total_fichiers} fichiers analysés")
    print(f"🤔 {len(candidats_doublons)} candidats doublons (même taille)")
    
    if not candidats_doublons:
        print("✅ Aucun doublon potentiel détecté !")
        return
    
    # Hash des candidats pour confirmation
    print("🕐 Vérification des doublons réels...")
    
    fichiers_par_hash = defaultdict(list)
    
    for i, fichier in enumerate(candidats_doublons[:500]):  # Limiter pour la vitesse
        hash_val = hash_rapide(fichier)
        if hash_val:
            fichiers_par_hash[hash_val].append(fichier)
            
        if i % 50 == 0:
            print(f"   🔄 {i+1}/{min(len(candidats_doublons), 500)} vérifiés...")
    
    # Résultats finaux
    doublons_reels = []
    espace_recuperable = 0
    
    for hash_val, fichiers in fichiers_par_hash.items():
        if len(fichiers) > 1:
            doublons_reels.append(fichiers)
            taille_fichier = fichiers[0].stat().st_size
            espace_recuperable += taille_fichier * (len(fichiers) - 1)
    
    # Affichage des résultats
    print(f"\n📊 RÉSULTATS FINAUX")
    print("=" * 20)
    print(f"✅ Groupes de doublons trouvés: {len(doublons_reels)}")
    
    total_doublons = sum(len(groupe) - 1 for groupe in doublons_reels)
    print(f"📁 Fichiers doublons: {total_doublons}")
    print(f"💾 Espace récupérable: {taille_readable(espace_recuperable)}")
    
    if doublons_reels:
        print(f"\n🔍 EXEMPLES DE DOUBLONS:")
        print("-" * 30)
        
        for i, groupe in enumerate(doublons_reels[:5]):
            taille = taille_readable(groupe[0].stat().st_size)
            print(f"\n📂 Groupe {i+1}: {len(groupe)} fichiers ({taille})")
            
            for j, fichier in enumerate(groupe[:3]):
                statut = "🟢 ORIGINAL" if j == 0 else "🔴 DOUBLON"
                nom_court = fichier.name if len(fichier.name) < 40 else fichier.name[:37] + "..."
                print(f"   {statut} {nom_court}")
                
            if len(groupe) > 3:
                print(f"   ... et {len(groupe) - 3} autres")
                
        if len(doublons_reels) > 5:
            print(f"\n... et {len(doublons_reels) - 5} autres groupes")
    
    print(f"\n⚠️  MODE ANALYSE SEULEMENT")
    print("💡 Pour nettoyer, utiliser le mode complet avec confirmation")
    
    return len(doublons_reels), espace_recuperable

def main():
    if len(sys.argv) > 1:
        dossier = sys.argv[1]
    else:
        print("🚀 Détection Rapide des Doublons")
        print("=" * 35)
        print("💡 Dossiers suggérés :")
        print("   • Downloads")
        print("   • Desktop")
        print("   • Documents")
        print()
        
        nom = input("📁 Dossier à analyser: ").strip()
        
        if not nom:
            print("❌ Aucun dossier spécifié")
            return
        
        # Chemins courts
        home = Path.home()
        raccourcis = {
            'downloads': home / 'Downloads',
            'desktop': home / 'Desktop',
            'documents': home / 'Documents'
        }
        
        if nom.lower() in raccourcis:
            dossier = raccourcis[nom.lower()]
        else:
            dossier = nom
    
    analyser_doublons_rapide(dossier)

if __name__ == "__main__":
    main()