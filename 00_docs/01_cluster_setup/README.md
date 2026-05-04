# Cluster Setup

## Steps

1. (Optional) Create a virtual python environment for ansible

1. Run the [install_ansible.sh](../../install_ansible.sh) script, set the variables `USE_VENV` and `VENV_DIR` in the script according to your setup
    ```sh
    bash install_ansible.sh   
    ```
   Ansible modules can also be installed manually.

1. Configure your inventory using the [default_inventory](../default_inventory.yml) template. To setup the K3S cluster, the following minimal template can be used
    ```yml
    ## inventory.yml
    all:
        vars:
            ENVIRONMENT: # e.g. dev, stg, prd

        children:
            servers:
            hosts:
                main_server:
                ansible_host: <remote-ip>
                ansible_user: <remote-user>
                ansible_ssh_private_key_file: /path/to/ssh/file
                ansible_python_interpreter: /usr/bin/python3

                localhost:
                ansible_host: 127.0.0.1
                ansible_connection: local
                ansible_python_interpreter: /usr/bin/python3
    ```
    Futhermore, variables can be edited/added in the file [00_default.yml](./vars/00_default.yml) to further configure the K3S installation

1. Run playbook by using following command
    ```sh
    ansible-playbook -i path/to/inventory.yml setup_k3s_cluster.yml
    ```

1. Your kubeconfig file should now be available under `~/.kube/default.yml`. Change the ip from `127.0.0.1` to the ip of the server and done! The cluster should now be accessible using [kubectl](https://kubernetes.io/docs/reference/kubectl/)

## Playbook Details

Playbook does the following:
- Use UFW to configure firewall, see the k3s docs for more info on ports used (https://docs.k3s.io/installation/requirements#networking)

- Loads the [config file](./files/00_config.yaml) for K3S on the remote host

- Installs K3S and fetches the kubeconfig file