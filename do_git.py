import subprocess
import os

with open("git_log.txt", "w") as log:
    def run(cmd):
        log.write(f"> {cmd}\n")
        try:
            # We use timeout to avoid hanging indefinitely if git asks for credentials
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=45)
            log.write("STDOUT:\n" + (res.stdout or "") + "\n")
            log.write("STDERR:\n" + (res.stderr or "") + "\n")
            log.write(f"Return code: {res.returncode}\n\n")
        except subprocess.TimeoutExpired:
            log.write("TIMEOUT EXPIRED (Command hung, possibly waiting for credentials)\n\n")
        except Exception as e:
            log.write("ERROR: " + str(e) + "\n\n")

    run("git init")
    run("git config user.email team@mavericKX.dev")
    run("git config user.name TeamMavericKX")
    
    # We remove origin just in case it already exists
    run("git remote remove origin")
    run("git remote add origin https://github.com/TeamMavericKX/Mastery-Decision-Engine.git")
    
    run("git add .")
    run("git commit -m \"feat: Mastery Decision Engine v1.0 — GATEKEEPER complete\"")
    run("git branch -M main")
    
    # Push to GitHub
    run("set GIT_TERMINAL_PROMPT=0 & git push -u origin main --force")
