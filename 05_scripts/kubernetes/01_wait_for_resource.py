import os, sys, logging, time
import helpers.k8s_helpers as k8s_helpers, helpers.init as init

from dotenv import load_dotenv
from typing import Any
from kubernetes import client, config

if __name__ == "__main__":
    # Get Flags
    LOG_LEVEL, LOAD_ENV, INCLUSTER, KUBECONFIG = (init.parseFlags()).values()
    init.setupCustomLogger(LOG_LEVEL)
    main_logger = logging.getLogger('main')

    if LOAD_ENV:
        load_dotenv()

    # Env Vars
    RESOURCE_GROUP: str = os.getenv('RESOURCE_GROUP')
    RESOURCE_VERSION: str = os.getenv('RESOURCE_VERSION')
    RESOURCE_NAME: str = os.getenv('RESOURCE_NAME')
    RESOURCE_NAMESPACE: str = os.getenv('RESOURCE_NAMESPACE')
    RESOURCE_PLURAL: str = os.getenv('RESOURCE_PLURAL')

    # If flag is not set or empty
    if (KUBECONFIG == None or KUBECONFIG == '') and LOAD_ENV:
        KUBECONFIG: str = os.getenv('KUBECONFIG')

    if INCLUSTER:
        config.load_incluster_config()
    elif (KUBECONFIG != None and KUBECONFIG != ''):
        config.load_kube_config(
            config_file=KUBECONFIG
        )
    else:
        config.load_kube_config()

    main_logger.info('Finished loading kubeconfig file')

    api_client: client.CustomObjectsApi = client.CustomObjectsApi()

    resource_running: bool = k8s_helpers.waitForResourceReady(
        api_client=api_client,
        group=RESOURCE_GROUP,
        version=RESOURCE_VERSION,
        namespace=RESOURCE_NAMESPACE,
        plural=RESOURCE_PLURAL,
        name=RESOURCE_NAME
    )

    exit_val: int = 0 if resource_running else -1

    sys.exit(exit_val)
