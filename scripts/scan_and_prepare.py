stages:
  - prepare
  - terraform

variables:
  TF_VAR_subgroup: "$SUBGROUP"
  TF_VAR_project_name: "$CI_PROJECT_NAME"
  TF_VAR_location: "eastus"

prepare:
  stage: prepare
  image: python:3.11
  before_script:
    - pip install requests
  script:
    - python3 scripts/scan_and_prepare.py "$GITLAB_TOKEN"
  artifacts:
    paths:
      - terraform/backend_templates/
    expire_in: 1 hour

terraform_apply:
  stage: terraform
  image: hashicorp/terraform:1.7.0
  needs: ["prepare"]
  parallel:
    matrix:
      - ENVIRONMENT: ["QA", "UAT", "PROD"]

  script:
    - cd terraform
    - echo "🔧 Using backend config for ${ENVIRONMENT}"
    - cp backend_templates/backend_${ENVIRONMENT}.hcl backend.hcl
    - terraform init -backend-config=backend.hcl
    - terraform plan -out=tfplan \
        -var "environment=${ENVIRONMENT}" \
        -var "subgroup=${SUBGROUP}" \
        -var "project_name=${CI_PROJECT_NAME}" \
        -var "arm_client_id=${ARM_CLIENT_ID_${ENVIRONMENT}}" \
        -var "arm_client_secret=${ARM_CLIENT_SECRET_${ENVIRONMENT}}" \
        -var "arm_tenant_id=${ARM_TENANT_ID_${ENVIRONMENT}}" \
        -var "arm_subscription_id=${ARM_SUBSCRIPTION_ID_${ENVIRONMENT}}"
    - terraform apply -auto-approve tfplan

  variables:
    ARM_CLIENT_ID: "$ARM_CLIENT_ID_${ENVIRONMENT}"
    ARM_CLIENT_SECRET: "$ARM_CLIENT_SECRET_${ENVIRONMENT}"
    ARM_TENANT_ID: "$ARM_TENANT_ID_${ENVIRONMENT}"
    ARM_SUBSCRIPTION_ID: "$ARM_SUBSCRIPTION_ID_${ENVIRONMENT}"
