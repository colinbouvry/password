# Quick Start Guide

## Commandes Rapides

### 1. Exécuter TOUS les tests (10 + 8 + 100 = 118 tests)
```bash
python tests/test_all.py
```
**Résultat attendu:**
```
Unit Tests          : PASS
Integration Tests   : PASS
Exhaustive Tests    : PASS (100 cycles)

All tests passed!
```

### 2. Exécuter tests exhaustifs uniquement (100 cycles)
```bash
python tests/test_exhaustive_100cycles.py
```
**Résultat attendu:**
```
100/100 CYCLES RÉUSSIS
✅ 24 mots correspondent
✅ Hash SHA256 correspond
✅ Toutes les combinaisons fonctionnent
```

### 3. Générer un secret (24 mots + 3 parts)
```bash
python core/generate_secret.py
```
**Workflow:**
1. Choisir: Générer 24 mots aléatoires (option 1) ou utiliser une passphrase (option 2)
2. Recevoir: 3 parts Shamir robustes
3. Voir: Tous les checksums SHA256

### 4. Récupérer le secret (avec 2 parts)
```bash
python core/recover_secret.py
```
**Workflow:**
1. Entrer: Part 1 ou 2 ou 3 (64 caractères hexa)
2. Entrer: Une autre part
3. Recevoir: Hash SHA256 du secret retrouvé

---

## Structure Minimale

```
IMPORTANT: Exécuter à partir du dossier racine (e:\dev\password\)

Pas bon:
  cd tests
  python test_unit.py        ❌ Erreur d'import

Correct:
  cd e:\dev\password
  python tests/test_unit.py  ✅ Fonctionne
```

---

## Tests Disponibles

### Suite Complète (test_all.py)
- **10** tests unitaires
- **8** tests d'intégration
- **100** cycles exhaustifs
- **Temps**: ~2-3 minutes

### Tests Unitaires Seuls (test_unit.py)
- Teste chaque fonction individuellement
- **10** tests
- **Temps**: ~5-10 secondes

### Tests d'Intégration Seuls (test_integration.py)
- Teste le flux complet: génération → division → récupération
- **8** tests
- **Temps**: ~5-10 secondes

### Tests Exhaustifs (test_exhaustive_100cycles.py)
- **100** cycles complets avec validation
- Teste les **6 fonctions** principales
- Valide les **24 mots** et **hash SHA256**
- Teste les **3 combinaisons** de parts (1+2, 1+3, 2+3)
- **Temps**: ~1-2 minutes

---

## Qu'est-ce que ça teste?

### Tests Unitaires (10 tests)
1. Initialisation de la classe
2. Génération d'un secret
3. Division en 3 parts
4. Validation d'une part valide
5. Rejet d'une part invalide (format)
6. Détection de corruption (checksum)
7. Récupération avec Part 1+2
8. Récupération avec Part 1+3
9. Récupération avec Part 2+3
10. Rejet d'une part corrompue

### Tests d'Intégration (8 tests)
1. Flux complet (génération + division)
2. Récupération Part 1+2
3. Récupération Part 1+3
4. Récupération Part 2+3
5. Cohérence des secrets
6. Détection corruption
7. Validation métadonnées
8. Checksums uniques

### Tests Exhaustifs (100 cycles)

**Par cycle (6 étapes):**
```
1. __init__()
   └─ Initialise nouvel objet Shamir

2. Génération 24 mots aléatoires
   └─ Sélectionne 24 mots de la liste

3. generate_secret(passphrase)
   └─ Crée secret SHA256 avec checksum

4. split_secret(passphrase)
   └─ Divise en 3 parts Shamir robustes

5. verify_part() x3
   └─ Valide chaque part (format + intégrité)

6. recover_secret() x3 combinaisons
   └─ Récupère avec 1+2, 1+3, 2+3
   └─ Utilise _lagrange_interpolation()
   └─ Valide 24 mots et hash SHA256

Result: ✅ Tous les 24 mots correspondent
```

**Total par cycle:**
- 6 fonctions testées
- 3 combinaisons validées
- 24 mots vérifiés
- 1 hash SHA256 validé

**Sur 100 cycles:**
- 600 appels de fonctions
- 300 combinaisons
- 2400 mots validés
- 100 hash SHA256 vérifiés

---

## Fichiers Clés

### Implementation
- **core/shamir_polynomial_robust.py** - Classe principale (9.3K)
  - Shamir Polynomial Division
  - Lagrange Interpolation
  - Checksums & Validation

- **core/generate_secret.py** - Génération interface (3.1K)
  - Génère 24 mots aléatoires
  - Divise en 3 parts
  - Affiche checksums

- **core/recover_secret.py** - Récupération interface (2.1K)
  - Récupère avec 2 parts
  - Valide intégrité
  - Retourne hash SHA256

### Tests
- **tests/test_unit.py** - 10 tests unitaires
- **tests/test_integration.py** - 8 tests d'intégration
- **tests/test_exhaustive_100cycles.py** - 100 cycles exhaustifs (NOUVEAU)
- **tests/test_all.py** - Lance tous les tests

### Documentation
- **README.md** - Guide principal
- **PRODUCTION_GUIDE.md** - Guide déploiement
- **PROJECT_STATUS.md** - Status final du projet
- **EXHAUSTIVE_TEST_README.md** - Documentation tests exhaustifs
- **QUICK_START.md** - Ce fichier

---

## Résultats Attendus

### ✅ Tests Réussis
```
Unit Tests          : PASS (10/10)
Integration Tests   : PASS (8/8)
Exhaustive Tests    : PASS (100/100)

All tests passed!
```

### ❌ Tests Échoués
Si un test échoue, vérifier:
1. Python 3.6+ installé
2. Exécution à partir du dossier racine
3. Tous les fichiers présents (core/ + tests/)
4. Pas de modification du code

---

## Performance

### Temps d'exécution
- **Unit tests**: ~5-10 secondes
- **Integration tests**: ~5-10 secondes
- **Exhaustive tests (100 cycles)**: ~60-120 secondes
- **Total (all tests)**: ~1.5-2.5 minutes

### Ressources
- **RAM**: <50 MB
- **CPU**: Minimal
- **Disque**: <5 MB

---

## Cas d'Usage Réels

### Générer une sauvegarde sécurisée
```
1. python core/generate_secret.py
2. Copier les 24 mots sur papier physique
3. Copier les 3 parts dans 3 endroits différents
4. Conserver les checksums pour audit
```

### Récupérer votre secret
```
1. Récupérer 2 parts (sur les 3)
2. python core/recover_secret.py
3. Entrer les 2 parts
4. Vérifier que le hash correspond
```

### Vérifier le système
```
1. python tests/test_all.py
2. Si tous les tests passent: système OK ✅
3. Prêt pour production ✅
```

---

## Conseils Sécurité

### À faire
- ✅ Tester d'abord (python tests/test_all.py)
- ✅ Utiliser les 24 mots pour la génération
- ✅ Ranger les 3 parts dans 3 endroits différents
- ✅ Archiver les checksums
- ✅ Tester la récupération avant de supprimer l'original

### À éviter
- ❌ Ne pas partager les parts
- ❌ Ne pas stocker au même endroit
- ❌ Ne pas modifier les parts
- ❌ Ne pas oublier les checksums
- ❌ Ne pas tester en production sans vérification préalable

---

## Support

### Questions fréquentes

**Q: Combien de temps pour 100 cycles?**
A: ~1-2 minutes (60-120 secondes)

**Q: Tous les tests doivent passer?**
A: Oui, 118/118 tests doivent passer (100%)

**Q: Je dois modifier le code?**
A: Non, utiliser le code fourni tel quel

**Q: D'où viennent les 24 mots?**
A: De la liste dans core/generate_secret.py

**Q: Les parts sont garanties uniques?**
A: Oui, grâce aux checksums SHA256 uniques

---

## Résumé

```
✅ 118 tests
✅ 100 cycles exhaustifs
✅ 24 mots validés 2400 fois
✅ Hash SHA256 validé 100 fois
✅ Combinaisons 300/300 testées
✅ Système production-ready

STATUS: PRODUCTION READY ✅
```

---

**Voir aussi:** README.md, PRODUCTION_GUIDE.md, PROJECT_STATUS.md
