#!/usr/bin/env python3
import os
import sys

ENVIRONMENTS = ["QA", "UAT", "PROD"]

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 inject_backend.py <project_name> <subgroup>")
        sys.exit(1)

    project_name = sys.argv[1]
    subgroup = sys.argv[2]

    project_path = os.path.join(".", project_name)
    if not os.path.exists(project_path):
        os.makedirs(project_path)

    for env in ENVIRONMENTS:
        env_folder = os.path.join(project_path, "environment", env)
        os.makedirs(env_folder, exist_ok=True)
        backend_file = os.path.join(env_folder, "backend.hcl")

        backend_content = f"""
resource_group_name  = "{subgroup}-{env}-rg"
storage_account_name = "st{subgroup}{env}"  # deterministic for backend
container_name       = "{project_name}-container"
key                  = "terraform.tfstate"
"""
        with open(backend_file, "w") as f:
            f.write(backend_content.strip())
        print(f"✅ Created backend.hcl for {env} at {backend_file}")

    print("✅ Backend injection completed for all environments.")

if __name__ == "__main__":
    main()
