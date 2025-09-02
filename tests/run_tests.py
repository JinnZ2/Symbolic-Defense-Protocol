#!/usr/bin/env python3
# Symbolic-Defense-Protocol — test runner (v0.1)

import json, sys
from pathlib import Path

# Import functions from run_example.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from run_example import detect_tactics

ROOT = Path(__file__).resolve().parent
TEST_FILE = ROOT / "sample_tests.json"

def load_tests():
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    tests = load_tests()
    print(f"=== Running {len(tests)} sample tests ===\n")

    passed = 0
    for i, case in enumerate(tests, 1):
        text = case["input"]
        expect = case["expect"]

        matches = detect_tactics(text)
        detected = []
        for m in matches:
            tid = m["tactic"]["id"]
            if tid.startswith("dict."):
                detected.append(tid.split(".", 1)[1])
            else:
                detected.append(m["tactic"].get("id", m["tactic"].get("name", "unknown")))

        # normalize for benign cases
        if "benign" in expect and not detected:
            ok = True
        else:
            ok = all(e in detected for e in expect if e != "benign")

        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1

        print(f"Test {i}: {status}")
        print(f"  Input: {text}")
        print(f"  Expect: {expect}")
        print(f"  Detected: {detected}\n")

    print(f"=== {passed}/{len(tests)} tests passed ===")

if __name__ == "__main__":
    main()
