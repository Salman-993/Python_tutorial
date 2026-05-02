import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

# ===== YAHAN APNA SAHI GITHUB LINK DAALO =====
GITHUB_REPO_LINK = "Salman-993"
# ========================================

REPO_PATH = os.path.dirname(os.path.abspath(__file__))

class AutoGitHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"🔄 Change detected: {os.path.basename(event.src_path)}")
            subprocess.run(["git", "add", "."], cwd=REPO_PATH)
            subprocess.run(["git", "commit", "-m", "Auto push"], cwd=REPO_PATH)
            subprocess.run(["git", "push"], cwd=REPO_PATH)
            print("✅ Pushed to GitHub\n")

# ===== FIX: Purana remote hatao aur naya daalo =====
if not os.path.exists(os.path.join(REPO_PATH, ".git")):
    print("🔧 First time setup - Initializing git...")
    subprocess.run(["git", "init"], cwd=REPO_PATH)
else:
    # Git already exists, remove old remote if any
    print("🔧 Cleaning old remote configuration...")
    subprocess.run(["git", "remote", "remove", "origin"], cwd=REPO_PATH, capture_output=True)
    
# Add new remote
subprocess.run(["git", "remote", "add", "origin", GITHUB_REPO_LINK], cwd=REPO_PATH)
subprocess.run(["git", "branch", "-M", "main"], cwd=REPO_PATH)
print("✅ Git configured with new repo link")

# ===== FIX: Purani commits hatao aur fresh push karo =====
print("📤 Cleaning cache and pushing all files to GitHub...")
subprocess.run(["git", "add", "."], cwd=REPO_PATH)
subprocess.run(["git", "commit", "-m", "Initial commit - all files"], cwd=REPO_PATH)

# Force push to overwrite old commits
result = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=REPO_PATH, capture_output=True, text=True)

if result.returncode == 0:
    print("✅ Initial push complete! (Old cache cleared)")
else:
    print(f"⚠️ Push failed: {result.stderr}")
    print("\n📌 Manually run these commands:")
    print(f"  cd {REPO_PATH}")
    print("  git remote remove origin")
    print(f"  git remote add origin {GITHUB_REPO_LINK}")
    print("  git push -u origin main --force")

print("\n" + "="*50)

# Ab watch karo
observer = Observer()
observer.schedule(AutoGitHandler(), REPO_PATH, recursive=True)
observer.start()
print(f"🚀 Watching: {REPO_PATH}")
print("📁 Ab jo bhi file banayoge ya change karoge, auto push hoga!\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()