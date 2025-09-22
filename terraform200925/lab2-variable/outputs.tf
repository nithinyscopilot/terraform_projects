output "application_name" {
  value = var.application_name

}
output "environment_name" {
  value = var.environment_name

}
output "environment_prefix" {
  value = local.environment_prefix
}
output "suffix" {
  value = random_string.suffix.result
}
output "nithin_name" {
  value = var.nithin_name
}
output "api_key" {
  value     = var.api_key
  sensitive = true

}
output "name_regions" {
  value = var.region[0]

}
output "region_instance_count" {
  value = var.region_instance_count["us-east-1"]

}
# output "region_map" {
#   value = var.region_map[0]

# }
output "name_sku" {
  value = var.sku_setting.sku_name
}
output "modle" {
  value = module.alpha.random_string

}
