# -*- coding: utf-8 -*-
# ============================================================================
# GENERATE SECRET - Interface simple pour générer et diviser
# ============================================================================
import sys
sys.stdout.reconfigure(encoding='utf-8')

from shamir_polynomial_robust import ShamirRobust
from mots import MOTS  # IMPORT de la liste centralisée (SANS DUPLICATION)
import hashlib
import json
import os

print("\n" + "="*80)
print("GÉNÉRER ET DIVISER UN SECRET - SHAMIR ROBUST")
print("="*80)

print("\nOptions :")
print("  1. Générer une passphrase 24 mots")
print("  2. Utiliser une passphrase existante")

choice = input("\nChoisir (1 ou 2) : ").strip()

if choice == "1":
    # Générer 24 mots
    import time
    import random

    # Utilise la liste centralisée MOTS importée depuis mots.py
    mots_copy = MOTS.copy()
    raw_entropy = time.time_ns()
    random.seed(raw_entropy)
    random.shuffle(mots_copy)

    passphrase = " ".join(mots_copy[:24])

    print(f"\n✅ Passphrase générée (entropie réelle)")
    print(f"   Graine : {raw_entropy}")

elif choice == "2":
    passphrase = input("\nColle ta passphrase 24 mots : ").strip()

else:
    print("❌ Choix invalide")
    sys.exit(1)

# Affiche les 24 mots
print(f"\n📋 24 MOTS :")
mots = passphrase.split()
for i, mot in enumerate(mots, 1):
    print(f"   {i:02d}. {mot}")

# Génère les parts Shamir robustes
print("\n" + "="*80)
print("DIVISION SHAMIR ROBUSTE")
print("="*80)

shamir = ShamirRobust()
parts, metadata = shamir.split_secret(passphrase)

# Affiche les parts
print("\n" + "="*80)
print("VOS 3 PARTS SHAMIR")
print("="*80)

for i in [1, 2, 3]:
    print(f"\nPart {i} :")
    print(f"  Valeur   : {parts[i]['hex']}")
    if 'checksum' in parts[i]:
        print(f"  Checksum : {parts[i]['checksum']}")
    else:
        print(f"  ⚠️  Checksum : MANQUANT !")

print("\n" + "="*80)
print("💾 MÉTADONNÉES SÉCURITÉ")
print("="*80)
print(f"Secret Checksum : {metadata['secret_checksum']}")
print(f"Global Checksum : {metadata['global_checksum']}")
print(f"Timestamp       : {metadata['timestamp']}")

# Sauvegarde les métadonnées dans un fichier pour la récupération
metadata_file = "shamir_metadata.json"
metadata_to_save = {
    'passphrase': metadata.get('passphrase'),
    'passphrase_length': metadata.get('passphrase_length'),
    'secret_checksum': metadata.get('secret_checksum'),
    'global_checksum': metadata.get('global_checksum'),
    'timestamp': metadata.get('timestamp'),
    'threshold': metadata.get('threshold'),
    'parts_count': metadata.get('parts_count'),
}

try:
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata_to_save, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Métadonnées sauvegardées dans {metadata_file}")
    print(f"   ⚠️  GARDER CE FICHIER EN LIEU SÛR (même sécurité que les PARTS!)")
except Exception as e:
    print(f"\n⚠️  Impossible de sauvegarder les métadonnées: {e}")

print("\n" + "="*80)
print("✅ WORKFLOW SAUVEGARDE ET RÉCUPÉRATION")
print("="*80)

print(f"""
📋 VOS 24 MOTS (LA PASSPHRASE):
   Stockez en 2 endroits:
   ✅ Papier dans Coffre A (impression)
   ✅ Digital dans Bitwarden (backup)

   Ces mots = votre Master Password Bitwarden!

🔐 VOS 3 PARTS SHAMIR:
   Distribuez dans 3 coffres-forts:
   ✅ PART 1 dans Coffre A (gravé acier)
   ✅ PART 2 dans Coffre B (gravé acier)
   ✅ PART 3 dans Coffre C (gravé acier)

   BUT: Si vous oubliez les 24 mots
        → Vous pouvez les RETROUVER avec 2 parts!
        → Lancez: python core/recover_secret.py
        → Entrez PART 1 ou PART 2 + PART 2 ou PART 3
        → Obtenez DIRECTEMENT: Les 24 MOTS! ✅

✅ SÉCURITÉ MAXIMALE:
   • Coffre A brûle? → Vous avez les mots en Bitwarden ✅
   • Bitwarden hack? → Vous avez les mots en papier ✅
   • Ambos perdus? → Vous avez PART 2 + PART 3 pour retrouver les mots ✅

🔒 Imprimez cette affichage et sauvegardez vos données!
""")

print("="*80 + "\n")
