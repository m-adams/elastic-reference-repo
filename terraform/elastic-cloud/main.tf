terraform {
  required_version = ">= 1.0.0"
  required_providers {
    ec = {
      source = "elastic/ec"
    }
  }
}
data "ec_stack" "latest" {
  version_regex = "latest"
  region = "us-west-1"
}
variable "name" {
  type = string
  default = "my_example_deployment"
}
variable "EC_API_KEY" {
  type = string
  sensitive = true
}
variable "region" {
  type = string
  default = "gcp-europe-west1"
}
variable "deployment_template_id" {
  type = string
  default = "gcp-memory-optimized-v2"
}
provider "ec" {
  apikey= var.EC_API_KEY
}
resource "ec_deployment"  "example" {
  name = var.name
  region = var.region
  version = data.ec_stack.latest.version
  deployment_template_id = var.deployment_template_id 
  elasticsearch = {
    hot = {
      zone_count = 2
      autoscaling = {
        min_size = "4g"
        max_size = "8g"
      }
    }
    ml = {
      autoscaling = {
        min_size = "0g"
        max_size = "32g"
      }
    }
  }
  kibana = {}
  enterprise_search = {}
  integrations_server = {}
}
