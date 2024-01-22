variable "hcloud_token" {
  sensitive = true # Requires terraform >= 0.14
}

# Configure the Hetzner Cloud Provider
provider "hcloud" {
  token = var.hcloud_token
}

# Create a new server running ubuntu
resource "hcloud_server" "polkadot-telemetry-test" {
  name        = "polkadot-telemetry-test"
  image       = "ubuntu-22.04"
  server_type = "cpx21"
  # location = "nbg1"
  ssh_keys = ["gdz", "spd@aira.life", "falcon"]
  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }
  lifecycle {
    ignore_changes = [
      # Ignore changes to tags, e.g. because a management agent
      # updates these based on some ruleset managed elsewhere.
      ssh_keys,
    ]
  }
}
