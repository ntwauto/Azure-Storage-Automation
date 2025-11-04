gitlab_azure_automation/
├── scripts/                      # Python automation scripts (for GitLab)
├── terraform/
│   ├── main.tf                   # Calls module per environment
│   ├── variables.tf
│   ├── outputs.tf
│   └── modules/
│       └── storage_account/
│           ├── main.tf
│           ├── variables.tf
│           └── outputs.tf
└── .gitlab-ci.yml
