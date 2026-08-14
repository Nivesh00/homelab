# Infrastructure

Infrastructure repository contains the controllers (`01_controllers`) and configurations (`02_configs`). Configurations depends on the controllers as they are mostly custom resources and must wait for the Helm Chart to

## Cert Manager

- Used for TLS certificates
- Let's Encrypt is used as CA
- `letsencrypt-staging` for staging and `letsencrypt-production` for prodution

## Github Runner

- Github runner helm charts are installed
- Dockerfile for runner container can be found at [utility-tools](../files/dockerfiles/utility-tools)


## Keycloak

- Keycloak used for OIDC

## Kube Prometheus Stack

- Used for monitoring

## Postgres Operator

- Postgres as DB for cluster

## Traefik

Traefik is used for the gateway api. Ingress is disabled

- ListenerSets are not currently used, they will be added as soon as they are ready: https://github.com/traefik/traefik/pull/12909
- All configs for httproutes are found in [](../03_infrastructure/02_configs/traefik/http-route.yml)