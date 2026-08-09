#!/bin/bash

# Pull all helm charts for debug

if [ -z $1 ]; then
    dest="$(pwd)";
else
    dest=$1;
fi

echo "Pulling Helm Charts in directory $dest";

declare -A repo=(
    ['cert-manager']='oci://quay.io/jetstack/charts/cert-manager'
    ['kube-prometheus-stack']='oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack'
    ['postgres-operator']='https://opensource.zalando.com/postgres-operator/charts/postgres-operator/postgres-operator'
    ['traefik']='oci://ghcr.io/traefik/helm/traefik'
)

declare -A version=(
    ['cert-manager']='v1.20.2'
    ['kube-prometheus-stack']='86.3.2'
    ['postgres-operator']='v1.15.1'
    ['traefik']='41.0.0'
)

for app in "${!repo[@]}"
do
    echo "App: $app, URL: ${repo[$app]}, Version: ${version[$app]}"

    chart_repo_url=${repo[$app]}
    chart_version=${version[$app]}

    # OCI Chart
    if [[ $chart_repo_url == oci* ]]; then
        helm pull $chart_repo_url --version $chart_version --destination $dest/$app-$chart_version --untar
    # HTTPS Chart
    elif [[ $chart_repo_url == https* ]]; then
    fi
done
