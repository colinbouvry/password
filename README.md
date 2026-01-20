# Shamir Secret Sharing 2-of-3 + BIP39

![Logo](logo.jpg)

A cryptographic system for permanent archival of a Master Password (24 words) using Shamir Secret Sharing. Designed for 50-500 year durability.

## How It Works

Your secret (24-word passphrase) is split into **3 parts** using Shamir's threshold scheme. Any **2 parts** can reconstruct the original secret, but a single part reveals **nothing**.

```
Secret ──► Split into 3 parts ──► Store in 3 locations
                                      │
Recovery: Retrieve any 2 parts ──► Reconstruct secret
```

## Features

- **Shamir 2-of-3**: Mathematical guarantee - 2 parts recover, 1 part reveals nothing
- **BIP39 Standard**: Industry-standard 24-word format (Bitcoin/Ethereum compatible)
- **Zero Dependencies**: Pure Python, works offline, no external libraries
- **Windows EXE**: Standalone executable for long-term compatibility

## Project Structure

```
password/
├── core/
│   ├── shamir_polynomial_robust.py   # Shamir 2-of-3 engine
│   ├── generate_secret.py            # Generate 24 words + 3 parts
│   ├── recover_secret.py             # Interactive recovery
│   ├── recover_secret_standalone.py  # Standalone version (no deps)
│   ├── convert_hex_to_24words.py     # HEX <-> 24 words conversion
│   └── mots.py                       # BIP39 wordlist (2048 words)
│
├── tests/
│   ├── test_unit.py                  # Unit tests
│   ├── test_integration.py           # Integration tests
│   └── test_hex_to_words.py          # Conversion tests (2002 tests)
│
├── dist/
│   └── Shamir_Recover.exe            # Windows executable
│
├── build_exe.bat                     # EXE compilation script
├── gravure_launcher.py               # Steel engraving templates
└── shamir_metadata.json              # Generated data (KEEP SECURE!)
```

## Quick Start

### 1. Generate a Secret

```bash
python core/generate_secret.py
```

Output:
- 24 BIP39 words (your passphrase)
- 3 Shamir parts (HEX and 24-word format)
- `shamir_metadata.json` file

### 2. Recover the Secret

```bash
python core/recover_secret.py
```

- Enter any 2 of 3 parts (HEX or 24 words)
- Recovers the original passphrase

### 3. Run Tests

```bash
python tests/test_hex_to_words.py
```

Expected: `2002/2002 tests PASSED`

## Security Model

```
Polynomial: f(x) = secret + a*x (mod PRIME)

Parts:
  Part 1 = f(1)
  Part 2 = f(2)
  Part 3 = f(3)

Recovery:
  2 points ──► Lagrange interpolation ──► f(0) = secret
  1 point alone = ZERO information (mathematically proven)
```

**Field**: secp256k1 (PRIME = 2^256 - 2^32 - 977)

## Recommended Storage

Distribute the 3 parts across separate physical locations:

```
SAFE A (Home):
  ├── Laminated paper (24 words)
  ├── USB drive (code + EXE)
  └── Part 1 in sealed envelope

SAFE B (Bank):
  ├── Steel plate engraving (24 words)
  ├── Backup USB drive
  └── Part 2 in sealed envelope

SAFE C (Relative/Friend):
  └── Part 3 in sealed envelope
```

**Why this works:**
- Lose 1 safe? No problem (2 remaining parts recover secret)
- Attacker gets 1 part? Useless (reveals nothing mathematically)
- House fire? Bank safe and relative's copy survive

## Steel Engraving

For multi-century durability, engrave on stainless steel:

```bash
python gravure_launcher.py
```

Options:
1. **Simple engraving** (HEX) - 30-60 EUR
2. **Manual engraving** (Words + Parts) - 10-50 EUR (recommended)
3. **Professional laser** - 150-300 EUR

## Building Windows EXE

```bash
build_exe.bat
```

See [BUILD_EXE_GUIDE.md](BUILD_EXE_GUIDE.md) for details.

## Test Results

| Suite | Tests | Status |
|-------|-------|--------|
| Unit tests | 10 | PASS |
| Integration | 8 | PASS |
| HEX <-> Words | 2002 | PASS |

## Recovery Scenarios

```
NORMAL CASE:
  Open Safe A ──► Read paper ──► Enter in Bitwarden ──► 2 min

DISASTER CASE:
  Part 1 + Part 2 ──► recover_secret.py ──► 24 words ──► 30 min

EXTREME CASE:
  Open shamir_metadata.json in Notepad ──► 24 words in plaintext ──► 5 min
```

## Critical Files

| File | Priority | Lifespan |
|------|----------|----------|
| 24 words (paper) | CRITICAL | 100+ years |
| shamir_metadata.json | CRITICAL | 100 years |
| Parts 1, 2, 3 | Important | Indefinite |
| Shamir_Recover.exe | Useful | 50 years |

## Troubleshooting

**"ModuleNotFoundError"**
```bash
cd e:\dev\password
python core/generate_secret.py
```

**"Invalid hex format"**
- Verify exactly 64 hexadecimal characters
- No spaces before/after

**"Checksum mismatch"**
- Part was corrupted or modified
- Retrieve from original source

## Technical Specifications

- **Algorithm**: Shamir Secret Sharing (2-of-3 threshold)
- **Entropy**: 256 bits
- **Checksum**: SHA256 (8 bits for BIP39)
- **Wordlist**: 2048 BIP39 English words
- **Encoding**: UTF-8

---

Version: 3.0 FINAL
Status: Production-ready
Created: 2025-11-19
