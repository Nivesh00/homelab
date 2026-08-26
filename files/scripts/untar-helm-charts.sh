#!/bin/bash

## Parameter is destination
if [ -z $1 ]; then
    dest="$(pwd)";
else
    dest=$1;
fi

echo "Pulling Helm Charts in directory $dest";

declare -A repo_list=(
    ['cert-manager']='oci://quay.io/jetstack/charts/cert-manager'
    ['kube-prometheus-stack']='oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack'
    ['postgres-operator']='https://opensource.zalando.com/postgres-operator/charts/postgres-operator'
    ['traefik']='oci://ghcr.io/traefik/helm/traefik'
    ['github-runner-controller']='oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller'
    ['github-runner']='oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set'
    ['grafana']='oci://ghcr.io/grafana-community/helm-charts/grafana'
    ['loki']='oci://ghcr.io/grafana-community/helm-charts/loki'
    ['alloy']='https://grafana.github.io/helm-charts'
)

declare -A chart_https_list=(
    ['postgres-operator']=postgres-operator
    ['alloy']='alloy'
)

declare -A version_list=(
    ['cert-manager']='v1.20.2'
    ['kube-prometheus-stack']='86.3.2'
    ['postgres-operator']='v1.15.1'
    ['traefik']='41.0.0'
    ['github-runner-controller']='0.14.2'
    ['github-runner']='0.14.2'
    ['grafana']='13.0.0'
    ['loki']='18.11.3'
    ['alloy']='1.12.0'
)

for app in "${!repo_list[@]}"
do
    echo "App: $app, URL: ${repo_list[$app]}, Version: ${version_list[$app]}"

    chart_repo_url=${repo_list[$app]}
    chart_version=${version_list[$app]}

    # OCI Chart
    if [[ $chart_repo_url == oci* ]]; then
        helm pull $chart_repo_url --version $chart_version --destination $dest/$app-$chart_version --untar
    # HTTPS Chart
    elif [[ $chart_repo_url == https* ]]; then
        chart_name=${chart_https_list[$app]}
        helm pull $chart_name --repo $chart_repo_url --version $chart_version --destination $dest/$app-$chart_version --untar
    fi
done
