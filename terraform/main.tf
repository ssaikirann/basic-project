terraform {
  required_version = ">= 1.0"
  
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

provider "local" {}
provider "null" {}

# Variables
variable "app_name" {
  description = "Application name"
  type        = string
  default     = "finance-tracker"
}

variable "app_version" {
  description = "Application version"
  type        = string
  default     = "1.0.0"
}

variable "docker_registry" {
  description = "Docker registry URL"
  type        = string
  default     = "ghcr.io"
}

variable "docker_image_tag" {
  description = "Docker image tag"
  type        = string
  default     = "latest"
}

# Local outputs directory
locals {
  config_dir = "${path.module}/k8s-config"
}

# Create k8s config directory
resource "local_file" "k8s_config_dir" {
  filename = "${local.config_dir}/.gitkeep"
  content  = ""
}

# Kubernetes Namespace
resource "local_file" "k8s_namespace" {
  filename = "${local.config_dir}/01-namespace.yaml"
  content = templatefile("${path.module}/../terraform/templates/namespace.tpl", {
    namespace = var.app_name
  })
  
  depends_on = [local_file.k8s_config_dir]
}

# Kubernetes ConfigMap
resource "local_file" "k8s_configmap" {
  filename = "${local.config_dir}/02-configmap.yaml"
  content = templatefile("${path.module}/../terraform/templates/configmap.tpl", {
    namespace = var.app_name
    app_name  = var.app_name
  })
  
  depends_on = [local_file.k8s_namespace]
}

# Kubernetes Deployment
resource "local_file" "k8s_deployment" {
  filename = "${local.config_dir}/03-deployment.yaml"
  content = templatefile("${path.module}/../terraform/templates/deployment.tpl", {
    namespace      = var.app_name
    app_name       = var.app_name
    docker_image   = "${var.docker_registry}/${var.app_name}:${var.docker_image_tag}"
    replicas       = 2
    memory_request = "128Mi"
    memory_limit   = "256Mi"
    cpu_request    = "100m"
    cpu_limit      = "500m"
  })
  
  depends_on = [local_file.k8s_configmap]
}

# Kubernetes Service
resource "local_file" "k8s_service" {
  filename = "${local.config_dir}/04-service.yaml"
  content = templatefile("${path.module}/../terraform/templates/service.tpl", {
    namespace = var.app_name
    app_name  = var.app_name
    port      = 8000
  })
  
  depends_on = [local_file.k8s_deployment]
}

# Kubernetes HorizontalPodAutoscaler
resource "local_file" "k8s_hpa" {
  filename = "${local.config_dir}/05-hpa.yaml"
  content = templatefile("${path.module}/../terraform/templates/hpa.tpl", {
    namespace   = var.app_name
    app_name    = var.app_name
    min_replicas = 2
    max_replicas = 5
  })
  
  depends_on = [local_file.k8s_service]
}

# Outputs
output "k8s_config_directory" {
  value       = local.config_dir
  description = "Path to generated Kubernetes manifests"
}

output "deployment_info" {
  value = {
    app_name       = var.app_name
    docker_image   = "${var.docker_registry}/${var.app_name}:${var.docker_image_tag}"
    namespace      = var.app_name
    replicas       = 2
  }
  description = "Deployment information"
}
