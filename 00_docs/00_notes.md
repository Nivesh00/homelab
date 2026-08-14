
# General notes

## Flux commands

- Build manifests locally
    ```sh
    kubectl kustomize  03_infrastructure/01_controllers --output .local/infra-controllers.yml
    ```

    ```sh
    kubectl kustomize  03_infrastructure/02_configs --output .local/infra-config.yml
    ```

- [flux build](https://fluxcd.io/flux/cmd/flux_build_kustomization/)

    Build controllers
    ```sh
    flux build kustomization infra-controllers --path ./02_clusters/homelab/flux-system > .local/infra-controllers.yml
    ```

    Build configs
    ```sh
    flux build kustomization infra-config --path ./02_clusters/homelab/flux-system > .local/infra-config.yml     
    ```

- `flux reconcile` - reconcile git repo state with cluster state


## Github Actions

- `workflow_dispatch` - manually trigger github actions workflow

## Rotate Token

- Following commands are ran
    ```sh
    # Delete existing secret
    kubectl -n flux-system delete secret flux-system

    # Create new secret
    flux create secret git flux-system --url ssh://git@github.com/Nivesh00/homelab --private-key-file ~/.ssh/homelab_github_ed25519

    # Run bootstrap command again

    flux bootstrap git --url ssh://git@github.com/Nivesh00/homelab --branch main --private-key-file ~/.ssh/homelab_github_ed25519 --path ./02_clusters/homelab
    ```