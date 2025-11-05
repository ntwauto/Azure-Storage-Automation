## Project Structure

```bash
gitlab_azure_automation/
├── scripts/
│   └── scan_and_prepare.py
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── modules/
│   │   └── storage_account/
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       └── outputs.tf
│   └── backend_templates/
│       ├── backend_QA.hcl
│       ├── backend_UAT.hcl
│       ├── backend_PROD.hcl
├── .gitlab-ci.yml
