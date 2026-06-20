# Infrastructure

Infrastructure repository contains the controllers and configurations. Configurations depends on the controllers as they are mostly custom resources and must wait for the Helm Chart to 

## Traefik

Traefik is used for the gateway api. Ingress is disabled

## Cert Manager

- Used for TLS certificates
- Let's Encrypt is used as CA
- `letsencrypt-staging` for staging and `letsencrypt-production` foe prodution
