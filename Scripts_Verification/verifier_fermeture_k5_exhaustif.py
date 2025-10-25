#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VÉRIFICATION EXHAUSTIVE DE LA FERMETURE POUR k=5
=================================================

Suite aux suggestions de Claude.AI :
- Vérifier TOUS les nombres 10000-99999 (pas échantillonnage)
- Prouver rigoureusement que image(S₅) ⊆ S

⚠️ ATTENTION : ~90000 nombres à tester
   Temps estimé : 1-2 heures

Date: 10 octobre 2025, 19:45
"""

import json
import time
from datetime import datetime


def reverse_number(n: int) -> int:
    """Inverse un nombre."""
    return int(str(n)[::-1])


def reverse_and_add(n: int) -> int:
    """Opération T: n + reverse(n)."""
    return n + reverse_number(n)


def calculer_porte(n: int) -> tuple:
    """Calcule la porte π_k(n)."""
    digits = [int(d) for d in str(n)]
    k = len(digits)
    reverse_digits = digits[::-1]
    
    sommes = []
    for i in range(k):
        s = digits[i] + reverse_digits[i]
        sommes.append(s)
    
    return tuple(sommes)


def charger_ensemble_S(fichier_json: str = "Scripts/ensemble_S_ferme.json") -> dict:
    """Charge l'ensemble S depuis JSON."""
    with open(fichier_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def extraire_portes_par_k(S_data: dict, k: int) -> set:
    """Extrait toutes les portes de dimension k. Reconstruit portes symétriques."""
    portes = set()
    
    k_str = str(k)
    if k_str in S_data['ensemble_S']['portes_par_longueur']:
        for porte_half in S_data['ensemble_S']['portes_par_longueur'][k_str]:
            if k % 2 == 1:
                milieu = porte_half[-1]
                debut = porte_half[:-1]
                porte_complete = debut + [milieu] + list(reversed(debut))
            else:
                porte_complete = porte_half + list(reversed(porte_half))
            
            porte_tuple = tuple(porte_complete)
            portes.add(porte_tuple)
    
    return portes


def extraire_toutes_portes_S(S_data: dict) -> set:
    """Extrait TOUTES les portes de S (tous k). Reconstruit portes symétriques."""
    toutes_portes = set()
    
    for k_str, portes_list in S_data['ensemble_S']['portes_par_longueur'].items():
        k = int(k_str)
        for porte_half in portes_list:
            if k % 2 == 1:
                milieu = porte_half[-1]
                debut = porte_half[:-1]
                porte_complete = debut + [milieu] + list(reversed(debut))
            else:
                porte_complete = porte_half + list(reversed(porte_half))
            
            porte_tuple = tuple(porte_complete)
            toutes_portes.add(porte_tuple)
    
    return toutes_portes


def verifier_fermeture_k5_exhaustif():
    """
    Vérifie EXHAUSTIVEMENT la fermeture pour k=5.
    Teste TOUS les nombres 10000-99999.
    
    ⚠️ Long calcul : ~1-2 heures
    """
    print("="*70)
    print("VÉRIFICATION EXHAUSTIVE - FERMETURE k=5")
    print("="*70)
    print()
    
    # Charger S
    print("📂 Chargement ensemble S...")
    S_data = charger_ensemble_S()
    
    S_k5 = extraire_portes_par_k(S_data, k=5)
    S_toutes = extraire_toutes_portes_S(S_data)
    
    print(f"✅ Portes S₅ (k=5) : {len(S_k5)} portes")
    print(f"✅ Portes S (tous k) : {len(S_toutes)} portes")
    print()
    
    # Vérification exhaustive
    print("🔍 Vérification exhaustive [10000, 99999]...")
    print("⏳ ATTENTION : ~90000 nombres, calcul peut prendre 1-2 heures...")
    print()
    
    debut = time.time()
    
    nombres_testes = 0
    nombres_dans_S5 = 0
    fermeture_violee = []
    distributions_k_images = {}
    
    checkpoint_interval = 10000  # Sauvegarde intermédiaire tous les 10k
    
    for n in range(10000, 100000):
        nombres_testes += 1
        
        porte_n = calculer_porte(n)
        
        if porte_n in S_k5:
            nombres_dans_S5 += 1
            
            T_n = reverse_and_add(n)
            porte_T_n = calculer_porte(T_n)
            
            if porte_T_n not in S_toutes:
                fermeture_violee.append({
                    'n': n,
                    'porte_n': porte_n,
                    'T_n': T_n,
                    'porte_T_n': porte_T_n
                })
            
            k_image = len(porte_T_n)
            distributions_k_images[k_image] = distributions_k_images.get(k_image, 0) + 1
        
        # Affichage progression
        if (n - 10000 + 1) % checkpoint_interval == 0:
            pct = 100 * (n - 10000 + 1) / 90000
            temps_ecoule = time.time() - debut
            vitesse = (n - 10000 + 1) / temps_ecoule  # nombres/sec
            temps_restant = (90000 - (n - 10000 + 1)) / vitesse
            
            print(f"  Progression: {n - 10000 + 1}/90000 ({pct:.1f}%) - "
                  f"Vitesse: {vitesse:.0f} nb/s - "
                  f"Temps restant: ~{temps_restant/60:.0f} min")
    
    duree = time.time() - debut
    
    # Résultats
    print()
    print("="*70)
    print("📊 RÉSULTATS")
    print("="*70)
    print()
    
    print(f"🔢 Nombres testés : {nombres_testes}")
    print(f"📌 Nombres avec porte ∈ S₅ : {nombres_dans_S5}")
    print(f"⏱️  Durée : {duree:.2f}s ({duree/60:.1f} min = {duree/3600:.2f}h)")
    print()
    
    if len(fermeture_violee) == 0:
        print("✅ FERMETURE VÉRIFIÉE : Tous les T(n) restent dans S")
        print()
        print("🎯 CONCLUSION : image(S₅) ⊆ S (PROUVÉ EXHAUSTIVEMENT)")
        fermeture_ok = True
    else:
        print(f"❌ FERMETURE VIOLÉE : {len(fermeture_violee)} cas trouvés")
        fermeture_ok = False
    
    print()
    print("📈 Distribution dimensions des images:")
    for k_img in sorted(distributions_k_images.keys()):
        count = distributions_k_images[k_img]
        pct = 100 * count / nombres_dans_S5 if nombres_dans_S5 > 0 else 0
        print(f"  k={k_img} : {count} images ({pct:.1f}%)")
    
    print()
    
    # Sauvegarder résultats
    resultats = {
        'dimension_testee': 5,
        'methode': 'exhaustive',
        'intervalle': [10000, 99999],
        'nombres_testes': nombres_testes,
        'nombres_dans_S5': nombres_dans_S5,
        'fermeture_verifiee': fermeture_ok,
        'violations': len(fermeture_violee),
        'exemples_violations': fermeture_violee[:10] if fermeture_violee else [],
        'distribution_k_images': distributions_k_images,
        'duree_secondes': duree,
        'timestamp': datetime.now().isoformat(),
        'portes_S5': list(S_k5),
        'nombre_portes_S5': len(S_k5),
        'nombre_portes_S_total': len(S_toutes)
    }
    
    fichier_sortie = f"verification_exhaustive_k5_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        json.dump(resultats, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Résultats sauvegardés : {fichier_sortie}")
    print()
    
    return resultats


if __name__ == "__main__":
    print("⚠️  AVERTISSEMENT : Calcul long (~1-2 heures)")
    print()
    
    reponse = input("Voulez-vous continuer ? (oui/non) : ").strip().lower()
    
    if reponse in ['oui', 'o', 'y', 'yes']:
        resultats = verifier_fermeture_k5_exhaustif()
        
        print("="*70)
        print("✅ VÉRIFICATION k=5 TERMINÉE")
        print("="*70)
        
        if resultats['fermeture_verifiee']:
            print()
            print("🎉 SUCCÈS : Fermeture prouvée exhaustivement pour k=5 !")
            print()
            print("🎓 k=3, k=4, k=5 : Tous vérifiés exhaustivement ✅")
    else:
        print()
        print("❌ Annulé par l'utilisateur")
