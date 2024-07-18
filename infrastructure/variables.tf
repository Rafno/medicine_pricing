variable "server" {
  type = string
  default = "localhost:9000"
}

variable "user" {
    type = string
    default = "youraccesskey"
}

variable "password"{
    type = string
    sensitive = true
    default = "yoursecretkey"
}
