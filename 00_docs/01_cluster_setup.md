# Cluster Setup

Playbook will:
- install K3S and copy the kubeconfig to the localhost
- deploy Flux2
- install CRDs for some apps

## Steps

1. (Optional) Create a virtual python environment for ansible

1. Run the [install_ansible.sh](../01_cluster_setup/install_ansible.sh) script, set the variables `USE_VENV` and `VENV_DIR` in the script according to your setup
    ```bash
    bash install_ansible.sh
    ```
   Ansible modules can also be installed manually.

1. Configure your inventory using the [default_inventory](../01_cluster_setup/default_inventory.yml) template. To setup the K3S cluster, the following minimal template can be used

    Futhermore, variables can be edited/added in the file [00_default.yml](../01_cluster_setup/vars/00_default.yml) to further configure the K3S installation

1. Run playbook by using following command
    ```bash
    ansible-playbook -i path/to/inventory.yml 01_cluster_setup.yml
    ```

## Further Details

- See the k3s docs for more info on ports used [here](https://docs.k3s.io/installation/requirements#networking)

- Directory [files](../01_cluster_setup/files/) contains some files not currently used in the deployment, but could be useful for further development