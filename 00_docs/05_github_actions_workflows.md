# Github Actions Workflows

Notes about Gihub Actions flows.

Folder `05_scripts` contains scripts for workflows

## Environment Variables

Variables for workflow

| variable key  | variable value  |
|---|---|
| `GH_ACCESS_TOKEN`  | Github classic access token with `delete:packages`, `repo` and `write:packages` access token  |
|   |   |

## Utility docker image

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

## Workflows

- `.publish-utility-image.yml` - build and push utility tools docker image, usese Github hostes runners
- `.test-workflows.yml` - test workflows for miscellaneous runs

## Scripts

Scripts are found at [05_scripts](../05_scripts/)

## Notes

- Seting a file as secret does not work as encrytion may be broken

## References

- built-in variables: https://docs.github.com/en/actions/reference/workflows-and-actions/variables

- built-in contexts: https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#github-context

- Evaluation: https://docs.github.com/en/actions/reference/workflows-and-actions/expressions

- Best practices: https://github.com/orgs/community/discussions/187543#discussioncomment-15862260