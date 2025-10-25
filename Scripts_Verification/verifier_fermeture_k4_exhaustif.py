#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VÉRIFICATION EXHAUSTIVE DE LA FERMETURE POUR k=4
=================================================

Suite aux suggestions de Claude.AI :
- Vérifier TOUS les nombres 1000-9999 (pas échantillonnage)
- Prouver rigoureusement que image(S₄) ⊆ S

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


def verifier_fermeture_k4_exhaustif():
    """
    Vérifie EXHAUSTIVEMENT la fermeture pour k=4.
    Teste TOUS les nombres 1000-9999.
    """
    print("="*70)
    print("VÉRIFICATION EXHAUSTIVE - FERMETURE k=4")
    print("="*70)
    print()
    
    # Charger S
    print("📂 Chargement ensemble S...")
    S_data = charger_ensemble_S()
    
    S_k4 = extraire_portes_par_k(S_data, k=4)
    S_toutes = extraire_toutes_portes_S(S_data)
    
    print(f"✅ Portes S₄ (k=4) : {len(S_k4)} portes")
    print(f"✅ Portes S (tous k) : {len(S_toutes)} portes")
    print()
    
    # Vérification exhaustive
    print("🔍 Vérification exhaustive [1000, 9999]...")
    print("⏳ Attention : ~9000 nombres, peut prendre quelques minutes...")
    print()
    
    debut = time.time()
    
    nombres_testes = 0
    nombres_dans_S4 = 0
    fermeture_violee = []
    distributions_k_images = {}
    
    for n in range(1000, 10000):
        nombres_testes += 1
        
        porte_n = calculer_porte(n)
        
        if porte_n in S_k4:
            nombres_dans_S4 += 1
            
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
        if (n - 1000 + 1) % 1000 == 0:
            pct = 100 * (n - 1000 + 1) / 9000
            print(f"  Progression: {n - 1000 + 1}/9000 ({pct:.1f}%)...")
    
    duree = time.time() - debut
    
    # Résultats
    print()
    print("="*70)
    print("📊 RÉSULTATS")
    print("="*70)
    print()
    
    print(f"🔢 Nombres testés : {nombres_testes}")
    print(f"📌 Nombres avec porte ∈ S₄ : {nombres_dans_S4}")
    print(f"⏱️  Durée : {duree:.2f}s ({duree/60:.1f} min)")
    print()
    
    if len(fermeture_violee) == 0:
        print("✅ FERMETURE VÉRIFIÉE : Tous les T(n) restent dans S")
        print()
        print("🎯 CONCLUSION : image(S₄) ⊆ S (PROUVÉ EXHAUSTIVEMENT)")
        fermeture_ok = True
    else:
        print(f"❌ FERMETURE VIOLÉE : {len(fermeture_violee)} cas trouvés")
        fermeture_ok = False
    
    print()
    print("📈 Distribution dimensions des images:")
    for k_img in sorted(distributions_k_images.keys()):
        count = distributions_k_images[k_img]
        pct = 100 * count / nombres_dans_S4 if nombres_dans_S4 > 0 else 0
        print(f"  k={k_img} : {count} images ({pct:.1f}%)")
    
    print()
    
    # Sauvegarder résultats
    resultats = {
        'dimension_testee': 4,
        'methode': 'exhaustive',
        'intervalle': [1000, 9999],
        'nombres_testes': nombres_testes,
        'nombres_dans_S4': nombres_dans_S4,
        'fermeture_verifiee': fermeture_ok,
        'violations': len(fermeture_violee),
        'exemples_violations': fermeture_violee[:10] if fermeture_violee else [],
        'distribution_k_images': distributions_k_images,
        'duree_secondes': duree,
        'timestamp': datetime.now().isoformat(),
        'portes_S4': list(S_k4),
        'nombre_portes_S4': len(S_k4),
        'nombre_portes_S_total': len(S_toutes)
    }
    
    fichier_sortie = f"verification_exhaustive_k4_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        json.dump(resultats, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Résultats sauvegardés : {fichier_sortie}")
    print()
    
    return resultats


if __name__ == "__main__":
    resultats = verifier_fermeture_k4_exhaustif()
    
    print("="*70)
    print("✅ VÉRIFICATION k=4 TERMINÉE")
    print("="*70)
    
    if resultats['fermeture_verifiee']:
        print()
        print("🎉 SUCCÈS : Fermeture prouvée exhaustivement pour k=4 !")
        print()
        print("➡️  Prochaine étape : k=5")
