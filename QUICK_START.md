# Quick Start Guide

## Verification

```bash
cd e:\dev\password
python tests/test_hex_to_words.py
```

Resultat attendu : `2002/2002 tests PASSED`

---

## Generer un secret (3 PARTS)

```bash
python core/generate_secret.py
```

Resultat :
1. Genere 24 mots BIP39 aleatoires
2. Cree 3 Shamir PARTS (seuil 2-of-3)
3. Affiche chaque PART en deux formats :
   - **HEX** : 64 caracteres
   - **24 MOTS** : format lisible pour gravure

---

## Recuperer le secret

```bash
python core/recover_secret.py
```

Resultat :
1. Demande 2 PARTS sur 3
2. Accepte HEX ou 24 mots pour chaque PART
3. Recupere la passphrase originale de 24 mots

---

## Commandes principales

| Commande | Description |
|----------|-------------|
| `python tests/test_hex_to_words.py` | Lancer 2002 tests |
| `python core/generate_secret.py` | Generer 3 PARTS |
| `python core/recover_secret.py` | Recuperer depuis 2 PARTS |

---

## Fonctionnalites

- **Conversion bidirectionnelle HEX <-> 24 mots** : Roundtrip parfait, standard BIP39
- **Shamir 2-of-3** : 3 PARTS, 2 suffisent pour recuperer
- **Input flexible** : HEX ou 24 mots acceptes
- **Archivage long terme** : Format 24 mots pour gravure acier

---

## Workflow

```
1. Generer   ->  3 PARTS (HEX + 24 mots chacune)
                    |
2. Distribuer -> Part 1, 2, 3 dans 3 lieux separes
                    |
3. Recuperer -> 2 PARTS quelconques -> passphrase
```

---

## Exemple

**Input HEX** :
```
380e8fb7ad86fc83f440780e31fea61104585dd2a341e46477f8bcb4bda3b4e7
```

**Output 24 mots** :
```
day inner unknown force hurt draft speed audit athlete morning praise capital
easily confirm enhance habit tongue casual wreck just envelope spike squeeze toast
```

**Reconversion** : HEX identique (roundtrip parfait)
