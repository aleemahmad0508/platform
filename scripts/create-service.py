import os
import shutil
from pathlib import Path

# -----------------------------
# Platform Paths
# -----------------------------
ROOT = Path(__file__).resolve().parent.parent

TEMPLATE_APP = ROOT / "templates" / "app"
TEMPLATE_HELM = ROOT / "templates" / "helm"

APPLICATIONS = ROOT / "applications"
print(ROOT)
print(TEMPLATE_APP)

print(TEMPLATE_HELM)

# -----------------------------
# User Input
# -----------------------------
print("=" * 50)
print("Platform Engineering - Create New Service")
print("=" * 50)

service_name = input("Service Name : ").strip().lower()
namespace = input("Namespace    : ").strip().lower()
docker_repo = input("Docker Repo  : ").strip()
image_tag = input("Image Tag    : ").strip()

container_port = input("Container Port (5000): ").strip()
service_port = input("Service Port (80): ").strip()

host = input("Ingress Host (service.local): ").strip()

if container_port == "":
    container_port = "5000"

if service_port == "":
    service_port = "80"

if host == "":
    host = f"{service_name}.local"

# # -----------------------------
# # Destination Paths
# # -----------------------------
service_dir = APPLICATIONS / service_name

app_dir = service_dir / "app"
helm_dir = service_dir / "helm"

print(service_dir)
print(app_dir)
print(helm_dir)

# -----------------------------
# Check Existing Service
# -----------------------------
if service_dir.exists():
    print(f"\nERROR: '{service_name}' already exists.")
    exit(1)

# -----------------------------
# Create Folder Structure
# -----------------------------
print("\nCreating folders...")

service_dir.mkdir(parents=True)

# -----------------------------
# Copy Templates
# -----------------------------
print("Copying application template...")

shutil.copytree(TEMPLATE_APP, app_dir)

print("Copying Helm chart...")

shutil.copytree(TEMPLATE_HELM, helm_dir)

print("\nService structure created successfully.")

print("\nGenerated:")

print(app_dir)
print(helm_dir)





# -----------------------------
# OpenTelemetry Endpoint
# -----------------------------
OTEL_ENDPOINT = (
    "otel-collector-collector.observability.svc.cluster.local:4317"
)

# -----------------------------
# Helper Function
# -----------------------------
def replace_in_file(file_path, replacements):
    with open(file_path, "r") as f:
        content = f.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(file_path, "w") as f:
        f.write(content)

# -----------------------------
# Update app.py
# -----------------------------
print("\nUpdating app.py...")

app_file = app_dir / "app.py"

replace_in_file(
    app_file,
    {
        "{{SERVICE_NAME}}": service_name,
        "{{OTEL_ENDPOINT}}": OTEL_ENDPOINT,
        "{{PORT}}": container_port,
    },
)

# -----------------------------
# Update Helm values.yaml
# -----------------------------
print("Updating values.yaml...")

values_file = helm_dir / "values.yaml"

replace_in_file(
    values_file,
    {
        "name: flask": f"name: {service_name}",
        "namespace: flask": f"namespace: {namespace}",
        "repository: aleemahmad2/flask-demo": f"repository: {docker_repo}",
        'tag: "v2"': f'tag: "{image_tag}"',
        "port: 5000": f"port: {container_port}",
        "targetPort: 5000": f"targetPort: {container_port}",
        "host: flask.local": f"host: {host}",
    },
)

# -----------------------------
# Generate ArgoCD Application
# -----------------------------
print("Generating ArgoCD Application...")

template = ROOT / "shared" / "gitops" / "application-template.yaml"

output = (
    ROOT
    / "shared"
    / "gitops"
    / f"{service_name}-application.yaml"
)

with open(template, "r") as f:
    app_yaml = f.read()

app_yaml = app_yaml.replace("{{APP_NAME}}", service_name)
app_yaml = app_yaml.replace("{{NAMESPACE}}", namespace)
app_yaml = app_yaml.replace(
    "{{REPO_URL}}",
    "https://github.com/aleemahmad0508/platform.git",
)

with open(output, "w") as f:
    f.write(app_yaml)

print("ArgoCD Application created.")

print("\nConfiguration completed successfully.")


# -----------------------------
# Summary
# -----------------------
# ------
print("\n" + "=" * 60)
print("SERVICE CREATED SUCCESSFULLY")
print("=" * 60)

print(f"Service Name : {service_name}")
print(f"Namespace    : {namespace}")
print(f"Docker Image : {docker_repo}:{image_tag}")
print(f"Container    : {container_port}")
print(f"Service Port : {service_port}")
print(f"Ingress Host : {host}")

print("\nCreated Files")

print(f"Application : {app_dir}")
print(f"Helm Chart  : {helm_dir}")
print(f"ArgoCD App  : {output}")

print("\nNext Steps")
print("-" * 60)

print("1. Develop your business logic inside:")
print(f"   {app_dir / 'app.py'}")

print("\n2. Build Docker image")
print(f"   docker build -t {docker_repo}:{image_tag} {app_dir}")

print("\n3. Push Docker image")
print(f"   docker push {docker_repo}:{image_tag}")

print("\n4. Commit your changes")
print("   git add .")
print(f"   git commit -m 'Add {service_name} service'")
print("   git push")

print("\n5. ArgoCD will detect the Git change")
print("   and deploy the application automatically.")

print("=" * 60)