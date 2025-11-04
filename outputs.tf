output "storage_accounts" {
  description = "Map of storage accounts per environment"
  value       = { for k, m in module.storage_accounts : k => m.storage_account_name }
}

output "containers" {
  description = "Map of container names per environment"
  value       = { for k, m in module.storage_accounts : k => m.container_name }
}
