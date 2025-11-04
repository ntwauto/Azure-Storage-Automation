import os
import requests

# ────────────────────────────────
# CONFIGURATION
# ────────────────────────────────
GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")  # Personal Access Token
ENVIRONMENTS = ["QA", "UAT", "PROD"]
HEADERS = {
    "PRIVATE-TOKEN": GITLAB_TOKEN,
    "Content-Type": "application/json"
}

# Known subgroup IDs for reference (optional, can be removed if fully dynamic)
SUBGROUPS = {
    792: "neteng",
    791: "wineng"
}

# ────────────────────────────────
# HELPER FUNCTIONS
# ────────────────────────────────
def get_parent_subgroup(project_name):
    """
    Searches all known subgroups for the project and returns the subgroup ID
    """
    for subgroup_id in SUBGROUPS.keys():
        search_url = f"{GITLAB_URL}/api/v4/groups/{subgroup_id}/projects?search={project_name}"
        r = requests.get(search_url, headers=HEADERS)
        if r.status_code == 200 and len(r.json()) > 0:
            return r.json()[0]["namespace"]["id"]  # subgroup ID
    return None


def create_project(subgroup_id, project_name):
    # Check if project exists
    search_url = f"{GITLAB_URL}/api/v4/groups/{subgroup_id}/projects?search={project_name}"
    r = requests.get(search_url, headers=HEADERS)
    if r.status_code == 200 and len(r.json()) > 0:
        project = r.json()[0]
        print(f"✅ Project already exists: {project['web_url']}")
        return project

    # Create project
    print(f"📁 Creating project {project_name} under subgroup ID {subgroup_id}")
    payload = {
        "name": project_name,
        "namespace_id": subgroup_id,
        "initialize_with_readme": True,
        "visibility": "private"
    }
    create_url = f"{GITLAB_URL}/api/v4/projects"
    r = requests.post(create_url, headers=HEADERS, json=payload)
    if r.status_code == 201:
        project = r.json()
        print(f"✅ Created: {project['web_url']}")
        return project
    else:
        print(f"❌ Failed to create project: {r.text}")
        return None


def create_environment_folders(project):
    project_id = project["id"]
    print("📁 Creating environment folders (QA, UAT, PROD)...")

    actions = []
    for env in ENVIRONMENTS:
        path = f"environments/{env}/.keep"
        content = f"# {env} environment folder\n"
        actions.append({"action": "create", "file_path": path, "content": content})

    commit_payload = {
        "branch": "main",
        "commit_message": "Add environments folders (QA, UAT, PROD)",
        "actions": actions
    }

    commit_url = f"{GITLAB_URL}/api/v4/projects/{project_id}/repository/commits"
    r = requests.post(commit_url, headers=HEADERS, json=commit_payload)
    if r.status_code == 201:
        print("✅ Environments folders created.")
    else:
        print(f"❌ Failed to create folders: {r.text}")


def create_ci_variables(project):
    project_id = project["id"]
    print("🔐 Creating CI/CD variables per environment...")

    for env in ENVIRONMENTS:
        for var in ["ARM_CLIENT_ID", "ARM_CLIENT_SECRET", "ARM_TENANT_ID", "ARM_SUBSCRIPTION_ID"]:
            key = f"{env}_{var}"
            value = f"PLACEHOLDER_{env}_{var}"

            payload = {
                "key": key,
                "value": value,
                "masked": True,
                "protected": False
            }

            url = f"{GITLAB_URL}/api/v4/projects/{project_id}/variables"
            r = requests.post(url, headers=HEADERS, json=payload)
            if r.status_code != 201:
                print(f"⚠️ Could not create {key}: {r.text}")

    print("✅ CI/CD variables created per environment.")


# ────────────────────────────────
# MAIN
# ────────────────────────────────
def main():
    if not GITLAB_TOKEN:
        print("❌ Missing GITLAB_TOKEN environment variable.")
        return

    # Project name comes from CI/CD variable
    project_name = os.getenv("CI_PROJECT_NAME_OVERRIDE")
    if not project_name:
        print("❌ CI_PROJECT_NAME_OVERRIDE not set in pipeline variables.")
        return

    # Detect subgroup automatically
    subgroup_id = get_parent_subgroup(project_name)
    if not subgroup_id:
        print("❌ Could not detect parent subgroup automatically.")
        return

    project = create_project(subgroup_id, project_name)
    if project:
        create_environment_folders(project)
        create_ci_variables(project)

    print("🎉 Project setup complete!")


if __name__ == "__main__":
    main()
