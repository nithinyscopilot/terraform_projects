resource "random_string" "suffix" {
  length  = 4
  special = false
  upper   = false
}

locals {
  environment_prefix = "${var.application_name}-${var.environment_name}-${random_string.suffix.result}-${var.nithin_name}-${var.sku_setting.sku_name}"
}
resource "random_string" "map" {

  for_each = var.region_instance_count
  length   = 4
  special  = true
  upper    = true

}

resource "random_string" "if" {

  count   = var.enabled ? 1 : 0
  length  = 4
  special = true
  upper   = true

}
module "alpha" {
  source  = "hashicorp/module/random"
  version = "1.0.0"

}
module "charlie" {
  source = "./module/rado"
  length = 4
}
