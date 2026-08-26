import os, sys, logging, keycloak
import helpers.init as init
import helpers.kc_realms as kc_realms, helpers.kc_clients as kc_clients

from dotenv import load_dotenv
from typing import Any
from keycloak import KeycloakOpenID, KeycloakOpenIDConnection, KeycloakAdmin

if __name__ == "__main__":

    # Get Flags
    LOG_LEVEL, LOAD_ENV = (init.parseFlags()).values()
    init.setupCustomLogger(LOG_LEVEL)
    main_logger = logging.getLogger('main')

    if LOAD_ENV:
        load_dotenv()

    ## Get envvars
    # Domain
    DOMAIN: str = os.getenv('DOMAIN')
    KC_URL: str = os.getenv('KC_URL')

    # Master Admin User
    KC_ADMIN_REALM: str = os.getenv('KC_ADMIN_REALM')
    KC_ADMIN_USERNAME: str = os.getenv('KC_ADMIN_USERNAME')
    KC_ADMIN_PASSWORD: str = os.getenv('KC_ADMIN_PASSWORD')

    # App Admin User
    KC_APP_REALM: str = os.getenv('KC_APP_REALM')
    KC_APP_ADMIN_USER: str = os.getenv('KC_APP_ADMIN_USER')
    KC_APP_ADMIN_PASSWORD: str = os.getenv('KC_APP_ADMIN_PASSWORD')

    # Clients and secrets
    KC_CLIENTS: str = os.getenv('KC_CLIENTS')

    main_logger.info(f'Finished loading environment variables')

    ##
    # Create connection for master admin user
    kc_conn_app = KeycloakOpenIDConnection(
                            server_url = KC_URL,
                            username = KC_ADMIN_USERNAME,
                            password = KC_ADMIN_PASSWORD,
                            realm_name = KC_APP_REALM,
                            user_realm_name = KC_ADMIN_REALM,
                            client_id = KC_CLIENT_ID,
                            client_secret_key = "",
                            verify = True
                        )
    kc_admin_app = KeycloakAdmin(connection=kc_conn_app)

    ##
    # Get client dir
    current_dir: str = os.path.dirname(os.path.realpath(__file__))
    clients_dir: str = os.path.join(current_dir, "clients")
    roles_dir: str = os.path.join(current_dir, "roles")

    # Get client id and secrets as dict
    kc_clients_dict: dict[str, str] = kc_clients.formatClients(KC_CLIENTS)

    kc_clients.createClientsAndRoles(
        kc_admin=kc_admin_app,
        domain=DOMAIN,
        kc_clients=kc_clients_dict,
        clients_dir=clients_dir,
        roles_dir=roles_dir
    )

    sys.exit()