terraform {
  required_providers {
    minio = {
      source  = "aminueza/minio"
      version = "2.3.2"
    }
  }
}

provider "minio" {
  minio_server   = "localhost:9000"
  minio_user     = "youraccesskey"
  minio_password = "yoursecretkey"
}

resource "minio_s3_bucket" "logs" {
  bucket = "logs"
  acl    = "public"
}

resource "minio_s3_bucket" "staging" {
  bucket = "staging"
  acl    = "public"
}

resource "minio_s3_bucket" "db" {
  bucket = "database"
  acl    = "public"
}
