resource "random_string" "suffix" {
  length  = 6
  upper   = false
  special = false
}

resource "azurerm_resource_group" "rg" {
  name     = "${var.subgroup}-${var.environment}-rg"
  location = var.location
}

resource "azurerm_storage_account" "sa" {
  # ✅ Fixed: prefixed with "st", includes subgroup/env, and adds random suffix
  name                     = lower("st${var.subgroup}${var.environment}${random_string.suffix.result}")
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  allow_blob_public_access = false
}

resource "azurerm_storage_container" "container" {
  name                  = var.container_name
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "private"
}

output "storage_account_name" {
  value = azurerm_storage_account.sa.name
}

output "container_name" {
  value = azurerm_storage_container.container.name
}
