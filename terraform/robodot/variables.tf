terraform {
  required_providers {
    hcloud = {
      source = "hetznercloud/hcloud"
    }
    google = {
      source = "hashicorp/google"
    }
  }
  required_version = ">= 0.13"
}

variable "hcloud_robodot_nodes" {
  type = map(object({
    name = string
    location = string
    volume_name  = string
    volume_size = number
  }))
  #TODO: volume_size at least 360Gb
  default = {
    robodot-collator-1 = {
      name = "robodot-collator-1"
      location    = "fsn1"
      volume_name  = "robodot-collator-1-vol"
      volume_size = 15
    },
    robodot-bootnode-1 = {
      name = "robodot-bootnode-1"
      location    = "hel1"
      volume_name  = "robodot-bootnode-1-vol"
      volume_size = 10
    },
    robodot-bootnode-2 = {
      name = "robodot-bootnode-2"
      location    = "fsn1"
      volume_name  = "robodot-bootnode-2-vol"
      volume_size = 10
    },
    robodot-public-node-1 = {
      name = "robodot-public-node-1"
      location    = "nbg1"
      volume_name  = "robodot-public-node-1-vol"
      volume_size = 10
    }
  }
}

variable "google_robodot_nodes" {
  type = map(object({
    name = string
    location = string
    volume_name  = string
    volume_size = number
  }))
  default = {
    robodot-collator-2 = {
      name = "robodot-collator-2"
      location    = "fsn1"
      volume_name  = "robodot-collator-2-vol"
      volume_size = 15
    },
    robodot-bootnode-3 = {
      name = "robodot-bootnode-3"
      location    = "hel1"
      volume_name  = "robodot-bootnode-3-vol"
      volume_size = 10
    }
  }
}