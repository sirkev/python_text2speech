variable "vultr_api_key" {
  description = "Vultr API Key"
  type        = string
}

variable "region" {
  default = "fra" # Frankfurt, or change to user preference
}

variable "plan" {
  default = "vc2-1c-2gb" # 2 vCPU, 2GB RAM
}

variable "os_id" {
  default = 2284 # Ubuntu 24.04 LTS x64
}
