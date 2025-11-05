## Project Structure

```bash
Azure Infrastructure/              <-- Top-level group
├─ Terraform-Automation/          <-- Automation project with terraform & scripts
│  ├─ terraform/
│  │   ├─ modules/
│  │   │   └─ storage_account/
│  │   ├─ main.tf
│  │   ├─ provider.tf
│  │   └─ variables.tf
│  ├─ scripts/
│  │   └─ inject_backend.py
│  └─ .gitlab-ci.yml
├─ neteng/                        <-- Subgroup
│  └─ NewProject1/                <-- Project created dynamically
│      └─ environment/
│          ├─ QA/backend.hcl
│          ├─ UAT/backend.hcl
│          └─ PROD/backend.hcl
└─ wineng/                        <-- Subgroup
   └─ NewProject2/
       └─ environment/
           ├─ QA/backend.hcl
           ├─ UAT/backend.hcl
           └─ PROD/backend.hcl
