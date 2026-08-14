# Github Actions Workflows

Notes about Gihub Actions flows

## Environment Variables

| variable key  | variable value  |
|---|---|
|   |   |

## Utility docker image

```bash
# ghcr login
echo <token> | docker login ghcr.io --username <user> --password-stdin

# Build and push
docker build --tag ghcr.io/nivesh00/utillity-tools -f utility-tools .
docker push ghcr.io/nivesh00/utillity-tools:latest

# Debug
docker run -it --rm --name utility-tools ghcr.io/nivesh00/utillity-tools:latest
```

## References

- built-in variables: https://docs.github.com/en/actions/reference/workflows-and-actions/variables

- built-in contexts: https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#github-context

- Evaluation: https://docs.github.com/en/actions/reference/workflows-and-actions/expressions

- Best practices: https://github.com/orgs/community/discussions/187543#discussioncomment-15862260