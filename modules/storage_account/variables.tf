variable "resource_group_name" {
  type        = string
  description = "Resource group name"
}

variable "storage_account_name" {
  type        = string
  description = "Storage account name"
}

variable "container_name" {
  type        = string
  description = "Container name for the project"
}

variable "location" {
  type        = string
  default     = "eastus"
}

variable "subgroup" {
  type        = string
}

variable "environment" {
  type        = string
}
