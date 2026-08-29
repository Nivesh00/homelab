# Application

Contains `01_controllers` and `01_configs`, analog to infrastructure directory. This directory is used for applications (instead of infrastructure things)

## Grafana

A single grafana instance is used for monitoring and every other dashboards

## Jellyfin

Media server

- Bug - Inotify wachers not enough: to fix, run following command on host nodes
    ```bash
    # From https://anatoly.dev/posts/2025/10/k9s-too-many-open-files/#the-fix
    The Fix

    # Create a file /etc/sysctl.d/99-k3s.conf with the following content:

    fs.inotify.max_user_instances=512
    fs.inotify.max_user_watches=524288

    # Apply the changes right away
    sudo sysctl -p /etc/sysctl.d/99-k3s.conf

    # Verify it worked
    sysctl fs.inotify.max_user_instances fs.inotify.max_user_watches

    # Expected results:

    fs.inotify.max_user_instances = 512
    fs.inotify.max_user_watches = 524288

    ```
