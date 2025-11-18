# -*- coding: utf-8 -*-
# ============================================================================
# TESTS D'INTÉGRATION - Shamir Robust
# Test du flux complet : Génération → Division → Récupération
# ============================================================================
import sys
import os
import time
import random
import hashlib

# Ajouter le parent directory au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.shamir_polynomial_robust import ShamirRobust
from core.mots import MOTS  # IMPORT de la liste centralisée (SANS DUPLICATION)

print("\n" + "="*80)
print("TESTS D'INTÉGRATION - SHAMIR ROBUST")
print("="*80)

# ============================================================================
# SETUP : Générer une passphrase aléatoire
# ============================================================================
print("\n" + "="*80)
print("SETUP : Génération d'une passphrase aléatoire (utilise core/mots.py)")
print("="*80)

raw_entropy = time.time_ns()
random.seed(raw_entropy)
random.shuffle(MOTS)

passphrase = " ".join(MOTS[:24])
print(f"✅ Passphrase générée : {passphrase[:50]}...")

# ============================================================================
# TEST 1 : Flux complet - Génération + Division
# ============================================================================
print("\n" + "="*80)
print("TEST 1️⃣  : Flux complet (Génération + Division)")
print("="*80)

try:
    shamir = ShamirRobust()
    parts, metadata = shamir.split_secret(passphrase)

    assert len(parts) == 3, "Devrait avoir 3 parts"
    assert all(i in parts for i in [1, 2, 3]), "Parts manquantes"

    print("✅ PASS - Division en 3 parts réussie")
    test1_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test1_pass = False

# ============================================================================
# TEST 2 : Récupération avec Part 1 + Part 2
# ============================================================================
print("\n" + "="*80)
print("TEST 2️⃣  : Récupération avec Part 1 + Part 2")
print("="*80)

try:
    recovered1 = shamir.recover_secret(1, parts[1]['hex'], 2, parts[2]['hex'])

    assert recovered1 is not None, "Secret non récupéré"
    assert recovered1.hex() == shamir.secret_hash.hex(), "Hash ne correspond pas"

    print("✅ PASS - Part 1 + Part 2 récupère le secret")
    test2_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test2_pass = False

# ============================================================================
# TEST 3 : Récupération avec Part 1 + Part 3
# ============================================================================
print("\n" + "="*80)
print("TEST 3️⃣  : Récupération avec Part 1 + Part 3")
print("="*80)

try:
    recovered2 = shamir.recover_secret(1, parts[1]['hex'], 3, parts[3]['hex'])

    assert recovered2 is not None, "Secret non récupéré"
    assert recovered2.hex() == shamir.secret_hash.hex(), "Hash ne correspond pas"

    print("✅ PASS - Part 1 + Part 3 récupère le secret")
    test3_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test3_pass = False

# ============================================================================
# TEST 4 : Récupération avec Part 2 + Part 3
# ============================================================================
print("\n" + "="*80)
print("TEST 4️⃣  : Récupération avec Part 2 + Part 3")
print("="*80)

try:
    recovered3 = shamir.recover_secret(2, parts[2]['hex'], 3, parts[3]['hex'])

    assert recovered3 is not None, "Secret non récupéré"
    assert recovered3.hex() == shamir.secret_hash.hex(), "Hash ne correspond pas"

    print("✅ PASS - Part 2 + Part 3 récupère le secret")
    test4_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test4_pass = False

# ============================================================================
# TEST 5 : Tous les secrets récupérés sont identiques
# ============================================================================
print("\n" + "="*80)
print("TEST 5️⃣  : Vérification de cohérence (tous les secrets identiques)")
print("="*80)

try:
    assert recovered1 == recovered2, "Secret 1 ≠ Secret 2"
    assert recovered2 == recovered3, "Secret 2 ≠ Secret 3"
    assert recovered1.hex() == shamir.secret_hash.hex(), "Secret ≠ Hash original"

    print("✅ PASS - Tous les secrets récupérés sont identiques")
    test5_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test5_pass = False

# ============================================================================
# TEST 6 : Détection de corruption lors du flux
# ============================================================================
print("\n" + "="*80)
print("TEST 6️⃣  : Détection de corruption dans le flux")
print("="*80)

try:
    # Corrompt Part 1
    corrupted_part1 = parts[1]['hex'][:-2] + "00"
    recovered_bad = shamir.recover_secret(1, corrupted_part1, 2, parts[2]['hex'])

    assert recovered_bad is None, "Should reject corrupted part"

    print("✅ PASS - Corruption détectée et rejetée")
    test6_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test6_pass = False

# ============================================================================
# TEST 7 : Métadonnées correctes
# ============================================================================
print("\n" + "="*80)
print("TEST 7️⃣  : Vérification des métadonnées")
print("="*80)

try:
    assert metadata['threshold'] == 2, "Threshold incorrect"
    assert metadata['parts_count'] == 3, "parts_count incorrect"
    assert 'secret_checksum' in metadata, "secret_checksum manquant"
    assert 'global_checksum' in metadata, "global_checksum manquant"
    assert 'timestamp' in metadata, "timestamp manquant"

    print("✅ PASS - Métadonnées complètes et correctes")
    test7_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test7_pass = False

# ============================================================================
# TEST 8 : Checksums différents pour parts différentes
# ============================================================================
print("\n" + "="*80)
print("TEST 8️⃣  : Unicité des checksums")
print("="*80)

try:
    checksums = [parts[i]['checksum'] for i in [1, 2, 3]]
    assert len(set(checksums)) == 3, "Les checksums doivent être uniques"

    print("✅ PASS - Chaque part a un checksum unique")
    test8_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test8_pass = False

# ============================================================================
# RÉSUMÉ
# ============================================================================
print("\n" + "="*80)
print("RÉSUMÉ DES TESTS D'INTÉGRATION")
print("="*80)

tests = [
    ("1. Flux complet (Génération + Division)", test1_pass),
    ("2. Récupération Part 1 + Part 2", test2_pass),
    ("3. Récupération Part 1 + Part 3", test3_pass),
    ("4. Récupération Part 2 + Part 3", test4_pass),
    ("5. Cohérence des secrets", test5_pass),
    ("6. Détection de corruption", test6_pass),
    ("7. Métadonnées complètes", test7_pass),
    ("8. Unicité des checksums", test8_pass),
]

passed = sum(1 for _, result in tests if result)
total = len(tests)

for name, result in tests:
    status = "✅" if result else "❌"
    print(f"{status} {name}")

print(f"\nTests réussis : {passed}/{total}")

if passed == total:
    print("\n🎉 TOUS LES TESTS D'INTÉGRATION PASSENT !")
else:
    print(f"\n⚠️  {total - passed} test(s) échoué(s)")

print("="*80 + "\n")

sys.exit(0 if passed == total else 1)
