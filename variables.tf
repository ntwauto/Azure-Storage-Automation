variable "subgroup" {
  description = "Subgroup (e.g., neteng or wineng)"
  type        = string
}

variable "project_name" {
  description = "Project name (used for container)"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}
