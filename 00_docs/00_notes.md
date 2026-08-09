
# General notes

## SOPS

- Flux SOPS docs: https://fluxcd.io/flux/guides/mozilla-sops/

- List all secrets
    ```sh
    gpg --list-secret-keys
    ```

- Encrypt secret
    ```sh
    # template
    sops --encrypt --encrypted-regex <regex-of-secret-keys> --pgp <PGP-key-id> --in-place /path/to/secret/file.yml
    # example with values
    sops --encrypt --encrypted-regex '^(data|stringData)$' --pgp "87AD5A3C61D4124E53D41EACAB6F74E497AB" --in-place secrets.yml
    ```

## Rotate Token

- Following commands are ran
    ```sh
    # Delete existing secret
    kubectl -n flux-system delete secret flux-system

    # Create new secret
    flux create secret git flux-system --url ssh://git@github.com/Nivesh00/homelab --private-key-file ~/.ssh/homelab_github_ed25519

    # Run bootstrap command again

    flux bootstrap git --url ssh://git@github.com/Nivesh00/homelab --branch main --private-key-file ~/.ssh/homelab_github_ed25519 --path ./02_clusters/homelab
    ```

