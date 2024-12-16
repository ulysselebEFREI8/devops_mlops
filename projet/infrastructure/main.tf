terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_network" "mlops_network" {
  name = "mlops_network"
}

resource "docker_container" "ml_app" {
  name  = "ml_app"
  image = "python:3.9-slim"
  networks_advanced {
    name = docker_network.mlops_network.name
  }
  ports {
    internal = 5000
    external = 5000
  }
  command = [
    "sh", "-c", "pip install -r /app/requirements.txt && python /app/app.py"
  ]
  volumes {
    host_path      = abspath("${path.module}/../ml_app")  # Utilisation de abspath pour obtenir un chemin absolu
    container_path = "/app"
  }
}
