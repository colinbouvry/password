# 🔒 Guide Production - Shamir Secret Sharing

## 📊 Deux versions disponibles

### 1. **Version Standard** (Recommandée pour usage personnel)
```
generate_24_passphrase.py
shamir_polynomial_2sur3.py
recovery_polynomial.py
```

**Caractéristiques :**
- ✅ Shamir polynomial correct
- ✅ Interpolation de Lagrange
- ✅ 2-sur-3 fonctionne parfaitement
- ✅ Entropie réelle
- ⚠️ Pas de détection d'erreurs
- ⚠️ Pas de checksums

**Quand l'utiliser :**
- Protéger votre passphrase personnelle
- Backup de clé privée
- Usage non-critique

---

### 2. **Version Robuste** (Production critique)
```
shamir_polynomial_robust.py
```

**Caractéristiques additionnelles :**
- ✅ Checksum pour chaque part
- ✅ Checksum global (3 parts ensemble)
- ✅ Détection de corruption
- ✅ Vérification du format (64 caractères hexa)
- ✅ Validation du secret retrouvé
- ✅ Métadonnées de sécurité
- ✅ Messages d'erreur détaillés

**Quand l'utiliser :**
- Systèmes critiques
- Production blockchain
- Trésorier d'entreprise
- Où la corruption est un risque réel

---

## 🔍 Comparaison détaillée

| Feature | Standard | Robuste |
|---------|----------|---------|
| **Shamir polynomial** | ✅ | ✅ |
| **2-sur-3** | ✅ | ✅ |
| **Checksum parts** | ❌ | ✅ |
| **Checksum global** | ❌ | ✅ |
| **Détecte corruption** | ❌ | ✅ |
| **Vérif format** | ❌ | ✅ |
| **Vérif secret** | ❌ | ✅ |
| **Métadonnées** | ❌ | ✅ |
| **Classe OOP** | ❌ | ✅ |
| **Messages erreur** | Basiques | Détaillés |

---

## 🧪 Exemple : Détection de corruption

### Version Standard
```
Part 1 : c90811c9eabd3... (OK)
Part 2 : 88132580eb13b... (OK)

→ Secret retrouvé : 09fcfe12ea66a... ✅
  (Mais si Part 1 était corrompue, on aurait un mauvais secret)
```

### Version Robuste
```
Part 1 : c90811c9eabd... (CORROMPU)

Vérification :
  ❌ ERREUR : Format hexa invalide

→ Refuse de continuer ✅
  (Impossible de retourner un secret invalide)
```

---

## 💻 Utilisation

### Standard
```bash
# Générer
python generate_24_passphrase.py

# Diviser
python shamir_polynomial_2sur3.py

# Récupérer
python recovery_polynomial.py
```

### Robuste
```python
from shamir_polynomial_robust import ShamirRobust

# Créer une instance
shamir = ShamirRobust()

# Diviser
parts, metadata = shamir.split_secret("votre passphrase 24 mots")

# Vérifier une part
valid, msg = shamir.verify_part(1, part1_hex)

# Récupérer avec vérifications
secret = shamir.recover_secret(1, part1_hex, 2, part2_hex)
```

---

## 🔐 Sécurité

### Version Standard
**Risques :**
- ❌ Une part corrompue n'est pas détectée
- ❌ Modification silencieuse possible
- ❌ Pas de trace de tampering

### Version Robuste
**Protections :**
- ✅ Checksum détecte toute modification
- ✅ Valide le format avant traitement
- ✅ Vérifie que le secret est correct
- ✅ Refuse les parts invalides
- ✅ Métadonnées pour audit

---

## 📋 Checklist Production

### Avant déploiement en production :

- [ ] Tester la division (split)
- [ ] Tester la récupération (recovery)
- [ ] Vérifier que 2 parts suffisent
- [ ] Vérifier que les 3 combinaisons marchent
- [ ] Tester avec données réelles
- [ ] Simuler une corruption (Version robuste)
- [ ] Vérifier les messages d'erreur
- [ ] Documenter les procédures
- [ ] Former les opérateurs
- [ ] Ranger les parts en sécurité

### Pour version robuste uniquement :

- [ ] Vérifier les checksums
- [ ] Tester la détection de corruption
- [ ] Archiver les métadonnées
- [ ] Monitorer les erreurs
- [ ] Mettre à jour les logs

---

## 🎯 Recommandations

**Pour usage personnel / non-critique :**
```bash
→ Utilisez : generate_24_passphrase.py + shamir_polynomial_2sur3.py
```

**Pour production / critique :**
```bash
→ Utilisez : shamir_polynomial_robust.py
```

**Pour apprendre :**
```bash
→ Testez : test_shamir_polynomial_complet.py
→ Explorez : demo_complete.py
```

---

## 🚀 Migration Standard → Robuste

Si vous avez déjà utilisé la version standard :

1. Installez la version robuste
2. Testez avec vos parts existantes
3. Vérifiez que la récupération marche
4. Archivez les métadonnées
5. Passez à la production robuste

---

## 📞 Support

**Erreurs courantes :**

| Erreur | Cause | Solution |
|--------|-------|----------|
| Format hexa invalide | Caractères incorrects | Vérifier le copier-coller |
| Mauvais format | Pas 64 caractères | Complète avec les 0 au début |
| Checksum ne correspond pas | Part corrompue | Récupérer depuis la source |
| Secret ne correspond pas | Mauvaises parts | Utiliser les bonnes combinaisons |

---

**Créé** : 2025-11-18
**Version** : 2.1 (Standard + Robuste)
**Statut** : ✅ Production-ready
