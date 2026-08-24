import os, sys, logging

from typing import Any
from kubernetes import client, config

main_logger = logging.getLogger('main')

def waitForPodRunning(
    v1_client: client.CoreV1Api,
    pod_name: str,
    pod_namespace: str
) -> bool :
    """
    Wait for a pod to be ready, timeout occurs after 500 seconds
    :param v1_client: the CoreV1Api client
    :param pod_name: Name of pod
    :param pod_namespace: Namespace of pod
    :returns: Returns True if pod is running, False if not
    """

    # Timeout is 100 sleep count, i.e. 500 seconds for each function
    sleep_max: int = 100
    sleep_sec: int = 5
    sleep_count: int = 0

    while True:

        # Try to get pod, if it does not exist, retry
        try:
            pod: client.V1Pod = v1_client.read_namespaced_pod(
                name=pod_name,
                namespace=pod_namespace
            )
        except client.exceptions.NotFoundException as e:
            if sleep_count == sleep_max:
                main_logger.error("Timeout while waiting for pod creation")
                return False

            main_logger.debug("Pod not yet created")
            time.sleep(sleep_sec)
            sleep_count += 1
            continue

        main_logger.info("Pod is already created")

        sleep_count = 0
        while pod.status.phase.lower() != "running":
            if sleep_count == sleep_max:
                main_logger.error("Timeout while waiting for running status")
                return False

            main_logger.debug("Pod status phase not running, sleeping for 5 seconds...")
            time.sleep(sleep_sec)
            sleep_count += 1
        
        main_logger.info("Pod is in status phase running")
        
        break

    return True

def waitForResourceReady(
    api_client: client.CustomObjectsApi,
    group: str,
    version: str,
    namespace: str,
    plural: str,
    name: str
) -> bool:
    """
    Function waits for a resource to be created (max 300 sec) and checks the 'Ready' status of said resource
    :param api_client: the api kubernetes client being used
    :param group: kubernetes group of the resource
    :param version: kubernetes version of the resource
    :param namespace: namespace of the resource
    :param plural: plural name of resource
    :param name: name of resource
    :returns: True if resource is in state ready, else false for a timeout
    """
    # Timeout is 60 sleep count, i.e. 300 seconds for each function
    sleep_max: int = 60
    sleep_sec: int = 5
    sleep_count: int = 0

    resource_ready: bool = False
    while not resource_ready:

        # Try to get pod, if it does not exist, retry
        try:
            resource_status: object = api_client.get_namespaced_custom_object_status(
                group=group,
                version=version,
                namespace=namespace,
                plural=plural,
                name=name,
            )
        except client.exceptions.NotFoundException as e:
            if sleep_count == sleep_max:
                main_logger.error("Timeout while waiting for pod creation")
                return False

            main_logger.debug(f"Resource not yet created, sleep for {sleep_sec} seconds...")
            time.sleep(sleep_sec)
            sleep_count += 1
            continue

        try:
            conditions_list: list[dict] = resource_status['status']['conditions']

            for condition in conditions_list:
                print(condition)
                
                if condition['type'].lower() != 'ready': continue

                elif condition['status'].lower() != 'true': break

                else:
                    resource_ready = True
                    break

        except KeyError as e:
            main_logger.debug(f"Resource status not yet available, sleep for {sleep_sec} seconds...")
            time.sleep(sleep_sec)
            sleep_count += 1
            continue

    return True
