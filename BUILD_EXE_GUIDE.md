# Guide de Compilation : Python vers EXE

## Pourquoi creer un EXE ?

```
PROBLEME EN 2045:
  - Python n'existe peut-etre plus
  - Installer Python sera impossible
  - Les dependances auront disparu

SOLUTION:
  - EXE = Executable standalone
  - Un simple double-clic
  - Zero installation
  - Fonctionne meme si Python disparait
```

---

## Etape 1 : Prerequis

### Avoir Python installe

```bash
python --version
# Output: Python 3.11.x ou superieur
```

Pas Python ? Telecharger sur https://www.python.org/downloads/

### PyInstaller

```bash
pip install pyinstaller
```

---

## Etape 2 : Compilation

### Option A : Script automatique (Recommande)

```bash
cd e:\dev\password
build_exe.bat
```

Le script va :
1. Installer PyInstaller
2. Compiler `recover_secret_standalone.py`
3. Creer `dist/Shamir_Recover.exe`

### Option B : Ligne de commande manuelle

```bash
cd e:\dev\password

pyinstaller --onefile --name "Shamir_Recover" core/recover_secret_standalone.py
```

---

## Etape 3 : Resultat

L'EXE cree se trouve dans :
```
e:\dev\password\dist\Shamir_Recover.exe
```

Taille : ~10-30 MB

---

## Etape 4 : Test

```bash
# Double-clic sur Shamir_Recover.exe
# Interface console interactive
# Entrer les PARTS Shamir
# Recuperer les 24 mots
```

---

## Etape 5 : Sauvegarde pour 20 ans

### Ou stocker l'EXE ?

```
COFFRE MAISON:
  - Cle USB (EXE + recover_secret_standalone.py + code source)
  - DVD-R grave (backup)
  - Papier imprime (code source en PDF)

COFFRE BANQUE:
  - DVD-R grave (backup EXE)
  - Papier + gravure acier (les 24 mots bruts)
```

### Instructions pour les heritiers

```
FICHIER: INSTRUCTIONS_HERITIERS.txt

Si vous lisez ceci apres mon deces ou en cas d'urgence:

1. Les 24 mots Bitwarden sont stockes:
   - Papier plastifie (Coffre A et B)
   - Gravure acier (Coffre B)
   - Fichier "shamir_metadata.json" (cle USB)

2. Pour retrouver les 24 mots SANS code:
   - Ouvrir shamir_metadata.json avec Notepad
   - Chercher "passphrase"
   - Les 24 mots y sont directement

3. Pour retrouver les 24 mots AVEC code (backup):
   - Double-clic sur Shamir_Recover.exe
   - Entrer PART 1 et PART 2 (enveloppes scellees)
   - Les 24 mots s'affichent

4. Une fois les mots recuperes:
   - Bitwarden: "Forgot Password?"
   - Entrer les 24 mots
   - Reconnexion reussie
```

---

## Verifications Avant Archivage

```bash
# 1. Tester l'EXE sur un autre ordinateur
cp dist/Shamir_Recover.exe /chemin/test
# Double-clic -> doit marcher

# 2. Verifier que shamir_metadata.json est lisible
notepad shamir_metadata.json
# Doit afficher les 24 mots en clair

# 3. Tester la recuperation manuelle
python core/recover_secret_standalone.py
# Entrer les PARTS
# Doit afficher les 24 mots
```

---

## Troubleshooting

### "PyInstaller not found"
```bash
pip install pyinstaller
# Puis relancer build_exe.bat
```

### "Python not found"
```bash
# Ajouter Python au PATH Windows
# Ou utiliser le chemin complet
C:\Python312\python.exe build_exe.bat
```

### "EXE ne se lance pas"
```bash
# Verifier Windows Defender/Antivirus
# Le nouvel EXE peut etre suspecte
# Whitelist le fichier ou desactiver temporairement
```

### "UnicodeEncodeError"
```bash
# Le script standalone gere ca automatiquement
# Si probleme: editer recover_secret_standalone.py
# Assurer que UTF-8 est configure
```

---

## Optimisations (Optionnel)

### Reduire la taille

```bash
# Utiliser Nuitka (plus optimise)
pip install nuitka
nuitka --onefile core/recover_secret_standalone.py

# Resultat: 3-5 MB au lieu de 10-30 MB
```

### Ajouter une icone personnalisee

```bash
pyinstaller --onefile --icon=icon.ico core/recover_secret_standalone.py
```

---

## Archivage Long-terme (20+ ans)

### Strategie Recommandee

```
ANNEE 2025: Creation
  - Creer l'EXE
  - Tester
  - Graver sur DVD-R (duree 50-100 ans)
  - Stocker cle USB + DVD en 2 coffres

ANNEE 2035: Verification
  - Tester que l'EXE marche
  - Repliquer si degradation DVD
  - Mettre a jour si Python change drastiquement

ANNEE 2045+: Utilisation
  - Si besoin: double-clic sur l'EXE
  - Si EXE ne marche plus: utiliser le JSON brut
  - Si tout echoue: lire le papier en Coffre A
```

---

## Pire Scenario

```
Situation en 2050:
  - Windows n'existe plus
  - EXE ne marche plus
  - recover_secret.py ne marche plus
  - Python est obsolete

Solution simple:
  - Ouvrir shamir_metadata.json avec n'importe quel editeur
  - Les 24 mots y sont EN CLAIR
  - Copier-coller dans Bitwarden
  - Fini!
```

Le JSON brut est l'ultime fallback.

---

## Fichiers Importants

| Fichier | Priorite | Duree | Ou |
|---------|----------|-------|-----|
| **24 mots (papier)** | CRITIQUE | infini | Coffre A + B |
| **shamir_metadata.json** | CRITIQUE | 100 ans | Cle USB + Coffre A |
| **Shamir_Recover.exe** | Important | 50 ans | Cle USB + DVD |
| **recover_secret_standalone.py** | Important | infini | Cle USB + Papier |
| **Code source Python (.py)** | Backup | infini | Cle USB + Papier |

---

## Compatibilite

- Python 3.7+
- Windows 7, 10, 11
- Zero dependances externes
- Zero internet requis

---

Cree le: 2025-11-19
Version: 1.0
