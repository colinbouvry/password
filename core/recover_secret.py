# -*- coding: utf-8 -*-
# ============================================================================
# RECOVER SECRET - Interface simple pour récupérer un secret
# ============================================================================
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import os
from shamir_polynomial_robust import ShamirRobust

print("\n" + "="*80)
print("RÉCUPÉRER UN SECRET - SHAMIR ROBUST")
print("="*80)

print("\nVous pouvez utiliser n'importe quelles 2 parts sur 3.")
print("Les 3 parts vous permettront aussi de récupérer le secret.")

shamir = ShamirRobust()

# Essaie de charger les métadonnées si disponibles
metadata_file = "shamir_metadata.json"
if os.path.exists(metadata_file):
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        shamir.metadata = metadata
        if metadata.get('passphrase'):
            shamir.passphrase_original = metadata['passphrase']
        print(f"\n✅ Métadonnées chargées depuis {metadata_file}")
    except Exception as e:
        print(f"\n⚠️  Impossible de charger les métadonnées: {e}")
else:
    print(f"\nℹ️  Fichier {metadata_file} non trouvé")
    print(f"   Les métadonnées ne seront pas disponibles pour validation")

# Entrée Part 1
print("\n" + "="*80)
print("PART 1")
print("="*80)

p1_num = int(input("Numéro de la part 1 (1, 2 ou 3) : ").strip())
if p1_num not in [1, 2, 3]:
    print("❌ Numéro invalide")
    sys.exit(1)

p1_hex = input(f"Colle la part {p1_num} (64 caractères hexa) : ").strip()

valid1, msg1 = shamir.verify_part(p1_num, p1_hex)
print(f"  {msg1}")

if not valid1:
    print("❌ Part 1 invalide")
    sys.exit(1)

# Entrée Part 2
print("\n" + "="*80)
print("PART 2")
print("="*80)

p2_num = int(input("Numéro de la part 2 (1, 2 ou 3) : ").strip())
if p2_num not in [1, 2, 3] or p2_num == p1_num:
    print("❌ Numéro invalide ou identique à Part 1")
    sys.exit(1)

p2_hex = input(f"Colle la part {p2_num} (64 caractères hexa) : ").strip()

valid2, msg2 = shamir.verify_part(p2_num, p2_hex)
print(f"  {msg2}")

if not valid2:
    print("❌ Part 2 invalide")
    sys.exit(1)

# Récupère la PASSPHRASE
print("\n" + "="*80)
print("RÉCUPÉRATION")
print("="*80)

passphrase = shamir.recover_secret(p1_num, p1_hex, p2_num, p2_hex)

if passphrase:
    print("\n" + "="*80)
    print("✅ SUCCÈS !")
    print("="*80)
    print(f"\n📋 PASSPHRASE RETROUVÉE (les 24 mots) :")
    print(f"  {passphrase}")

    # Affiche aussi les mots individuels
    words = passphrase.split()
    print(f"\n📝 Les mots individuels :")
    for i, word in enumerate(words, 1):
        print(f"   {i:02d}. {word}")

    print(f"\n✅ Vous pouvez utiliser ces mots comme Master Password Bitwarden!")
else:
    print("\n❌ Impossible de récupérer la passphrase")
    print("Vérifiez vos parts et réessayez.")

print("\n" + "="*80 + "\n")
