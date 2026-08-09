# Infrastructure

Infrastructure repository contains the controllers and configurations. Configurations depends on the controllers as they are mostly custom resources and must wait for the Helm Chart to

## Traefik

Traefik is used for the gateway api. Ingress is disabled

- ListenerSets are not currently used, they will be added as soon as they are ready: https://github.com/traefik/traefik/pull/12909
- All configs for httproutes are found in [](../03_infrastructure/02_configs/traefik/http-route.yml)

## Cert Manager

- Used for TLS certificates
- Let's Encrypt is used as CA
- `letsencrypt-staging` for staging and `letsencrypt-production` for prodution

## Prometheus

Prometheus is used for monitoring