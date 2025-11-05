## Project Structure

```bash
Sotrage-Automation/
├── main.tf
├── provider.tf
├── variables.tf
├── modules/
│   └── storage_account/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── backend_templates/
│   ├── backend_QA.hcl
│   ├── backend_UAT.hcl
│   └── backend_PROD.hcl

