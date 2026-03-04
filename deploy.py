import os
import shutil
import subprocess
import time
from pathlib import Path

def run_cmd(cmd, cwd=None):
    print(f"\n> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    return result

def main():
    base_dir = Path(r"C:\Users\kisho\Documents\Fun")
    
    print("=== STEP 1: Copying Screenshots ===")
    media_dir = Path(r"C:\Users\kisho\.gemini\antigravity\brain\9d2a27d4-00cb-4e02-872e-00cc3f4d8726\.tempmediaStorage")
    screenshots_dir = base_dir / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    
    src1 = media_dir / "media_9d2a27d4-00cb-4e02-872e-00cc3f4d8726_1772608351932.png"
    src2 = media_dir / "media_9d2a27d4-00cb-4e02-872e-00cc3f4d8726_1772608518044.png"
    
    if src1.exists():
        shutil.copy2(src1, screenshots_dir / "terminal_output.png")
        print("✓ Copied terminal_output.png")
    else:
        print(f"X Source screenshot not found: {src1}")
        
    if src2.exists():
        shutil.copy2(src2, screenshots_dir / "summary_cards.png")
        print("✓ Copied summary_cards.png")
    else:
        print(f"X Source screenshot not found: {src2}")

    print("\n=== STEP 2: Removing Unwanted Files ===")
    unwanted = ["run.bat", "run_capture.py", "task.txt", "setup.py", "deploy.ps1"]
    for f in unwanted:
        file_path = base_dir / f
        if file_path.exists():
            file_path.unlink()
            print(f"✓ Removed {f}")

    print("\n=== STEP 3: Initializing Git ===")
    run_cmd(["git", "init"], cwd=base_dir)
    run_cmd(["git", "config", "user.email", "team@mavericKX.dev"], cwd=base_dir)
    run_cmd(["git", "config", "user.name", "TeamMavericKX"], cwd=base_dir)
    
    print("\n=== STEP 4: Setting up Remote ===")
    run_cmd(["git", "remote", "remove", "origin"], cwd=base_dir)
    run_cmd(["git", "remote", "add", "origin", "https://github.com/TeamMavericKX/Mastery-Decision-Engine.git"], cwd=base_dir)

    print("\n=== STEP 5: Committing Files ===")
    run_cmd(["git", "add", "."], cwd=base_dir)
    commit_msg = (
        "feat: Mastery Decision Engine v1.0 — GATEKEEPER complete\n\n"
        "- MasteryEvaluator: 70/30 weighted score, 3-attempt circuit breaker\n"
        "- Threshold: MASTERY_GATE = 85 (permanent invariant)\n"
        "- 3 simulation archetypes: Sudden Drop, Steady Climb, Stagnant\n"
        "- Dockerized: python:3.11-slim, zero external dependencies\n"
        "- README with ASCII art, screenshots, architecture diagram"
    )
    run_cmd(["git", "commit", "-m", commit_msg], cwd=base_dir)

    print("\n=== STEP 6: Pushing to GitHub ===")
    run_cmd(["git", "branch", "-M", "main"], cwd=base_dir)
    print("Pushing to GitHub (this may take a few seconds)...")
    res = run_cmd(["git", "push", "-u", "origin", "main", "--force"], cwd=base_dir)
    
    if res.returncode == 0:
        print("\n=== SUCCESS: Deployment Complete! ===")
        print("Check your repo at: https://github.com/TeamMavericKX/Mastery-Decision-Engine")
    else:
        print("\n=== ERROR: Git Push Failed ===")
        print("You may need to authenticate with GitHub in the terminal first.")
        
    # Finally, remove this script itself to leave the repo perfectly clean
    print("\nCleaning up deploy script...")
    try:
        Path(__file__).unlink()
    except:
        pass

if __name__ == "__main__":
    main()
