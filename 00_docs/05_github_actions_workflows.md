# Github Actions Workflows

Notes about Gihub Actions flows.

Folder `05_scripts` contains scripts for workflows

## Environment Variables

Variables for workflow

| variable key  | variable value  |
|---|---|
| `GH_ACCESS_TOKEN`  | Github classic access token with `delete:packages`, `repo` and `write:packages` access token  |
| `KEYCLOAK_ENV`  | [Keycloak .env file](../05_scripts/keycloak/.env.example)  |
| `KUBERNETES_ENV` | [Kubernetes .env file](../05_scripts/kubernetes/.env.example)

## Actions

- `actions/checkout@v6` - checkout code

- `actions/upload-artifact@v8` - upload artifact to repo

- `actions/download-artifact@v8` - download uploaded artifact

- `actions/cache@v6` - cahce results without uploading

## Scripts

Scripts are found at [05_scripts](../05_scripts/)

### Misc flows

- `.publish-utility-image.yml` - build and push utility tools docker image, usese Github hostes runners
- `.test-workflows.yml` - test workflows for miscellaneous runs

### Keycloak

- `files` - directory
    ```
    └── files
       ├── clients
       └── roles
    ```
    - `clients`: Keycloak client representation in json
    - `roles`: Keycloak role representation in json for clients
    - Note: Both the files in the `clients` dir and `roles` dir must be named after their respective client id (e.g. for client-id `grafana`, client representation is named `client.json` and role representation is named `grafana.json` also )

1. `01_create_user_and_realm.py`: Create the admin user in master realm, and another realm (called the app realm) with its own admin user

1. `02_create_clients_and_roles.py`: Create the clients and roles, and assign the admin client roles to the admin user in the app realm

### Kubernetes

1. `01_wait_for_resource.py`: Wait for a resource to be created

## Notes

- Seting a file as secret does not work as encrytion may be broken


### Github Actions

- `workflow_dispatch` - manually trigger github actions workflow

### Utility docker image

- Docker file at [files/dockerfiles/utility-tools](../files/dockerfiles/utility-tools)

```bash
# ghcr login
echo <token> | docker login ghcr.io --username <user> --password-stdin

# Build and push
docker build --tag ghcr.io/nivesh00/utillity-tools -f utility-tools .
docker push ghcr.io/nivesh00/utillity-tools:latest

# Debug
docker run -it --rm --name utility-tools ghcr.io/nivesh00/utillity-tools:latest
```


### Kubernetes

- Python Client docs https://github.com/kubernetes-client/python/tree/master/kubernetes/docs

### References

- built-in variables: https://docs.github.com/en/actions/reference/workflows-and-actions/variables

- built-in contexts: https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#github-context

- Evaluation: https://docs.github.com/en/actions/reference/workflows-and-actions/expressions

- Best practices: https://github.com/orgs/community/discussions/187543#discussioncomment-15862260