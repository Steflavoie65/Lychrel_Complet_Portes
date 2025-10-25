#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VÉRIFICATION EXHAUSTIVE DE LA FERMETURE POUR k=6
=================================================

Suite à l'ENTHOUSIASME de Claude.AI pour k=3,4,5 !

Claude prédit : ~2.4s pour 900,000 nombres (à 380k nombres/sec)

Objectif : Prouver exhaustivement que image(S₆) ⊆ S

Date: 10 octobre 2025, 20h50
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


def verifier_fermeture_k6_exhaustif():
    """
    Vérifie EXHAUSTIVEMENT la fermeture pour k=6.
    Teste TOUS les 900,000 nombres (100000-999999).
    
    Prédiction Claude : ~2.4s à 380k nombres/sec
    """
    print("="*70)
    print("VÉRIFICATION EXHAUSTIVE - FERMETURE k=6")
    print("="*70)
    print()
    
    # Charger S
    print("📂 Chargement ensemble S...")
    S_data = charger_ensemble_S()
    
    S_k6 = extraire_portes_par_k(S_data, k=6)
    S_toutes = extraire_toutes_portes_S(S_data)
    
    print(f"✅ Portes S₆ (k=6) : {len(S_k6)} portes")
    print(f"✅ Portes S (tous k) : {len(S_toutes)} portes")
    print()
    
    # Vérification exhaustive
    print("🔍 Vérification exhaustive [100000, 999999]...")
    print("⏳ ATTENTION : ~900,000 nombres")
    print("🎯 Prédiction Claude : ~2.4s à 380k nombres/sec")
    print()
    
    debut = time.time()
    
    nombres_testes = 0
    nombres_dans_S6 = 0
    fermeture_violee = []
    distributions_k_images = {}
    
    checkpoint_interval = 100000  # Affichage tous les 100k
    
    for n in range(100000, 1000000):
        nombres_testes += 1
        
        porte_n = calculer_porte(n)
        
        if porte_n in S_k6:
            nombres_dans_S6 += 1
            
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
        if (n - 100000 + 1) % checkpoint_interval == 0:
            pct = 100 * (n - 100000 + 1) / 900000
            temps_ecoule = time.time() - debut
            vitesse = (n - 100000 + 1) / temps_ecoule  # nombres/sec
            temps_restant = (900000 - (n - 100000 + 1)) / vitesse
            
            print(f"  Progression: {n - 100000 + 1}/900000 ({pct:.1f}%) - "
                  f"Vitesse: {vitesse:.0f} nb/s - "
                  f"Temps restant: ~{temps_restant:.0f}s")
    
    duree = time.time() - debut
    vitesse_moyenne = nombres_testes / duree
    
    # Résultats
    print()
    print("="*70)
    print("📊 RÉSULTATS")
    print("="*70)
    print()
    
    print(f"🔢 Nombres testés : {nombres_testes:,}")
    print(f"📌 Nombres avec porte ∈ S₆ : {nombres_dans_S6}")
    print(f"⏱️  Durée : {duree:.2f}s")
    print(f"🚀 Vitesse moyenne : {vitesse_moyenne:,.0f} nombres/sec")
    print()
    
    # Comparaison avec prédiction Claude
    prediction_claude = 2.4
    if duree < prediction_claude:
        ratio = prediction_claude / duree
        print(f"🎯 Prédiction Claude : {prediction_claude}s")
        print(f"✅ Réalité : {duree:.2f}s ({ratio:.1f}x PLUS RAPIDE !) ⚡")
    else:
        print(f"🎯 Prédiction Claude : {prediction_claude}s")
        print(f"📊 Réalité : {duree:.2f}s")
    print()
    
    if len(fermeture_violee) == 0:
        print("✅ FERMETURE VÉRIFIÉE : Tous les T(n) restent dans S")
        print()
        print("🎯 CONCLUSION : image(S₆) ⊆ S (PROUVÉ EXHAUSTIVEMENT)")
        fermeture_ok = True
    else:
        print(f"❌ FERMETURE VIOLÉE : {len(fermeture_violee)} cas trouvés")
        fermeture_ok = False
    
    print()
    print("📈 Distribution dimensions des images:")
    for k_img in sorted(distributions_k_images.keys()):
        count = distributions_k_images[k_img]
        pct = 100 * count / nombres_dans_S6 if nombres_dans_S6 > 0 else 0
        print(f"  k={k_img} : {count} images ({pct:.1f}%)")
    
    # Analyse stabilité (comme pour k=5)
    if 6 in distributions_k_images and nombres_dans_S6 > 0:
        stable_pct = 100 * distributions_k_images[6] / nombres_dans_S6
        monte_pct = 100 - stable_pct
        print()
        print("🎯 Analyse stabilité (comme k=5) :")
        print(f"   k=6 stable : {stable_pct:.1f}%")
        print(f"   k=6→k=7 monte : {monte_pct:.1f}%")
        if stable_pct > 85:
            print("   ⭐ HAUTE STABILITÉ (comme k=5) !")
    
    print()
    
    # Sauvegarder résultats
    resultats = {
        'dimension_testee': 6,
        'methode': 'exhaustive',
        'intervalle': [100000, 999999],
        'nombres_testes': nombres_testes,
        'nombres_dans_S6': nombres_dans_S6,
        'fermeture_verifiee': fermeture_ok,
        'violations': len(fermeture_violee),
        'exemples_violations': fermeture_violee[:10] if fermeture_violee else [],
        'distribution_k_images': distributions_k_images,
        'duree_secondes': duree,
        'vitesse_moyenne_nb_sec': vitesse_moyenne,
        'prediction_claude_sec': prediction_claude,
        'timestamp': datetime.now().isoformat(),
        'portes_S6': list(S_k6),
        'nombre_portes_S6': len(S_k6),
        'nombre_portes_S_total': len(S_toutes)
    }
    
    fichier_sortie = f"verification_exhaustive_k6_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        json.dump(resultats, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Résultats sauvegardés : {fichier_sortie}")
    print()
    
    return resultats


if __name__ == "__main__":
    print("🎯 Suite à l'enthousiasme de Claude pour k=3,4,5 !")
    print()
    print("Claude dit : 'LANCER k=6 MAINTENANT (très important !)'")
    print()
    
    resultats = verifier_fermeture_k6_exhaustif()
    
    print("="*70)
    print("✅ VÉRIFICATION k=6 TERMINÉE")
    print("="*70)
    
    if resultats['fermeture_verifiee']:
        print()
        print("🎉 SUCCÈS : Fermeture prouvée exhaustivement pour k=6 !")
        print()
        print("🎓 k=3, k=4, k=5, k=6 : Tous vérifiés exhaustivement ✅")
        print()
        print("📊 Couverture : TOUS les nombres jusqu'à 999,999 ! 🎯")
        print()
        print("➡️  Prochaine étape : k=7 (9M nombres, ~30-60s)")
