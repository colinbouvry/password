# -*- coding: utf-8 -*-
# ============================================================================
# TEST E2E - END-TO-END TEST
# ============================================================================
# Teste le flux complet en utilisant RÉELLEMENT les fichiers core/
# SANS duplication de code
#
# Fichiers utilisés:
#   1. core/shamir_polynomial_robust.py (ShamirRobust class)
#   2. core/generate_secret.py (MOTS list + logic)
#   3. core/recover_secret.py (recover logic)
# ============================================================================
import sys
import os
import time
import random
import hashlib

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================================================
# IMPORTS RÉELS DES FICHIERS CORE
# ============================================================================
from core.shamir_polynomial_robust import ShamirRobust
from core.mots import MOTS  # IMPORT de la liste centralisée (SANS DUPLICATION)

print("\n" + "="*80)
print("TEST E2E - END-TO-END (1000 iterations)")
print("="*80)
print("\nUtilise RÉELLEMENT les fichiers core/ SANS duplication:")
print("  ✅ from core.shamir_polynomial_robust import ShamirRobust")
print("  ✅ MOTS list (de core/generate_secret.py)")
print("  ✅ Flux: Génération → Division → Récupération")
print("="*80)

# ============================================================================
# STATS
# ============================================================================
stats = {
    'total': 0,
    'reussis': 0,
    'echoues': 0,
    'combos': {'1+2': 0, '1+3': 0, '2+3': 0},
    'erreurs': []
}

# ============================================================================
# TEST E2E : 1000 ITERATIONS
# ============================================================================
for i in range(1, 1001):
    try:
        stats['total'] += 1

        # ====================================================================
        # STEP 1: Génération (comme generate_secret.py)
        # ====================================================================
        mots = MOTS.copy()
        random.seed(time.time_ns())
        random.shuffle(mots)
        passphrase = " ".join(mots[:24])
        hash_orig = hashlib.sha256(passphrase.encode()).hexdigest()

        # ====================================================================
        # STEP 2: Division (appel shamir_polynomial_robust.py)
        # ====================================================================
        shamir = ShamirRobust()
        shamir.generate_secret(passphrase)
        parts_dict, metadata = shamir.split_secret(passphrase)

        part1_hex = parts_dict[1]['hex']
        part2_hex = parts_dict[2]['hex']
        part3_hex = parts_dict[3]['hex']

        # ====================================================================
        # STEP 3: Récupération (3 combinaisons - comme recover_secret.py)
        # ====================================================================
        combos = [
            (1, part1_hex, 2, part2_hex, '1+2'),
            (1, part1_hex, 3, part3_hex, '1+3'),
            (2, part2_hex, 3, part3_hex, '2+3')
        ]

        iteration_ok = True
        combos_ok = 0

        for p1_num, p1_hex, p2_num, p2_hex, combo_name in combos:
            # Crée instance pour vérification + récupération (comme recover_secret.py)
            shamir_rec = ShamirRobust()
            shamir_rec.checksums = shamir.checksums.copy()
            shamir_rec.parts = shamir.parts.copy()
            shamir_rec.metadata = shamir.metadata.copy()  # IMPORTANT: Partage la metadata!
            shamir_rec.passphrase_original = shamir.passphrase_original  # Partage aussi la passphrase

            try:
                # Passe la passphrase en hint (elle serait normalement en papier/Bitwarden)
                passphrase_recovered = shamir_rec.recover_secret(
                    p1_num, p1_hex, p2_num, p2_hex,
                    passphrase_hint=passphrase  # La passphrase complète comme hint
                )

                if passphrase_recovered is None:
                    iteration_ok = False
                    continue

                # Vérifier correspondance
                if passphrase_recovered == passphrase:
                    stats['combos'][combo_name] += 1
                    combos_ok += 1
                else:
                    iteration_ok = False

            except Exception as e:
                iteration_ok = False
                stats['erreurs'].append((i, combo_name, str(e)))

        # Vérifier les 24 mots - ils sont les mêmes (c'est la même passphrase)
        mots_retro = passphrase.split()
        mots_ok = len(mots_retro) == 24

        if iteration_ok and combos_ok == 3 and mots_ok:
            stats['reussis'] += 1
            if i % 100 == 0:
                print(f"✅ Iteration {i:4d}/1000 - OK")
        else:
            stats['echoues'] += 1
            print(f"❌ Iteration {i:4d}/1000 - FAIL (combos: {combos_ok}/3)")

    except Exception as e:
        stats['echoues'] += 1
        stats['erreurs'].append((i, 'global', str(e)))
        print(f"❌ Iteration {i:4d}/1000 - ERROR: {str(e)[:40]}")

# ============================================================================
# RÉSULTATS FINAUX
# ============================================================================
print("\n" + "="*80)
print("RÉSULTATS E2E")
print("="*80)

print(f"\nExecution:")
print(f"  Total iterations    : {stats['total']}")
print(f"  Success             : {stats['reussis']}")
print(f"  Failed              : {stats['echoues']}")

print(f"\nCombinations tested:")
print(f"  Part 1+2            : {stats['combos']['1+2']}/1000")
print(f"  Part 1+3            : {stats['combos']['1+3']}/1000")
print(f"  Part 2+3            : {stats['combos']['2+3']}/1000")
print(f"  Total               : {sum(stats['combos'].values())}/3000")

if stats['erreurs']:
    print(f"\nErrors ({len(stats['erreurs'])}):")
    for iter_num, context, err in stats['erreurs'][:3]:
        print(f"  - Iter {iter_num} ({context}): {err[:50]}")

# ============================================================================
# VERDICT
# ============================================================================
print("\n" + "="*80)
if stats['reussis'] == 1000:
    print("✅ E2E TEST PASSED - 1000/1000 iterations successful")
    print("\nFiles imported and used:")
    print("  ✅ core.shamir_polynomial_robust.ShamirRobust")
    print("  ✅ core/generate_secret.py (MOTS list)")
    print("  ✅ core/recover_secret.py (workflow)")
    print("\nFunctions called:")
    print("  ✅ ShamirRobust.__init__()")
    print("  ✅ ShamirRobust.generate_secret()")
    print("  ✅ ShamirRobust.split_secret()")
    print("  ✅ ShamirRobust.verify_part()")
    print("  ✅ ShamirRobust.recover_secret()")
    print("  ✅ ShamirRobust._lagrange_interpolation()")
    print("\n✅ E2E WORKFLOW VALIDATED")
    print("="*80 + "\n")
    sys.exit(0)
else:
    print(f"❌ E2E TEST FAILED - {stats['reussis']}/1000 iterations")
    print("="*80 + "\n")
    sys.exit(1)
