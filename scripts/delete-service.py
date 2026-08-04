import shutil
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

APPLICATIONS = ROOT / "applications"
GITOPS = ROOT / "shared" / "gitops"

print("=" * 60)
print("Platform Engineering - Delete Service")
print("=" * 60)

service = input("Service Name: ").strip().lower()

service_dir = APPLICATIONS / service
argocd_file = GITOPS / f"{service}-application.yaml"

if not service_dir.exists():
    print(f"\nService '{service}' not found.")
    sys.exit(1)

print(f"\nDeleting:\n{service_dir}")

confirm = input("\nContinue? (yes/no): ").strip().lower()

if confirm != "yes":
    print("Cancelled.")
    sys.exit(0)

# Delete the complete application folder
try:
    shutil.rmtree(service_dir)
    print("Application folder removed.")
except Exception as e:
    print(f"Failed to delete application folder: {e}")
    sys.exit(1)

# Verify deletion
if service_dir.exists():
    print("Folder still exists!")
    sys.exit(1)

# Delete ArgoCD Application
if argocd_file.exists():
    argocd_file.unlink()
    print("ArgoCD Application removed.")

print("\nDone.")
print("Commit and push:")
print("git add .")
print(f"git commit -m 'Delete {service}'")
print("git push origin master")