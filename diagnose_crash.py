import sys

print("1. Starting import checks...", flush=True)

try:
    print("   Importing os, sys, json...", flush=True)
    import os, json
    print("   [OK] Standard libs", flush=True)
except Exception as e:
    print(f"   [FAIL] Standard libs: {e}", flush=True)

try:
    print("   Importing pydantic...", flush=True)
    from pydantic import BaseModel
    print("   [OK] pydantic", flush=True)
except Exception as e:
    print(f"   [FAIL] pydantic: {e}", flush=True)

try:
    print("   Importing fastapi...", flush=True)
    import fastapi
    print("   [OK] fastapi", flush=True)
except Exception as e:
    print(f"   [FAIL] fastapi: {e}", flush=True)

try:
    print("   Importing google.genai...", flush=True)
    import google.genai
    print("   [OK] google.genai", flush=True)
except Exception as e:
    print(f"   [FAIL] google.genai: {e}", flush=True)

try:
    print("   Importing lancedb...", flush=True)
    import lancedb
    print("   [OK] lancedb", flush=True)
except Exception as e:
    print(f"   [FAIL] lancedb: {e}", flush=True)

print("2. All imports attempted.", flush=True)
