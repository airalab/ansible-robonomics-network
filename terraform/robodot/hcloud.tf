variable "hcloud_token" {
  sensitive = true
}

# Configure the Hetzner Cloud Provider
provider "hcloud" {
  token = var.hcloud_token
}

# Create a new server running debian
resource "hcloud_server" "robodot_node" {
  for_each    = var.hcloud_robodot_nodes
  name        = each.value["name"]
  image       = "ubuntu-22.04"
  server_type = "cx11"
  location    = "nbg1"
  ssh_keys    = ["gdz", "spd@aira.life", "falcon"]
  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }
  lifecycle {
    ignore_changes = [
      ssh_keys,
    ]
  }
}

resource "hcloud_volume" "robodot_node_volume" {
  for_each    = var.hcloud_robodot_nodes
  name      = each.value["volume_name"]
  size      = each.value["volume_size"]
  server_id = hcloud_server.robodot_node[each.key].id
  automount = true
  format    = "xfs"
}

output "server_ips" {
  value = hcloud_server.robodot_node.*
}