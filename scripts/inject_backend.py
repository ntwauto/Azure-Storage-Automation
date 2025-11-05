#!/usr/bin/env python3
import os
import sys
import requests

ENVIRONMENTS = ["QA", "UAT", "PROD"]
GITLAB_API = "https://gitlab.com/api/v4"

def get_project_variables(project_id, token):
    url = f"{GITLAB_API}/projects/{project_id}/variables"
    resp = requests.get(url, headers={"PRIVATE-TOKEN": token})
    resp.raise_for_status()
    return {v["key"]: v["value"] for v in resp.json()}

def main():
    if len(sys.argv) != 5:
        print("Usage: python3 inject_backend_and_validate_spns.py <gitlab_token> <project_id> <project_name> <subgroup>")
        sys.exit(1)

    gitlab_token = sys.argv[1]
    project_id = sys.argv[2]
    project_name = sys.argv[3]
    subgroup = sys.argv[4]

    # Create environment folders if they don't exist
    project_path = os.path.join("..", subgroup, project_name)  # automation runs from Terraform-Automation
    for env in ENVIRONMENTS:
        env_folder = os.path.join(project_path, "environment", env)
        os.makedirs(env_folder, exist_ok=True)

        # Create backend.hcl
        backend_file = os.path.join(env_folder, "backend.hcl")
        backend_content = f"""
resource_group_name  = "{subgroup}-{env}-rg"
storage_account_name = "st{subgroup}{env}"  # deterministic for backend
container_name       = "{project_name}-container"
key                  = "terraform.tfstate"
"""
        with open(backend_file, "w") as f:
            f.write(backend_content.strip())
        print(f"✅ backend.hcl created: {backend_file}")

    # Fetch SPNs from project-level variables
    project_vars = get_project_variables(project_id, gitlab_token)
    spns = {}
    error_flag = False

    for env in ENVIRONMENTS:
        spns[env] = {
            "ARM_CLIENT_ID": project_vars.get(f"ARM_CLIENT_ID_{env}"),
            "ARM_CLIENT_SECRET": project_vars.get(f"ARM_CLIENT_SECRET_{env}"),
            "ARM_TENANT_ID": project_vars.get(f"ARM_TENANT_ID_{env}"),
            "ARM_SUBSCRIPTION_ID": project_vars.get(f"ARM_SUBSCRIPTION_ID_{env}")
        }

        # Validate all SPNs exist
        missing_vars = [k for k, v in spns[env].items() if not v]
        if missing_vars:
            print(f"❌ ERROR: Missing SPNs for environment '{env}': {', '.join(missing_vars)}")
            error_flag = True

    if error_flag:
        print("❌ Aborting pipeline due to missing SPNs.")
        sys.exit(1)

    # Optionally print or export SPNs for logging
    for env in ENVIRONMENTS:
        print(f"✅ SPNs validated for {env}: {spns[env]}")

    print("✅ Backend injection and SPN validation completed successfully.")

if __name__ == "__main__":
    main()
