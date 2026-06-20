# Clusters

Clusters for FluxCD. Each cluster is divided into stacks:
- Infrastructure: for components that make up the cluster (proxy, certificate managers, etc)
- Applications: for application running inside the cluster

## Infrastructure

The `infrastructure.yml` file contains:
- `infra-controllers`: for controllers, helm charts deployment etc.
- `infra-configs`: for configurations, crds, etc.
