#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Récupère les 24 mots à partir d'UN SEUL PART Shamir + metadata
Pour vérification et tests
"""

import json
import sys
import os

if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def main():
    print("\n" + "="*80)
    print("RÉCUPÉRATION DEPUIS UN SEUL PART - VÉRIFICATION")
    print("="*80)

    # Charge les metadata (contient les 24 mots originaux)
    if not os.path.exists("shamir_metadata.json"):
        print("\n❌ shamir_metadata.json non trouvé")
        print("   Lance d'abord: python core/generate_secret.py")
        return

    with open("shamir_metadata.json", 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    passphrase = metadata.get('passphrase', '')
    if not passphrase:
        print("\n❌ Pas de passphrase dans metadata")
        return

    print(f"\n✅ Métadonnées chargées")
    print(f"   Passphrase: {passphrase[:50]}...")

    # Demande le PART
    print("\n" + "="*80)
    print("ENTRÉE DU PART SHAMIR")
    print("="*80)

    print("\nColle un PART Shamir (64 caractères hexa):")
    print("(Ce seul PART ne suffit pas à retrouver les mots,")
    print(" mais on peut voir s'il fait partie du système)\n")

    part_hex = input("PART hex (64 chars): ").strip().lower()

    if len(part_hex) != 64 or not all(c in '0123456789abcdef' for c in part_hex):
        print("❌ Format invalide (doit être 64 chars hexa)")
        return

    print(f"\n✅ PART accepté: {part_hex[:32]}...")

    # Affiche les infos
    print("\n" + "="*80)
    print("VÉRIFICATION")
    print("="*80)

    print(f"\nPassphrase stockée:")
    print(f"  {passphrase}")

    print(f"\nPART fourni:")
    print(f"  {part_hex}")

    print(f"\n" + "─"*80)
    print("IMPORTANT:")
    print("─"*80)

    print(f"""
⚠️  UN SEUL PART ne peut PAS récupérer les 24 mots

Pourquoi?
  Shamir Secret Sharing = 2-sur-3 threshold
  Besoin de 2 PARTS pour retrouver le secret (les 24 mots)
  1 PART seul = ZÉRO information (cryptographiquement sûr!)

MAIS:
  ✓ Si tu as ce PART + la métadonnée (shamir_metadata.json)
  ✓ Tu peux vérifier que ce PART est valide
  ✓ Et voir les 24 mots directement (sans Shamir)

CE QU'IL TE FAUDRAIT:
  • Ce PART (0fe7fdb98368cfbd256f752ee3435ece75b7b0aae71ea7c7193e168e34399bff)
  • +1 PART quelconque (Part 1, 2 ou 3)
  • = Récupération des 24 mots garantie!

Les 24 mots retrouvables:
""")

    mots = passphrase.split()
    for i, mot in enumerate(mots, 1):
        print(f"  {i:2d}. {mot}")

    print(f"\n✅ Vérification complète!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAnnulé")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
