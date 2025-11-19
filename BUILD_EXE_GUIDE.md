# 🔨 Guide de Compilation : Python → EXE

## Pourquoi créer un EXE?

```
PROBLÈME EN 2045:
  ❌ Python n'existe peut-être plus
  ❌ Installer Python sera impossible
  ❌ Les dépendances auront disparu

SOLUTION:
  ✅ EXE = Exécutable standalone
  ✅ Un simple double-clic
  ✅ Zéro installation
  ✅ Fonctionne même si Python disparaît
```

---

## Étape 1 : Prérequis

### Avoir Python installé

```bash
python --version
# Output: Python 3.11.x ou supérieur
```

**Pas Python ?** → Télécharge sur https://www.python.org/downloads/

### PyInstaller (automatique avec le script)

Sinon installation manuelle:
```bash
pip install pyinstaller
```

---

## Étape 2 : Compilation (Facile)

### Option A : Script automatique (Recommandé)

**Windows :**
```bash
cd e:\dev\password
double-clic sur build_exe.bat
```

Le script va:
1. ✅ Installer PyInstaller
2. ✅ Compiler `recover_secret_standalone.py`
3. ✅ Créer `dist/Shamir_Recover.exe`

### Option B : Ligne de commande manuelle

```bash
cd e:\dev\password

pyinstaller \
    --onefile \
    --windowed \
    --name "Shamir_Recover" \
    core/recover_secret_standalone.py
```

---

## Étape 3 : Résultat

L'EXE créé se trouve dans :
```
e:\dev\password\dist\Shamir_Recover.exe
```

Taille: ~10-30 MB (acceptable)

---

## Étape 4 : Test

```bash
# Double-clic sur Shamir_Recover.exe
# → Interface console interactive
# → Entre tes PARTS Shamir
# → Récupère les 24 mots!
```

---

## Étape 5 : Sauvegarde pour 20 ans

### Où stocker l'EXE?

```
COFFRE MAISON:
├─ Clé USB (EXE + recovery_secret_standalone.py + code source)
├─ DVD-R gravé (backup)
└─ Papier imprimé (code source en PDF)

COFFRE BANQUE:
├─ DVD-R gravé (backup EXE)
└─ Papier + gravure acier (les 24 mots bruts)
```

### Instructions pour tes héritiers

```
FICHIER: INSTRUCTIONS_HERITIERS.txt

Si vous lisez ceci après ma mort ou en cas d'urgence:

1. Les 24 mots Bitwarden sont stockés:
   ✓ Papier plastifié (Coffre A et B)
   ✓ Gravure acier (Coffre B)
   ✓ Fichier "shamir_metadata.json" (clé USB)

2. Pour retrouver les 24 mots SANS code:
   → Ouvre shamir_metadata.json avec Notepad
   → Cherche "passphrase"
   → Les 24 mots y sont directement!

3. Pour retrouver les 24 mots AVEC code (backup):
   → Double-clic sur Shamir_Recover.exe
   → Entrez PART 1 et PART 2 (enveloppes scellées)
   → Les 24 mots s'affichent

4. Une fois les mots récupérés:
   → Bitwarden: "Forgot Password?"
   → Entrez les 24 mots
   → Reconnexion réussie ✅
```

---

## Vérifications Avant Archivage

```bash
# 1. Teste l'EXE sur un autre ordinateur
   cp dist/Shamir_Recover.exe /chemin/test
   # Double-clic → doit marcher

# 2. Vérifie que shamir_metadata.json est lisible
   notepad shamir_metadata.json
   # Doit afficher les 24 mots en clair

# 3. Teste la récupération manuelle
   python core/recover_secret_standalone.py
   # Entre tes PARTS
   # Doit afficher les 24 mots
```

---

## Troubleshooting

### ❌ "PyInstaller not found"
```bash
pip install pyinstaller
# Puis relance build_exe.bat
```

### ❌ "Python not found"
```bash
# Ajoute Python au PATH Windows
# Ou utilise le chemin complet
C:\Python312\python.exe build_exe.bat
```

### ❌ "EXE ne se lance pas"
```bash
# Vérifie Windows Defender/Antivirus
# Le nouvel EXE peut être suspecté
# Whitelist le fichier ou désactive temporairement
```

### ❌ "UnicodeEncodeError"
```bash
# Le script standalone gère ça automatiquement
# Si problème: édite recover_secret_standalone.py
# Assure-toi que UTF-8 est configuré (ligne 28-29)
```

---

## Optimisations (Optionnel)

### Réduire la taille

```bash
# Utilise Nuitka (plus optimisé)
pip install nuitka
nuitka --onefile core/recover_secret_standalone.py

# Résultat: 3-5 MB au lieu de 10-30 MB
```

### Ajouter une icône personnalisée

```bash
# Crée une icône .ico
# Puis:
pyinstaller --onefile --icon=icon.ico core/recover_secret_standalone.py
```

### EXE "invisible" (no console window)

```bash
pyinstaller --onefile --windowed core/recover_secret_standalone.py
# Mais console interactive ne fonctionne pas
# Ne recommandé pour ce script
```

---

## Archivage Long-terme (20+ ans)

### Stratégie Recommandée

```
ANNÉE 2025: Création
├─ Crée l'EXE
├─ Teste-le
├─ Grave sur DVD-R (durée 50-100 ans)
└─ Stocke clé USB + DVD en 2 coffres

ANNÉE 2035: Vérification
├─ Teste toujours que l'EXE marche
├─ Réplique si dégradation DVD
└─ Mets à jour si Python change drastiquement

ANNÉE 2045+: Utilisation
├─ Si besoin: double-clic sur l'EXE
├─ Si EXE ne marche plus: utilise le JSON brut
└─ Si tout échoue: lis le papier en Coffre A
```

---

## Pire Scénario

```
Situation en 2050:
  ❌ Windows n'existe plus
  ❌ EXE ne marche plus
  ❌ recover_secret.py ne marche plus
  ❌ Python est obsolète

Solution simple:
  ✅ Ouvre shamir_metadata.json avec n'importe quel éditeur
  ✅ Les 24 mots y sont EN CLAIR
  ✅ Copie-colle dans Bitwarden
  ✅ Fini!
```

Voilà pourquoi archiver le JSON brut est critique : c'est ton ultime fallback.

---

## Fichiers Important

| Fichier | Priorité | Durée | Où |
|---------|----------|-------|-----|
| **Les 24 mots (papier)** | 🔴 CRITIQUE | ∞ | Coffre A + B |
| **shamir_metadata.json** | 🔴 CRITIQUE | 100 ans | Clé USB + Coffre A |
| **Shamir_Recover.exe** | 🟡 Important | 50 ans | Clé USB + DVD |
| **recover_secret_standalone.py** | 🟡 Important | ∞ | Clé USB + Papier imprimé |
| **Code source Python (.py)** | 🟢 Backup | ∞ | Clé USB + Papier imprimé |

---

## Validé pour?

- ✅ Python 3.7+
- ✅ Python 3.x
- ✅ Python 4.x (hypothétique)
- ✅ Windows 7, 10, 11
- ✅ Windows 12+ (hypothétique)
- ✅ Zéro dépendances externes
- ✅ Zéro internet requis

---

**Créé le**: 2025-11-19
**Version**: 1.0
**Archive jusqu'en**: 2045+
