terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

# Créer un réseau Docker
resource "docker_network" "mlops_network" {
  name = "mlops_network"
}

# Construire l'image Docker
resource "docker_image" "ml_app_image" {
  name = "ml_app_image:latest"
  build {
    context    = abspath("${path.module}/../ml_app")
    dockerfile = "Dockerfile"
  }
}

# Créer le conteneur pour l'application et MLflow
resource "docker_container" "ml_app" {
  name  = "ml_app"
  image = docker_image.ml_app_image.name
  networks_advanced {
    name = docker_network.mlops_network.name
  }
  ports {
    internal = 8000  # Flask
    external = 5000  # Accès Flask
  }
  ports {
    internal = 8001  # MLflow
    external = 8001  # Accès MLflow
  }
  volumes {
    host_path      = abspath("${path.module}/../ml_app")
    container_path = "/app"
  }
  restart = "always"
}
