# -*- coding: utf-8 -*-
# ============================================================================
# RECOVER SECRET - Interface simple pour récupérer un secret
# ============================================================================
import sys
sys.stdout.reconfigure(encoding='utf-8')

from shamir_polynomial_robust import ShamirRobust

print("\n" + "="*80)
print("RÉCUPÉRER UN SECRET - SHAMIR ROBUST")
print("="*80)

print("\nVous pouvez utiliser n'importe quelles 2 parts sur 3.")
print("Les 3 parts vous permettront aussi de récupérer le secret.")

shamir = ShamirRobust()

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

# Récupère le secret
print("\n" + "="*80)
print("RÉCUPÉRATION")
print("="*80)

secret = shamir.recover_secret(p1_num, p1_hex, p2_num, p2_hex)

if secret:
    secret_hex = secret.hex()
    print("\n" + "="*80)
    print("✅ SUCCÈS !")
    print("="*80)
    print(f"\nHash SHA256 du secret retrouvé :")
    print(f"  {secret_hex}")
    print("\n✅ Comparez avec votre hash original pour confirmer.")
else:
    print("\n❌ Impossible de récupérer le secret")
    print("Vérifiez vos parts et réessayez.")

print("\n" + "="*80 + "\n")
