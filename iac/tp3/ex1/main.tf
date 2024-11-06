terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.0"
    }
  }

  required_version = ">= 1.0"
}

provider "docker" {}

resource "docker_network" "web" {
  name = "web-network"
}

resource "docker_container" "http" {
  image = "nginx:1.27"
  name  = "http"

  ports {
    internal = 8080
    external = 8080
  }

  networks_advanced {
    name = docker_network.web.name
  }

  volumes {
    host_path      = "/home/ulbefrei/devops_efrei/iac/tp3/ex1/app"
    container_path = "/app"
  }
}

resource "docker_container" "php_fpm" {
  image = "php:8.3-fpm"
  name  = "php-fpm"

  networks_advanced {
    name = docker_network.web.name
  }

  volumes {
    host_path      = "/home/ulbefrei/devops_efrei/iac/tp3/ex1/app"
    container_path = "/app"
  }
}
