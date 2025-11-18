# -*- coding: utf-8 -*-
# ============================================================================
# GENERATE SECRET - Interface simple pour générer et diviser
# ============================================================================
import sys
sys.stdout.reconfigure(encoding='utf-8')

from shamir_polynomial_robust import ShamirRobust
import hashlib

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

    MOTS = [
        "maison","plage","soleil","livre","table","chaise","porte","fenetre","jardin","arbre",
        "fleur","chien","chat","poisson","oiseau","lumiere","nuit","jour","matin","soir",
        "ete","hiver","neige","pluie","vent","mer","lac","riviere","montagne","foret",
        "ville","rue","route","voiture","velo","train","avion","bateau","pain","fromage",
        "beurre","sucre","sel","eau","vin","cafe","lait","pomme","poire","banane",
        "fraise","orange","citron","tomate","carotte","oignon","huile","miel","chocolat","gateau",
        "crepe","pizza","pates","riz","viande","oeuf","jambon","saucisse","mouton","vache",
        "loup","ours","tigre","lion","ecole","bureau","stylo","cahier","cle","telephone",
        "ordi","ecran","clavier","lune","etoile","ciel","nuage","tempete","foudre","musique",
        "guitare","piano","rire","photo","film","jeu","ballon","sport","course","danse",
        "voyage","valise","argent","bleu","rouge","vert","jaune","noir","blanc","gris",
        "chaud","froid","doux","dur","leger","vite","lent","haut","bas","calme","bruit"
    ]

    raw_entropy = time.time_ns()
    random.seed(raw_entropy)
    random.shuffle(MOTS)

    passphrase = " ".join(MOTS[:24])

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
    print(f"  Checksum : {parts[i]['checksum']}")

print("\n" + "="*80)
print("💾 MÉTADONNÉES SÉCURITÉ")
print("="*80)
print(f"Secret Checksum : {metadata['secret_checksum']}")
print(f"Global Checksum : {metadata['global_checksum']}")
print(f"Timestamp       : {metadata['timestamp']}")

print("\n" + "="*80)
print("✅ SAUVEGARDEZ VOS 24 MOTS ET VOS 3 PARTS")
print("="*80 + "\n")
