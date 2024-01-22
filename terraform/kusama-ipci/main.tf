provider "google" {
    credentials = file("gcp-creds.json")
    project = "robokusama"
    region = "europe-west2"
    zone = "europe-west2-c"
}

resource "google_compute_address" "static" {
  name = "ipv4-address"
}

### IPCI COLLATOR 2 ###
resource "google_compute_disk" "kusama_ipci_collator_2_volume" {
  name  = "kusama-ipci-collator-2-volume"
  type  = "pd-ssd"
  zone = "europe-west2-c"
  project = "robokusama"
  size = 700
  image = "polka-db-27112023"
}
resource "google_compute_attached_disk" "kusama_ipci_collator_2_volume" {
  disk     = google_compute_disk.kusama_ipci_collator_2_volume.id
  instance = google_compute_instance.kusama_ipci_collator_2.id
}
resource "google_compute_instance" "kusama_ipci_collator_2" {
  allow_stopping_for_update = true
  name = "kusama-ipci-collator-2"
  machine_type = "c2-standard-4"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.static.address
    }
  }

  metadata = {
    ssh-keys = "root:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCtR7Z2S1nQ39I6nm3G+zFqJX03QpPdkRwTxe8PLFQTXiq6hFfzn3SDkuZY1HJz8pJWhIscrjFKhqiYtVZfM5r4Bl+yVrFKfNkOxlN4n3Kt2/ddvGg/HXG0d47ljW1bY/9o+S5XSFKMuQfIcgPOULDQpIkhBnHLiC+yuMDrDigQvbQd5a3jHv4MKOvqEMRZ6ajhpGW76Uo4K04eimf5AfF8dxD27E5fTDNP+f0SK69kji5OZ7Hh76CM7Z/MNfBpbe44rc464RqlefwfHc3JFJ1y82qD6eGlqe8SpenOh2Ay1tT+Hax3/PWit+AujGpm273so7xHXjJEoF+knudiF7/F gdz"
  }

  lifecycle {
    ignore_changes = [attached_disk]
  }
}
### \IPCI COLLATOR 2 ###


### IPCI BOOTNODE 2 ###
resource "google_compute_address" "kusama_ipci_bootnode_2_static_ip" {
  name = "kusama-ipci-bootnode-2-static-ip"
}

resource "google_compute_disk" "kusama_ipci_bootnode_2_volume" {
  name  = "kusama-ipci-bootnode-2-volume"
  type  = "pd-ssd"
  zone = "europe-west2-c"
  project = "robokusama"
  size = 700
  image = "polka-db-27112023"
}
resource "google_compute_attached_disk" "kusama_ipci_bootnode_2_volume" {
  disk     = google_compute_disk.kusama_ipci_bootnode_2_volume.id
  instance = google_compute_instance.kusama_ipci_bootnode_2.id
}
resource "google_compute_instance" "kusama_ipci_bootnode_2" {
  # allow_stopping_for_update = true
  name = "kusama-ipci-bootnode-2"
  machine_type = "c2-standard-4"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = google_compute_address.kusama_ipci_bootnode_2_static_ip.address
    }
  }

  metadata = {
    ssh-keys = "root:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCtR7Z2S1nQ39I6nm3G+zFqJX03QpPdkRwTxe8PLFQTXiq6hFfzn3SDkuZY1HJz8pJWhIscrjFKhqiYtVZfM5r4Bl+yVrFKfNkOxlN4n3Kt2/ddvGg/HXG0d47ljW1bY/9o+S5XSFKMuQfIcgPOULDQpIkhBnHLiC+yuMDrDigQvbQd5a3jHv4MKOvqEMRZ6ajhpGW76Uo4K04eimf5AfF8dxD27E5fTDNP+f0SK69kji5OZ7Hh76CM7Z/MNfBpbe44rc464RqlefwfHc3JFJ1y82qD6eGlqe8SpenOh2Ay1tT+Hax3/PWit+AujGpm273so7xHXjJEoF+knudiF7/F gdz"
  }

  lifecycle {
    ignore_changes = [attached_disk]
  }
}
### /IPCI BOOTNODE 2 ###