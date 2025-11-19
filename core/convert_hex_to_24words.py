#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convertit HEX PART Shamir en 24 mots lisibles pour gravure
Approche simple: on utilise juste la conversion pour affichage

Les 24 mots sont une REPRÉSENTATION des hex pour faciliter la gravure
(pas une inversion cryptographique)
"""

import sys
import os
import hashlib

if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent_dir)

from mots import MOTS


def hex_to_words_bip39(hex_str):
    """
    Convertit 256 bits (64 chars hex) → 24 mots BIP39

    Standard BIP39: 256 bits entropy + 8 bits checksum = 264 bits = 24 × 11 bits
    """

    if len(hex_str) != 64:
        raise ValueError(f"Besoin 64 chars, tu as {len(hex_str)}")

    # 1. Convertit hex → bytes (32 bytes)
    entropy = bytes.fromhex(hex_str)

    # 2. Calcule checksum SHA256
    h = hashlib.sha256(entropy).digest()

    # 3. Prend les 8 premiers bits du checksum
    checksum_bits = bin(h[0])[2:].zfill(8)[:8]

    # 4. Combine entropy + checksum en bits
    entropy_bits = ''.join(format(byte, '08b') for byte in entropy)
    bits = entropy_bits + checksum_bits

    # 5. Divise en chunks de 11 bits → index dans wordlist
    words = []
    for i in range(0, len(bits), 11):
        chunk = bits[i:i+11]
        idx = int(chunk, 2)
        words.append(MOTS[idx])

    return words


def words_to_hex_bip39(words):
    """
    Convertit 24 mots BIP39 → 256 bits (64 chars hex)

    Inverse de hex_to_words_bip39
    """

    if len(words) != 24:
        raise ValueError(f"Besoin 24 mots, tu as {len(words)}")

    # 1. Convertit mots → indices → bits
    bits = ''
    for word in words:
        idx = MOTS.index(word.lower())
        bits += format(idx, '011b')

    # 2. Sépare entropy (256 bits) et checksum (8 bits)
    entropy_bits = bits[:256]
    checksum_bits = bits[256:264]

    # 3. Convertit entropy bits → bytes
    entropy = bytes(int(entropy_bits[i:i+8], 2) for i in range(0, 256, 8))

    # 4. Vérifie checksum
    h = hashlib.sha256(entropy).digest()
    expected_checksum = bin(h[0])[2:].zfill(8)[:8]

    if checksum_bits != expected_checksum:
        raise ValueError("Checksum invalide! Les mots ne correspondent pas à l'original")

    # 5. Convertit en hex
    return entropy.hex()


def main():
    print("\n" + "="*80)
    print("CONVERTIR PARTS SHAMIR → 24 MOTS (BIP39 Standard)")
    print("="*80)

    while True:
        print("\nChoix:")
        print("1. HEX (64 chars) → 24 MOTS")
        print("2. 24 MOTS → HEX (64 chars)")
        print("3. TEST: HEX → MOTS → HEX (vérifier exactitude)")
        print("0. Quitter\n")

        choice = input("Choix (0-3): ").strip()

        if choice == "0":
            print("Au revoir!")
            break

        elif choice == "1":
            print("\nColle HEX PART (64 caractères):")
            hex_input = input("> ").strip().lower()

            try:
                words = hex_to_words_bip39(hex_input)

                print("\n" + "="*80)
                print("RÉSULTAT - 24 MOTS")
                print("="*80)
                print("\nMots:")
                for i, w in enumerate(words, 1):
                    print(f"  {i:2d}. {w}")

                print("\nLigne complète:")
                print("  " + " ".join(words))

                # Sauvegarde
                with open("part_as_24words.txt", "w", encoding='utf-8') as f:
                    for i, w in enumerate(words, 1):
                        f.write(f"{i:2d}. {w}\n")
                    f.write("\n" + " ".join(words))

                print("\n✅ Sauvegardé dans: part_as_24words.txt")

            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "2":
            print("\nColle 24 mots (séparés par espaces ou Enter):")
            words = []
            try:
                while len(words) < 24:
                    line = input(f"Mots {len(words)+1}-{min(len(words)+6, 24)}: ").strip().lower()
                    if not line:
                        continue
                    words.extend(line.split())

                words = words[:24]
                hex_result = words_to_hex_bip39(words)

                print("\n" + "="*80)
                print("RÉSULTAT - HEX")
                print("="*80)
                print(f"\n{hex_result}")

                with open("part_as_hex.txt", "w", encoding='utf-8') as f:
                    f.write(hex_result)

                print("\n✅ Sauvegardé dans: part_as_hex.txt")

            except Exception as e:
                print(f"❌ Erreur: {e}")

        elif choice == "3":
            test_hex = "380e8fb7ad86fc83f440780e31fea61104585dd2a341e46477f8bcb4bda3b4e7"
            print(f"\nTest avec HEX: {test_hex}")

            try:
                print("HEX → MOTS...")
                words = hex_to_words_bip39(test_hex)
                print(f"MOTS: {' '.join(words)}")

                print("\nMOTS → HEX...")
                hex_back = words_to_hex_bip39(words)
                print(f"HEX: {hex_back}")

                if test_hex == hex_back:
                    print("\n✅ PARFAIT! Conversion bidirectionnelle réussie!")
                else:
                    print(f"\n❌ MISMATCH!")
                    print(f"  Original: {test_hex}")
                    print(f"  Reconverti: {hex_back}")

            except Exception as e:
                print(f"❌ Erreur: {e}")

        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAnnulé")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
