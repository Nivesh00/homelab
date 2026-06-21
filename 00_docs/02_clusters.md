# Clusters

Clusters for FluxCD. Each cluster is divided into stacks:
- Infrastructure: for components that make up the cluster (proxy, certificate managers, etc)
- Applications: for application running inside the cluster

## Secrets

- SOPs as secret encryption
- Command is
    ```bash
    sops --encrypt --encrypted-regex '^(data|stringData)$' --pgp ${KEY_FP} \
    --in-place 02_flux2/03_SOPS_demo/secret.yaml
    ```

- Useful links:
    - https://fluxcd.io/flux/guides/mozilla-sops/
    - https://devopstales.github.io/kubernetes/gitops-flux2-sops/

## Infrastructure

The `infrastructure.yml` file contains:
- `infra-controllers`: for controllers, helm charts deployment etc.
- `infra-configs`: for configurations, crds, etc.

