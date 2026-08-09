# Clusters

Clusters for FluxCD. Each cluster is divided into stacks:
- Infrastructure: for components that make up the cluster (proxy, certificate managers, etc)
- Applications: for application running inside the cluster

All variables are defined in file [vars-common.yml](../files/vars-common.yml) and then applied to the cluster using following command
```sh
kubectl apply -f files/vars-common.yml
```

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

