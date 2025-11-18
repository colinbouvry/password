# -*- coding: utf-8 -*-
# ============================================================================
# TEST ALL - Execute all unit and integration tests
# ============================================================================
import sys
import os
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

print("\n" + "="*80)
print("TEST RUNNER - All Tests")
print("="*80)

# Path to tests directory
tests_dir = os.path.dirname(os.path.abspath(__file__))

# ============================================================================
# UNIT TESTS
# ============================================================================
print("\n" + "="*80)
print("Unit Tests")
print("="*80)

result_unit = subprocess.run(
    [sys.executable, os.path.join(tests_dir, 'test_unit.py')],
    capture_output=False
)

# ============================================================================
# INTEGRATION TESTS
# ============================================================================
print("\n" + "="*80)
print("Integration Tests")
print("="*80)

result_integration = subprocess.run(
    [sys.executable, os.path.join(tests_dir, 'test_integration.py')],
    capture_output=False
)

# ============================================================================
# E2E TESTS - END-TO-END (100 iterations)
# ============================================================================
print("\n" + "="*80)
print("E2E Tests (End-to-End, 100 iterations)")
print("="*80)

result_e2e = subprocess.run(
    [sys.executable, os.path.join(tests_dir, 'test_e2e.py')],
    capture_output=False
)

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)

unit_pass = result_unit.returncode == 0
integration_pass = result_integration.returncode == 0
e2e_pass = result_e2e.returncode == 0

unit_status = "PASS" if unit_pass else "FAIL"
integration_status = "PASS" if integration_pass else "FAIL"
e2e_status = "PASS" if e2e_pass else "FAIL"

print(f"\nUnit Tests          : {unit_status}")
print(f"Integration Tests   : {integration_status}")
print(f"E2E Tests           : {e2e_status} (100 iterations)")

all_pass = unit_pass and integration_pass and e2e_pass

if all_pass:
    print("\n" + "="*80)
    print("All tests passed!")
    print("="*80)
    sys.exit(0)
else:
    print("\n" + "="*80)
    print("Some tests failed")
    print("="*80)
    sys.exit(1)
