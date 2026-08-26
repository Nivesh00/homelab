# Clusters

Clusters for FluxCD. Each cluster is divided into stacks:
- Infrastructure: for components that make up the cluster (proxy, certificate managers, etc)
- Applications: for application running inside the cluster

## Global Vars

- Variables are defined in file [vars-common.yml](../files/manual-deployments/vars-common.yml)

- Secrets are defined in file [secrets-common.yml](../files/manual-deployments/secrets-common.yml)

```sh
kubectl apply -f files/manual-deployments/
```

## Secrets

- SOPs as secret encryption

- List all secrets
    ```sh
    gpg --list-secret-keys
    ```

- Secret [sops-secret.yml](../files/manual-deployments/sops-secret.yml) must be applied
    ```sh
    kubectl apply -f files/manual-deployments/sops-secret.yml
    ```

- Encrypt secret
    ```sh
    # template
    sops --encrypt --encrypted-regex <regex-of-secret-keys> --pgp <PGP-key-id> --in-place /path/to/secret/file.yml
    # example with values
    sops --encrypt --encrypted-regex '^(data|stringData)$' --pgp "87AD5A3C61D4124E53D41EACAB6F74E497AB" --in-place secrets.yml
    ```

- Useful links:
    - https://fluxcd.io/flux/guides/mozilla-sops/
    - https://devopstales.github.io/kubernetes/gitops-flux2-sops/
    - Flux SOPS docs: https://fluxcd.io/flux/guides/mozilla-sops/

## Infrastructure

The `infrastructure.yml` file contains:
- `infra-controllers`: for controllers, helm charts deployment etc.
- `infra-configs`: for configurations, crs, etc.

## Application

Analog to infrastructure