import sys
import subprocess
from pathlib import Path

def run_tests():
    root = Path(__file__).parent.resolve()
    python_exe = sys.executable

    projects = [
        ("01 - Pharma Commercial Intelligence", root / "01-pharma-commercial-intelligence" / "backend"),
        ("02 - Regulatory Intelligence Copilot", root / "02-regulatory-intelligence-copilot" / "backend"),
        ("03 - Clinical Trial Intelligence", root / "03-clinical-trial-intelligence" / "backend"),
        ("04 - AI Pharmacovigilance Platform", root / "04-pharmacovigilance-ai" / "backend")
    ]

    print("=" * 80)
    print(" HLS AI SOLUTIONS PORTFOLIO — AUTOMATED TEST VERIFICATION RUNNER")
    print("=" * 80)

    total_passed = 0
    total_failed = 0
    results = []

    for name, path in projects:
        print(f"\n--> Executing tests for: {name}")
        cmd = [python_exe, "-m", "pytest", "-q"]
        res = subprocess.run(cmd, cwd=str(path), capture_output=True, text=True)
        
        output = res.stdout.strip() + " " + res.stderr.strip()
        is_success = (res.returncode == 0)
        
        # Count passes
        passed = 0
        if "passed" in output:
            for part in output.split():
                if part.isdigit() and "passed" in output[output.find(part):output.find(part)+20]:
                    passed = int(part)
                    break
            if passed == 0 and is_success:
                # Estimate from dots if needed
                passed = output.count(".")
        
        if is_success:
            total_passed += passed
            status_str = f"PASSED ({passed} tests)"
        else:
            total_failed += 1
            status_str = "FAILED"
            
        results.append((name, status_str, is_success))
        print(f"    Status: {status_str}")

    print("\n" + "=" * 80)
    print(" PORTFOLIO TEST SCORECARD")
    print("=" * 80)
    for name, status_str, is_success in results:
        symbol = "[OK]" if is_success else "[FAIL]"
        print(f" {symbol:6} | {name:<42} | {status_str}")
    print("-" * 80)
    print(f" Summary: {total_passed} tests passed across {len(projects)} applications. Total failures: {total_failed}.")
    print("=" * 80)

    return 0 if total_failed == 0 else 1

if __name__ == "__main__":
    sys.exit(run_tests())
