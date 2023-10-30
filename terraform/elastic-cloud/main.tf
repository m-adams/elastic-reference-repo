terraform {
  required_version = ">= 1.0.0"

  required_providers {
    ec = {
      source = "elastic/ec"
    }
    elasticstack = {
      source  = "elastic/elasticstack"
      version = "~>0.9"
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
variable "apikey" {
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
  apikey= var.apikey
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

# See docs here https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/guides/elasticstack-and-cloud
provider "elasticstack" {
  # Use our Elastic Cloud deployment outputs for connection details.
  # This also allows the provider to create the proper relationships between the two resources.
  elasticsearch {
    endpoints = ["${ec_deployment.example.elasticsearch[0].https_endpoint}"]
    username  = ec_deployment.example.elasticsearch_username
    password  = ec_deployment.example.elasticsearch_password
  }
}



