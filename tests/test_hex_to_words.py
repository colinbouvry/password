#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test unitaire pour conversion HEX ↔ 24 MOTS BIP39
Valide la conversion bidirectionnelle 1000 fois
"""

import sys
import os
import random

# Ajoute le parent dir au path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from core.convert_hex_to_24words import (
    hex_to_words_bip39,
    words_to_hex_bip39,
)
from core.mots import MOTS


def test_single_hex_to_words():
    """Test conversion hex → mots une fois"""
    hex_part = "380e8fb7ad86fc83f440780e31fea61104585dd2a341e46477f8bcb4bda3b4e7"
    words = hex_to_words_bip39(hex_part)

    assert len(words) == 24, f"Besoin 24 mots, obtenu {len(words)}"
    assert all(word in MOTS for word in words), "Un ou plusieurs mots invalides"
    print(f"✓ HEX → 24 mots: {' '.join(words[:3])}... OK")
    return words


def test_single_words_to_hex():
    """Test conversion mots → hex une fois"""
    words = [
        "day", "inner", "unknown", "force", "hurt", "draft",
        "speed", "audit", "athlete", "morning", "praise", "capital",
        "easily", "confirm", "enhance", "habit", "tongue", "casual",
        "wreck", "just", "envelope", "spike", "squeeze", "toast"
    ]
    hex_part = words_to_hex_bip39(words)

    assert len(hex_part) == 64, f"Hex doit faire 64 chars, obtenu {len(hex_part)}"
    assert all(c in "0123456789abcdef" for c in hex_part), "Hex invalide"
    print(f"✓ 24 mots → HEX: {hex_part[:16]}... OK")
    return hex_part


def test_roundtrip_hex_words_hex(hex_input):
    """Test aller-retour: hex → mots → hex"""
    # hex → mots
    words = hex_to_words_bip39(hex_input)

    # mots → hex
    hex_output = words_to_hex_bip39(words)

    # Vérifie que c'est identique
    if hex_input == hex_output:
        return True, hex_output
    else:
        return False, (hex_input, hex_output)


def test_roundtrip_words_hex_words(words_input):
    """Test aller-retour: mots → hex → mots"""
    # mots → hex
    hex_part = words_to_hex_bip39(words_input)

    # hex → mots
    words_output = hex_to_words_bip39(hex_part)

    # Vérifie que c'est identique
    if words_input == words_output:
        return True, words_output
    else:
        return False, (words_input, words_output)


def test_1000_random_hex():
    """Test 1000 conversions aléatoires hex → mots → hex"""
    print("\n" + "="*80)
    print("TEST 1000× RANDOM HEX → MOTS → HEX")
    print("="*80)

    passed = 0
    failed = 0
    errors = []

    for i in range(1000):
        try:
            # Génère hex aléatoire (64 chars)
            random_hex = format(random.randint(0, 2**256-1), '064x')

            # Test aller-retour
            success, result = test_roundtrip_hex_words_hex(random_hex)

            if success:
                passed += 1
                if (i + 1) % 100 == 0:
                    print(f"  [{i+1:4d}/1000] OK")
            else:
                failed += 1
                errors.append((i, random_hex, result))
                print(f"  [{i+1:4d}/1000] FAIL")

        except Exception as e:
            failed += 1
            errors.append((i, random_hex, str(e)))
            print(f"  [{i+1:4d}/1000] ERROR: {e}")

    print(f"\nResultat: {passed}/1000 passed, {failed}/1000 failed")

    if errors:
        print("\nErrors:")
        for idx, hex_val, error in errors[:5]:
            print(f"  Iteration {idx}: {error}")

    assert failed == 0, f"{failed} test(s) failed"
    return passed


def test_1000_random_words():
    """Test 1000 conversions aléatoires mots → hex → mots

    NOTE: Génère d'abord des hex valides, les convertit en mots,
    puis teste la conversion inverse. Les mots aléatoires purs
    auraient 99.6% d'échec sur checksum BIP39.
    """
    print("\n" + "="*80)
    print("TEST 1000× RANDOM MOTS → HEX → MOTS (via HEX valide)")
    print("="*80)

    passed = 0
    failed = 0
    errors = []

    for i in range(1000):
        try:
            # Génère hex aléatoire valide
            random_hex = format(random.randint(0, 2**256-1), '064x')

            # Convertit en mots (avec checksum correct)
            random_words = hex_to_words_bip39(random_hex)

            # Test aller-retour: mots → hex → mots
            success, result = test_roundtrip_words_hex_words(random_words)

            if success:
                passed += 1
                if (i + 1) % 100 == 0:
                    print(f"  [{i+1:4d}/1000] OK")
            else:
                failed += 1
                errors.append((i, random_words[:3], result))
                print(f"  [{i+1:4d}/1000] FAIL")

        except Exception as e:
            failed += 1
            errors.append((i, "N/A", str(e)))
            print(f"  [{i+1:4d}/1000] ERROR: {e}")

    print(f"\nResultat: {passed}/1000 passed, {failed}/1000 failed")

    if errors:
        print("\nErrors:")
        for idx, words_val, error in errors[:5]:
            print(f"  Iteration {idx}: {error}")

    assert failed == 0, f"{failed} test(s) failed"
    return passed


def test_edge_cases():
    """Test cas limites"""
    print("\n" + "="*80)
    print("TEST CAS LIMITES")
    print("="*80)

    # Test 1: Tous les zéros
    print("  Test 1: Hex tout zeros...")
    hex_zeros = "00" * 32
    words = hex_to_words_bip39(hex_zeros)
    assert len(words) == 24
    hex_back = words_to_hex_bip39(words)
    assert hex_zeros == hex_back
    print(f"    OK - {words[0]} ... {words[-1]}")

    # Test 2: Tous les FF
    print("  Test 2: Hex tout FF...")
    hex_ones = "ff" * 32
    words = hex_to_words_bip39(hex_ones)
    assert len(words) == 24
    hex_back = words_to_hex_bip39(words)
    assert hex_ones == hex_back
    print(f"    OK - {words[0]} ... {words[-1]}")

    # Test 3: Alternance
    print("  Test 3: Hex alternance...")
    hex_alt = ("aa" * 16 + "55" * 16)
    words = hex_to_words_bip39(hex_alt)
    assert len(words) == 24
    hex_back = words_to_hex_bip39(words)
    assert hex_alt == hex_back
    print(f"    OK - {words[0]} ... {words[-1]}")

    print("\n  Tous cas limites OK")


def main():
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  TEST UNITAIRE - HEX ↔ 24 MOTS BIP39".center(78) + "█")
    print("█" + "  Bidirectionnel (2000 iterations + edge cases)".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)

    # Tests simples
    print("\n" + "="*80)
    print("TESTS SIMPLES")
    print("="*80)

    words = test_single_hex_to_words()
    hex_part = test_single_words_to_hex()

    # Tests aller-retour
    passed_hex = test_1000_random_hex()
    passed_words = test_1000_random_words()

    # Tests cas limites
    test_edge_cases()

    # Résumé
    print("\n" + "="*80)
    print("RÉSUMÉ FINAL")
    print("="*80)
    print(f"OK - Test simple HEX → 24 mots: PASS")
    print(f"OK - Test simple 24 mots → HEX: PASS")
    print(f"OK - Test 1000× HEX → MOTS → HEX: {passed_hex}/1000 PASS")
    print(f"OK - Test 1000× MOTS → HEX → MOTS: {passed_words}/1000 PASS")
    print(f"OK - Test cas limites: PASS")
    print(f"\nOK - TOTAL: 2002/2002 tests PASSED")
    print("="*80)


if __name__ == "__main__":
    try:
        main()
        print("\nOK - TOUS LES TESTS REUSSIS!")
    except AssertionError as e:
        print(f"\nFAIL - ASSERTION: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nFAIL - ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
