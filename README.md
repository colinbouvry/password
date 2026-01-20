# Shamir Secret Sharing 2-of-3 + BIP39

Systeme cryptographique pour archiver un Master Password Bitwarden (24 mots) de maniere permanente (50-500 ans).

## Fonctionnalites

- **Shamir 2-of-3** : Divise le secret en 3 parts, 2 suffisent pour recuperer
- **BIP39** : Conversion HEX <-> 24 mots (standard Bitcoin)
- **Standalone** : Fonctionne sans dependances externes
- **EXE** : Executable portable pour Windows

## Structure du projet

```
e:\dev\password\
├── core/
│   ├── shamir_polynomial_robust.py   # Moteur Shamir 2-of-3
│   ├── generate_secret.py            # Generation 24 mots + 3 PARTS
│   ├── recover_secret.py             # Recuperation interactive
│   ├── recover_secret_standalone.py  # Version standalone (zero deps)
│   ├── convert_hex_to_24words.py     # Conversion HEX <-> 24 mots
│   └── mots.py                       # Liste 2048 mots BIP39
│
├── tests/
│   ├── test_unit.py                  # Tests unitaires
│   ├── test_integration.py           # Tests integration
│   └── test_hex_to_words.py          # Tests conversion (2002 tests)
│
├── dist/
│   └── Shamir_Recover.exe            # Executable Windows
│
├── build_exe.bat                     # Script compilation EXE
├── gravure_launcher.py               # Menu templates gravure
└── shamir_metadata.json              # Donnees generees (SECURISER!)
```

## Usage rapide

### 1. Generer un secret

```bash
python core/generate_secret.py
```

Resultat :
- 24 mots BIP39 (passphrase)
- 3 PARTS en format HEX et 24 mots
- Fichier `shamir_metadata.json`

### 2. Recuperer le secret

```bash
python core/recover_secret.py
```

- Entrer 2 PARTS (HEX ou 24 mots)
- Recupere la passphrase originale

### 3. Lancer les tests

```bash
python tests/test_hex_to_words.py
```

Resultat attendu : `2002/2002 tests PASSED`

## Securite Shamir

```
Polynome: f(x) = secret + a*x (mod PRIME)

Parts:
  Part1 = f(1)
  Part2 = f(2)
  Part3 = f(3)

Recuperation:
  2 points -> interpolation Lagrange -> f(0) = secret
  1 point seul = ZERO information
```

**Domaine** : secp256k1 (PRIME = 2^256 - 2^32 - 977)

## Distribution recommandee

```
COFFRE A (Maison):
  ├── Papier plastifie (24 mots)
  ├── Cle USB (code + EXE)
  └── PART 1 enveloppe scellee

COFFRE B (Banque):
  ├── Plaque acier gravee (24 mots)
  ├── Cle USB backup
  └── PART 2 enveloppe scellee

COFFRE C (Parent/Ami):
  └── PART 3 enveloppe scellee
```

## Gravure acier

```bash
python gravure_launcher.py
```

Options :
1. **Gravure simple** (HEX direct) - 30-60 EUR
2. **Gravure manuelle** (Mots + PARTS) - 10-50 EUR (recommandee)
3. **Plaque laser pro** - 150-300 EUR

## Compilation EXE

```bash
build_exe.bat
```

Voir [BUILD_EXE_GUIDE.md](BUILD_EXE_GUIDE.md) pour details.

## Tests valides

| Suite | Tests | Status |
|-------|-------|--------|
| Unit tests | 10 | PASS |
| Integration | 8 | PASS |
| HEX <-> Words | 2002 | PASS |

## Workflow de recuperation

```
CAS NORMAL:
  Coffre A -> Lire papier -> Bitwarden -> 2 min

CAS CATASTROPHE:
  PART 1 + PART 2 -> recover_secret.py -> 24 mots -> 30 min

CAS EXTREME:
  Notepad shamir_metadata.json -> 24 mots en clair -> 5 min
```

## Fichiers critiques

| Fichier | Importance | Duree |
|---------|------------|-------|
| 24 mots (papier) | CRITIQUE | 100+ ans |
| shamir_metadata.json | CRITIQUE | 100 ans |
| PARTS 1,2,3 | Important | infini |
| Shamir_Recover.exe | Utile | 50 ans |

## Depannage

**"ModuleNotFoundError"**
```bash
cd e:\dev\password
python core/generate_secret.py
```

**"Format hexa invalide"**
- Verifier 64 caracteres hexadecimaux
- Pas d'espaces avant/apres

**"Checksum ne correspond pas"**
- La part a ete modifiee
- Recuperer depuis la source originale

## Specifications techniques

- **Algorithme** : Shamir Secret Sharing (2-of-3)
- **Entropie** : 256 bits
- **Checksum** : SHA256 (8 bits pour BIP39)
- **Wordlist** : 2048 mots BIP39 anglais
- **Encodage** : UTF-8

---

Version: 3.0 FINAL
Status: Production-ready
Cree: 2025-11-19
