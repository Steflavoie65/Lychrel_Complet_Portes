#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VÉRIFICATION EXHAUSTIVE DE LA FERMETURE POUR k=3
=================================================

Suite aux suggestions de Claude.AI :
- Vérifier TOUS les nombres 100-999 (pas échantillonnage)
- Prouver rigoureusement que image(S₃) ⊆ S

Méthode:
1. Charger S depuis ensemble_S_ferme.json
2. Pour CHAQUE nombre n ∈ [100, 999]:
   - Calculer porte_n = π₃(n)
   - Si porte_n ∈ S₃:
     * Calculer T(n)
     * Calculer porte_T(n)
     * Vérifier porte_T(n) ∈ S
3. Documenter résultats

Date: 10 octobre 2025, 19:40
Auteur: Assistant (suggestion Claude)
"""

import json
import time
from datetime import datetime
from pathlib import Path


def reverse_number(n: int) -> int:
    """Inverse un nombre."""
    return int(str(n)[::-1])


def reverse_and_add(n: int) -> int:
    """Opération T: n + reverse(n)."""
    return n + reverse_number(n)


def calculer_porte_k3(n: int) -> tuple:
    """
    Calcule la porte π₃(n) pour un nombre à k chiffres.
    
    Porte = (s₁, s₂, s₃, s₄) où:
    - s₁ = somme des chiffres en position 1
    - s₂ = somme en position 2
    - etc.
    """
    digits = [int(d) for d in str(n)]
    k = len(digits)
    
    reverse_digits = digits[::-1]
    
    # Calculer sommes par position
    sommes = []
    for i in range(k):
        s = digits[i] + reverse_digits[i]
        sommes.append(s)
    
    return tuple(sommes)


def calculer_porte_apres_T(n: int) -> tuple:
    """
    Calcule la porte de T(n).
    
    Note: T(n) peut avoir k ou k+1 chiffres.
    """
    T_n = reverse_and_add(n)
    return calculer_porte_k3(T_n)


def charger_ensemble_S(fichier_json: str = "Scripts/ensemble_S_ferme.json") -> dict:
    """Charge l'ensemble S depuis JSON."""
    with open(fichier_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def extraire_portes_par_k(S_data: dict, k: int) -> set:
    """
    Extrait toutes les portes de dimension k.
    
    Note: Le JSON stocke seulement la moitié de la porte (symétrique).
    On reconstruit la porte complète.
    
    Returns: set de tuples
    """
    portes = set()
    
    # Structure: ensemble_S -> portes_par_longueur -> k -> liste de portes
    k_str = str(k)
    if k_str in S_data['ensemble_S']['portes_par_longueur']:
        for porte_half in S_data['ensemble_S']['portes_par_longueur'][k_str]:
            # Reconstruire porte complète (symétrique)
            # Si k impair: (a, b, c) → (a, b, c, b, a) mais stocké (a, b)
            # Si k pair: (a, b, c, d) → (a, b, c, d, c, b, a) mais stocké (a, b, c)
            
            if k % 2 == 1:
                # k impair: porte_half + [middle] + reverse(porte_half)
                # Mais middle n'est pas dans porte_half
                # En fait pour k=3: stocké (7, 18) mais complet est (7, 18, 7)
                # Donc: porte_half[:-1] + reverse(porte_half)
                milieu = porte_half[-1]
                debut = porte_half[:-1]
                porte_complete = debut + [milieu] + list(reversed(debut))
            else:
                # k pair: porte_half + reverse(porte_half)
                porte_complete = porte_half + list(reversed(porte_half))
            
            porte_tuple = tuple(porte_complete)
            portes.add(porte_tuple)
    
    return portes


def extraire_toutes_portes_S(S_data: dict) -> set:
    """
    Extrait TOUTES les portes de S (tous k).
    Reconstruit les portes complètes depuis leur format symétrique.
    """
    toutes_portes = set()
    
    for k_str, portes_list in S_data['ensemble_S']['portes_par_longueur'].items():
        k = int(k_str)
        for porte_half in portes_list:
            # Reconstruire porte complète
            if k % 2 == 1:
                # k impair
                milieu = porte_half[-1]
                debut = porte_half[:-1]
                porte_complete = debut + [milieu] + list(reversed(debut))
            else:
                # k pair
                porte_complete = porte_half + list(reversed(porte_half))
            
            porte_tuple = tuple(porte_complete)
            toutes_portes.add(porte_tuple)
    
    return toutes_portes


def verifier_fermeture_k3_exhaustif():
    """
    Vérifie EXHAUSTIVEMENT la fermeture pour k=3.
    
    Teste TOUS les nombres 100-999.
    """
    print("="*70)
    print("VÉRIFICATION EXHAUSTIVE - FERMETURE k=3")
    print("="*70)
    print()
    
    # Charger S
    print("📂 Chargement ensemble S...")
    S_data = charger_ensemble_S()
    
    S_k3 = extraire_portes_par_k(S_data, k=3)
    S_toutes = extraire_toutes_portes_S(S_data)
    
    print(f"✅ Portes S₃ (k=3) : {len(S_k3)} portes")
    print(f"✅ Portes S (tous k) : {len(S_toutes)} portes")
    print()
    
    # Vérification exhaustive
    print("🔍 Vérification exhaustive [100, 999]...")
    print()
    
    debut = time.time()
    
    nombres_testes = 0
    nombres_dans_S3 = 0
    fermeture_violee = []
    distributions_k_images = {}
    
    for n in range(100, 1000):
        nombres_testes += 1
        
        # Calculer porte de n
        porte_n = calculer_porte_k3(n)
        
        # Si n a une porte dans S₃
        if porte_n in S_k3:
            nombres_dans_S3 += 1
            
            # Calculer T(n) et sa porte
            T_n = reverse_and_add(n)
            porte_T_n = calculer_porte_k3(T_n)
            
            # Vérifier si porte_T_n ∈ S
            if porte_T_n not in S_toutes:
                fermeture_violee.append({
                    'n': n,
                    'porte_n': porte_n,
                    'T_n': T_n,
                    'porte_T_n': porte_T_n
                })
            
            # Statistiques: dimension de l'image
            k_image = len(porte_T_n)
            distributions_k_images[k_image] = distributions_k_images.get(k_image, 0) + 1
        
        # Affichage progression
        if (n - 100 + 1) % 100 == 0:
            print(f"  Progression: {n - 100 + 1}/900 nombres testés...")
    
    duree = time.time() - debut
    
    # Résultats
    print()
    print("="*70)
    print("📊 RÉSULTATS")
    print("="*70)
    print()
    
    print(f"🔢 Nombres testés : {nombres_testes}")
    print(f"📌 Nombres avec porte ∈ S₃ : {nombres_dans_S3}")
    print(f"⏱️  Durée : {duree:.2f}s")
    print()
    
    if len(fermeture_violee) == 0:
        print("✅ FERMETURE VÉRIFIÉE : Tous les T(n) restent dans S")
        print()
        print("🎯 CONCLUSION : image(S₃) ⊆ S (PROUVÉ EXHAUSTIVEMENT)")
        fermeture_ok = True
    else:
        print(f"❌ FERMETURE VIOLÉE : {len(fermeture_violee)} cas trouvés")
        print()
        print("Exemples de violations:")
        for violation in fermeture_violee[:5]:
            print(f"  n={violation['n']}, porte={violation['porte_n']}")
            print(f"    → T(n)={violation['T_n']}, porte_T(n)={violation['porte_T_n']} ∉ S")
        fermeture_ok = False
    
    print()
    print("📈 Distribution dimensions des images:")
    for k_img in sorted(distributions_k_images.keys()):
        count = distributions_k_images[k_img]
        pct = 100 * count / nombres_dans_S3
        print(f"  k={k_img} : {count} images ({pct:.1f}%)")
    
    print()
    
    # Sauvegarder résultats
    resultats = {
        'dimension_testee': 3,
        'methode': 'exhaustive',
        'intervalle': [100, 999],
        'nombres_testes': nombres_testes,
        'nombres_dans_S3': nombres_dans_S3,
        'fermeture_verifiee': fermeture_ok,
        'violations': len(fermeture_violee),
        'exemples_violations': fermeture_violee[:10] if fermeture_violee else [],
        'distribution_k_images': distributions_k_images,
        'duree_secondes': duree,
        'timestamp': datetime.now().isoformat(),
        'portes_S3': list(S_k3),
        'nombre_portes_S3': len(S_k3),
        'nombre_portes_S_total': len(S_toutes)
    }
    
    fichier_sortie = f"verification_exhaustive_k3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        json.dump(resultats, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Résultats sauvegardés : {fichier_sortie}")
    print()
    
    return resultats


if __name__ == "__main__":
    resultats = verifier_fermeture_k3_exhaustif()
    
    print("="*70)
    print("✅ VÉRIFICATION k=3 TERMINÉE")
    print("="*70)
    
    if resultats['fermeture_verifiee']:
        print()
        print("🎉 SUCCÈS : Fermeture prouvée exhaustivement pour k=3 !")
        print()
        print("➡️  Prochaine étape : k=4")
