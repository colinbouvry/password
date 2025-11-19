# -*- coding: utf-8 -*-
# ============================================================================
# TESTS UNITAIRES - Shamir Robust
# ============================================================================
import sys
import os
import hashlib

# Ajouter le parent directory au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.shamir_polynomial_robust import ShamirRobust

print("\n" + "="*80)
print("TESTS UNITAIRES - SHAMIR ROBUST")
print("="*80)

# ============================================================================
# TEST 1 : Initialisation
# ============================================================================
print("\n" + "="*80)
print("TEST 1️⃣  : Initialisation de ShamirRobust")
print("="*80)

try:
    shamir = ShamirRobust()
    print("✅ PASS - Initialisation réussie")
    test1_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test1_pass = False

# ============================================================================
# TEST 2 : Génération du secret
# ============================================================================
print("\n" + "="*80)
print("TEST 2️⃣  : Génération du secret")
print("="*80)

test_passphrase = "maison plage soleil livre table chaise porte fenetre jardin arbre fleur chien chat poisson oiseau lumiere nuit jour matin soir ete hiver neige"

try:
    secret_int = shamir.generate_secret(test_passphrase)
    assert secret_int is not None, "Secret généré mais None"
    assert shamir.secret_hash is not None, "secret_hash non défini"
    assert shamir.metadata['secret_checksum'] is not None, "Checksum non défini"
    print("✅ PASS - Secret généré avec checksum")
    test2_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test2_pass = False

# ============================================================================
# TEST 3 : Division en 3 parts
# ============================================================================
print("\n" + "="*80)
print("TEST 3️⃣  : Division en 3 parts")
print("="*80)

try:
    parts, metadata = shamir.split_secret(test_passphrase)
    assert len(parts) == 3, f"Devrait avoir 3 parts, en a {len(parts)}"
    assert all(i in parts for i in [1, 2, 3]), "Parts 1, 2, 3 manquantes"
    assert all('hex' in parts[i] for i in [1, 2, 3]), "hex manquant dans parts"
    assert all('checksum' in parts[i] for i in [1, 2, 3]), "Checksum manquant"
    assert len(parts[1]['hex']) == 64, f"Part 1 devrait faire 64 chars, en a {len(parts[1]['hex'])}"
    assert metadata['threshold'] == 2, "Threshold devrait être 2"
    assert metadata['parts_count'] == 3, "parts_count devrait être 3"
    print("✅ PASS - 3 parts générées avec checksums")
    test3_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test3_pass = False

# ============================================================================
# TEST 4 : Vérification de part valide
# ============================================================================
print("\n" + "="*80)
print("TEST 4️⃣  : Vérification de part valide")
print("="*80)

try:
    valid, msg = shamir.verify_part(1, parts[1]['hex'])
    assert valid is True, f"Part valide mais retourne {valid}"
    print("✅ PASS - Part valide détectée")
    test4_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test4_pass = False

# ============================================================================
# TEST 5 : Détection de part invalide (format)
# ============================================================================
print("\n" + "="*80)
print("TEST 5️⃣  : Détection de format invalide")
print("="*80)

try:
    invalid_part = "XX" + parts[1]['hex'][2:]
    valid, msg = shamir.verify_part(1, invalid_part)
    assert valid is False, "Should detect invalid part"
    print("✅ PASS - Part invalide détectée (format hexa)")
    test5_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test5_pass = False

# ============================================================================
# TEST 6 : Détection de part corrompue (checksum)
# ============================================================================
print("\n" + "="*80)
print("TEST 6️⃣  : Détection de corruption (checksum)")
print("="*80)

try:
    corrupted_part = parts[1]['hex'][:-2] + "00"
    valid, msg = shamir.verify_part(1, corrupted_part)
    assert valid is False, "Should detect corrupted part"
    assert "Checksum" in msg or "CORRUPTION" in msg, f"Message unclear: {msg}"
    print("✅ PASS - Part corrompue détectée (checksum invalide)")
    test6_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test6_pass = False

# ============================================================================
# TEST 7 : Récupération du secret (Part 1 + Part 2)
# ============================================================================
print("\n" + "="*80)
print("TEST 7️⃣  : Récupération avec Part 1 + Part 2")
print("="*80)

try:
    recovered = shamir.recover_secret(1, parts[1]['hex'], 2, parts[2]['hex'])
    assert recovered is not None, "Passphrase non récupérée"
    assert isinstance(recovered, str), "Devrait retourner une string (passphrase)"
    assert recovered == test_passphrase, "Passphrase ne correspond pas"
    print("✅ PASS - Passphrase récupérée correctement")
    test7_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test7_pass = False

# ============================================================================
# TEST 8 : Récupération du secret (Part 1 + Part 3)
# ============================================================================
print("\n" + "="*80)
print("TEST 8️⃣  : Récupération avec Part 1 + Part 3")
print("="*80)

try:
    recovered = shamir.recover_secret(1, parts[1]['hex'], 3, parts[3]['hex'])
    assert recovered is not None, "Passphrase non récupérée"
    assert isinstance(recovered, str), "Devrait retourner une string (passphrase)"
    assert recovered == test_passphrase, "Passphrase ne correspond pas"
    print("✅ PASS - Passphrase récupérée correctement")
    test8_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test8_pass = False

# ============================================================================
# TEST 9 : Récupération du secret (Part 2 + Part 3)
# ============================================================================
print("\n" + "="*80)
print("TEST 9️⃣  : Récupération avec Part 2 + Part 3")
print("="*80)

try:
    recovered = shamir.recover_secret(2, parts[2]['hex'], 3, parts[3]['hex'])
    assert recovered is not None, "Passphrase non récupérée"
    assert isinstance(recovered, str), "Devrait retourner une string (passphrase)"
    assert recovered == test_passphrase, "Passphrase ne correspond pas"
    print("✅ PASS - Passphrase récupérée correctement")
    test9_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test9_pass = False

# ============================================================================
# TEST 10 : Récupération avec part corrompue
# ============================================================================
print("\n" + "="*80)
print("TEST 10️⃣  : Rejet de part corrompue")
print("="*80)

try:
    corrupted = parts[1]['hex'][:-2] + "00"
    recovered = shamir.recover_secret(1, corrupted, 2, parts[2]['hex'])
    assert recovered is None, "Should reject corrupted part"
    print("✅ PASS - Part corrompue rejetée")
    test10_pass = True
except Exception as e:
    print(f"❌ FAIL - {e}")
    test10_pass = False

# ============================================================================
# RÉSUMÉ
# ============================================================================
print("\n" + "="*80)
print("RÉSUMÉ DES TESTS UNITAIRES")
print("="*80)

tests = [
    ("1. Initialisation", test1_pass),
    ("2. Génération du secret", test2_pass),
    ("3. Division en 3 parts", test3_pass),
    ("4. Vérification de part valide", test4_pass),
    ("5. Détection format invalide", test5_pass),
    ("6. Détection corruption (checksum)", test6_pass),
    ("7. Récupération Part 1+2", test7_pass),
    ("8. Récupération Part 1+3", test8_pass),
    ("9. Récupération Part 2+3", test9_pass),
    ("10. Rejet part corrompue", test10_pass),
]

passed = sum(1 for _, result in tests if result)
total = len(tests)

for name, result in tests:
    status = "✅" if result else "❌"
    print(f"{status} {name}")

print(f"\nTests réussis : {passed}/{total}")

if passed == total:
    print("\n🎉 TOUS LES TESTS UNITAIRES PASSENT !")
else:
    print(f"\n⚠️  {total - passed} test(s) échoué(s)")

print("="*80 + "\n")

sys.exit(0 if passed == total else 1)
