# Install k3S

## Steps

1. Install following packages:
    - ufw [installation instructions](https://linuxcapable.com/how-to-install-ufw-on-debian-linux/#install-ufw-on-debian-with-apt)

1. Add file [config.yaml](config.yaml) to `/etc/rancher/k3s/config.yaml`

1. Add file [psa.yaml](psa.yaml) to `/var/lib/rancher/k3s/server`

1. (Optional) Create network policies and mount it to `/var/lib/rancher/k3s/server/manifests` on path

1. Run following command to install from script
    ```sh
    source .env && curl -sfL https://get.k3s.io | sh -
    ```
   Or run following command to use script [install_k3s.sh](install_k3s.sh)
    ```sh
    source .env && sh install_k3s.sh
    ```