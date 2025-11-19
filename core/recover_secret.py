# -*- coding: utf-8 -*-
# ============================================================================
# RECOVER SECRET - Interface simple pour récupérer un secret
# ============================================================================
import sys
import json
import os

# Force UTF-8 encoding (safe pour EXE et console)
if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, RuntimeError):
        pass  # Cas EXE ou environnement spécial

# Ajoute le répertoire parent au path (pour imports du package core/)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from core.shamir_polynomial_robust import ShamirRobust

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

# Import pour conversion hex ↔ mots
try:
    from core.convert_hex_to_24words import hex_to_words_bip39, words_to_hex_bip39
    CONVERSION_AVAILABLE = True
except ImportError:
    try:
        # Fallback si import relatif échoue (par ex dans les tests)
        from convert_hex_to_24words import hex_to_words_bip39, words_to_hex_bip39
        CONVERSION_AVAILABLE = True
    except ImportError:
        CONVERSION_AVAILABLE = False

def input_part(part_num):
    """Demande une PART (hex ou 24 mots)"""
    print(f"\nPART {part_num}:")
    print("Choix d'entrée:")
    print("  1. Hex (64 caractères)")
    print("  2. 24 mots BIP39 (séparés par espaces)")

    choice = input("Choix (1 ou 2): ").strip()

    if choice == "2" and not CONVERSION_AVAILABLE:
        print("⚠️  Conversion mots→hex non disponible, utilise hex")
        choice = "1"

    if choice == "2":
        print(f"Colle les 24 mots de la part {part_num}:")
        words = []
        while len(words) < 24:
            line = input(f"Mots {len(words)+1}-{min(len(words)+6, 24)}: ").strip().lower()
            if line:
                words.extend(line.split())

        try:
            hex_part = words_to_hex_bip39(words[:24])
            print(f"  Converti en hex: {hex_part[:16]}...")
            return hex_part
        except Exception as e:
            print(f"❌ Erreur conversion: {e}")
            return None
    else:
        return input(f"Colle la part {part_num} (64 caractères hexa): ").strip()


# Entrée Part 1
print("\n" + "="*80)
print("PART 1")
print("="*80)

p1_num = int(input("Numéro de la part 1 (1, 2 ou 3): ").strip())
if p1_num not in [1, 2, 3]:
    print("❌ Numéro invalide")
    sys.exit(1)

p1_hex = input_part(p1_num)
if not p1_hex:
    print("❌ Erreur entrée Part 1")
    sys.exit(1)

valid1, msg1 = shamir.verify_part(p1_num, p1_hex)
print(f"  {msg1}")

if not valid1:
    print("❌ Part 1 invalide")
    sys.exit(1)

# Entrée Part 2
print("\n" + "="*80)
print("PART 2")
print("="*80)

p2_num = int(input("Numéro de la part 2 (1, 2 ou 3): ").strip())
if p2_num not in [1, 2, 3] or p2_num == p1_num:
    print("❌ Numéro invalide ou identique à Part 1")
    sys.exit(1)

p2_hex = input_part(p2_num)
if not p2_hex:
    print("❌ Erreur entrée Part 2")
    sys.exit(1)

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
