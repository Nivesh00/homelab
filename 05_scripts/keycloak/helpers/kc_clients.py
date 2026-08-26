import os, sys, logging, keycloak, json

from keycloak import KeycloakAdmin
from typing import Any

main_logger = logging.getLogger('main')

def createClientIfNotExists(
    kc_admin: KeycloakAdmin,
    client_representation: dict[str, Any]
) -> None:
    """
    Create a client if it does not already exists
    :param kc_admin: Keycloak client admin
    :param client_representation: Representation of client in JSON form (as a dict)
    """
    try:
        kc_admin.create_client(
            payload=client_representation,
            skip_exists=False
        )
    except keycloak.KeycloakPostError as e:
        error_message: dict[str, str] = json.loads(e.error_message.decode())
        main_logger.info(f"{error_message['errorMessage']}, skipping creation")
        return

    main_logger.info("Successfully created client")

    return

def createClientRoleIfNotExists(
    kc_admin: KeycloakAdmin,
    kc_client_id: str,
    role_representation: dict[str, str]
) -> None:
    """
    :param kc_admin: Keycloak admin client
    :param kc_client_id: Client id of client, fo which role should be created
    :param role_representation: The role representation for the role which is being created
    """
    try:
        client_role_id = kc_admin.get_client_id(kc_client_id)
        if client_role_id is None or client_role_id == "": raise keycloak.KeycloakGetError
    except keycloak.KeycloakGetError as e:
        main_logger.error(f"Could not get client internal id for client {kc_client_id}")
        return

    try:
        kc_admin.create_client_role(
            client_role_id=client_role_id,
            payload=role_representation,
            skip_exists=False
        )
    except keycloak.KeycloakPostError as e:
        error_message: dict[str, str] = json.loads(e.error_message.decode())
        main_logger.info(f"{error_message['errorMessage']}, skipping creation")
        return

    main_logger.info("Successfully created role")

    return

def formatClients(
    kc_clients: str
) -> dict[str, str]:
    """
    Transform a string of Keycloak clients into a dict
    :param kc_clients: String of Keycloak clients, in the form client_id_1=client_secret_1,client_id_2=client_secret_2,
    """
    clients: dict[str, str] = {}
    clients_list: list[str] = kc_clients.split(",")

    try:
        for client in clients_list:
            [client_id, client_secret] = client.split("=")
            clients[client_id] = client_secret
    except ValueError as e:
        pass

    main_logger.info("Finished formatting clients into dictionary")

    return clients

def createClientsAndRoles(
    kc_admin: KeycloakAdmin,
    domain: str,
    kc_clients: dict[str, str],
    clients_dir: str,
    roles_dir: str
) -> None:
    """
    Create all clients and roles found in the directories mentioned
    :param kc_admin: Keycloak admin client
    :param domain: Domain of the platform, without scheme or protocol
    :param kc_clients: Dictionary of client ids and secrets
    :param clients_dir: absolute path of directory where clients json files are found
    :param roles_dir: absolute path of directory where roles json files are found
    """

    # Read all clients file
    for root, dirs, files in os.walk(clients_dir):
        for client_file_name in files:
            client_file: str = os.path.join(root, client_file_name)

            main_logger.info(f"Reading client file {client_file_name}")

            current_client_id: str = client_file_name.split(".")[0]
            current_client_secret: str = kc_clients[current_client_id]

            with open(client_file, "r", errors="ignore") as file:
                content: str = file.read()
                client_representation: str = content\
                    .replace("$DOMAIN", domain)\
                    .replace("$KC_CLIENT_SECRET", current_client_secret)

            createClientIfNotExists(
                kc_admin=kc_admin,
                client_representation=json.loads(client_representation)
            )

            # Read role file, it has the same name as the client file
            role_file: str = os.path.join(roles_dir, client_file_name)
            main_logger.info(f"Reading role file {client_file_name}")
            with open(role_file, "r", errors="ignore") as file:
                content: str = file.read()
                roles_list: list[dict] = json.loads(content)

                for role in roles_list:
                    createClientRoleIfNotExists(
                        kc_admin=kc_admin,
                        kc_client_id=current_client_id,
                        role_representation=role
                    )

    main_logger.info("Finished creating all clients and roles")