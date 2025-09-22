variable "application_name" {
  type        = string
  description = "Name of the application"

  validation {
    condition     = length(var.application_name) >= 5 && length(var.application_name) <= 20
    error_message = "Application name must be between 5 and 20 characters."
  }
}

variable "environment_name" {
  type        = string
  description = "Name of the environment"
}

variable "nithin_name" {
  type        = string
  description = "Your name"
}
variable "api_key" {
  type        = string
  description = "API key for the service"
  sensitive   = true

}
variable "vm_count" {
  type = number

  validation {
    condition     = var.vm_count >= 3 && var.vm_count <= 10 && var.vm_count % 2 != 0
    error_message = "VM count must be between 1 and 10."
  }

}
variable "enabled" {
  type = bool
}
variable "region" {
  type = list(string)

}
variable "region_instance_count" {
  type = map(string)

}
variable "region_map" {
  type = set(string)

}
variable "sku_setting" {
  type = object({
    sku_name     = string
    sku_tier     = string
    sku_capacity = number
  })


}
