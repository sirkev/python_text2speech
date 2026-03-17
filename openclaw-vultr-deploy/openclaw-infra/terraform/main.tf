terraform {
  required_providers {
    vultr = {
      source  = "vultr/vultr"
      version = "2.21.0"
    }
  }
  backend "local" {
    path = "/home/kev/.terraform_states/openclaw/terraform.tfstate"
  }
}

provider "vultr" {
  api_key = var.vultr_api_key
}

resource "vultr_ssh_key" "openclaw_key" {
  name    = "openclaw-key"
  ssh_key = file("~/.ssh/id_rsa.pub")
}

resource "vultr_instance" "openclaw_server" {
  plan        = var.plan
  region      = var.region
  os_id       = var.os_id
  label       = "openclaw-server"
  tags        = ["openclaw"]
  hostname    = "openclaw"
  ssh_key_ids = [vultr_ssh_key.openclaw_key.id]
  backups     = "disabled"
  ddos_protection = false
  activation_email = true
}

output "server_ip" {
  value = vultr_instance.openclaw_server.main_ip
}
