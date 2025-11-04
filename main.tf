variable "subgroup" {
  type        = string
  description = "Subgroup name (e.g., neteng, wineng)"
}

variable "project_name" {
  type        = string
  description = "Project name inside the subgroup"
}

variable "location" {
  type        = string
  default     = "eastus"
}

locals {
  environments = ["QA", "UAT", "PROD"]
}

module "storage_accounts" {
  source = "./modules/storage_account"

  for_each = toset(local.environments)

  resource_group_name  = "${var.subgroup}-${each.key}-rg"
  storage_account_name = lower("${var.subgroup}${each.key}sa")   # one per env per subgroup
  container_name       = "${var.project_name}-container"          # one per project
  location             = var.location
  subgroup             = var.subgroup
  environment          = each.key
}
