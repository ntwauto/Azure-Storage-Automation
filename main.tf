variable "subgroup" {}
variable "project_name" {}
variable "location" { default = "eastus" }
variable "environment" {}

module "storage" {
  source = "./modules/storage_account"

  resource_group_name  = "${var.subgroup}-${var.environment}-rg"
  storage_account_name = "${var.subgroup}${var.environment}sa"
  container_name       = "${var.project_name}-container"
  location             = var.location
}
