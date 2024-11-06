terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "~> 2.0"
    }
  }
}

provider "docker" {}

# HTTP container
resource "docker_container" "http" {
  image = docker_image.nginx.latest
  name  = "http"

  ports {
    internal = 80
    external = 8080
  }

  volumes {
    host_path      = "/home/ulb/tp3/ex2/nginx.conf"
    container_path = "/etc/nginx/nginx.conf"
  }
}

# SCRIPT container
resource "docker_container" "script" {
  image = docker_image.php.latest
  name  = "script"

  env = ["PHP_FPM_HOST=http"]

  volumes {
    host_path      = "/home/ulb/tp3/ex2/app"
    container_path = "/var/www/html"
  }
}

# DATA container
resource "docker_container" "data" {
  image = docker_image.mariadb.latest
  name  = "data"

  env = [
    "MYSQL_ROOT_PASSWORD=rootpassword",
    "MYSQL_DATABASE=testdb",
    "MYSQL_USER=user",
    "MYSQL_PASSWORD=userpassword"
  ]

  ports {
    internal = 3306
    external = 3306
  }
}

# Docker images for each container
resource "docker_image" "nginx" {
  name = "nginx:latest"
  keep_locally = false
}

resource "docker_image" "php" {
  name = "php:7.4-fpm"
  keep_locally = false
}

resource "docker_image" "mariadb" {
  name = "mariadb:latest"
  keep_locally = false
}
