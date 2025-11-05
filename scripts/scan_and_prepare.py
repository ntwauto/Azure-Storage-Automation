#!/usr/bin/env python3
import os
import sys
import json
import requests

GITLAB_API = "https://gitlab.com/api/v4"
TOP_GROUP_ID = 795  # Azure Infrastructure group ID
ENVIRONMENTS = ["QA", "UAT", "PROD"]
REQUIRED_VARS = [
    "ARM_CLIENT_ID",
    "ARM_CLIENT_SECRET",
    "ARM_TENANT_ID",
    "ARM_SUBSCRIPTION_ID"
]

def get(url, token):
    r = requests.get(url, headers={"PRIVATE-TOKEN": token})
    r.raise_for_status()
    return r.json()

def ensure_env_folders(project_path):
    env_dir = os.path.join(project_path, "environment")
    os.makedirs(env_dir, exist_ok=True)
    for env in ENVIRONMENTS:
        os.makedirs(os.path.join(env_dir, env), exist_ok=True)

def create_backend_files(subgroup, project_name):
    os.makedirs("terraform/backend_templates", exist_ok=True)
    for env in ENVIRONMENTS:
        backend_content = f"""
resource_group_name  = "{subgroup}-{env}-rg"
storage_account_name = "st{subgroup}{env}"  # Terraform will add random suffix
container_name       = "{project_name}-container"
key                  = "terraform.tfstate"
"""
        with open(f"terraform/backend_templates/backend_{env}.hcl", "w") as f:
            f.write(backend_content.strip())

def check_project_vars(project_id, token, subgroup):
    url = f"{GITLAB_API}/projects/{project_id}/variables"
    vars_in_project = get(url, token)
    var_names = [v["key"] for v in vars_in_project]

    for env in ENVIRONMENTS:
        for base_var in REQUIRED_VARS:
            var_name = f"{base_var}_{env}"
            if var_name not in var_names:
                print(f"⚠️ Warning: Missing variable {var_name} in project {project_id} ({subgroup}/{env})")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scan_and_prepare.py <gitlab_token>")
        sys.exit(1)

    token = sys.argv[1]

    # Get all subgroups under top-level group
    subgroups = get(f"{GITLAB_API}/groups/{TOP_GROUP_ID}/subgroups?per_page=100", token)

    for sg in subgroups:
        subgroup_name = sg["name"]
        subgroup_id = sg["id"]
        print(f"🔍 Processing subgroup: {subgroup_name}")

        # Get all projects in subgroup
        projects = get(f"{GITLAB_API}/groups/{subgroup_id}/projects?per_page=100", token)
        for proj in projects:
            project_name = proj["name"]
            project_id = proj["id"]
            print(f"  📁 Checking project: {project_name}")
            ensure_env_folders(f"./{project_name}")
            check_project_vars(project_id, token, subgroup_name)
            create_backend_files(subgroup_name, project_name)

    print("✅ Completed scanning and backend file generation.")

if __name__ == "__main__":
    main()
