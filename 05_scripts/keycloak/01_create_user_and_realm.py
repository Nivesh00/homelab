import os, sys, logging, keycloak
import helpers.init as init
import helpers.kc_realms as kc_realms 

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
    KC_URL: str = os.getenv('KC_URL')

    # Initial username and password
    KC_INITIAL_USERNAME: str = os.getenv('KC_INITIAL_USERNAME')
    KC_INITIAL_PASSWORD: str = os.getenv('KC_INITIAL_PASSWORD')

    # Client
    KC_CLIENT_ID: str = os.getenv('KC_CLIENT_ID')

    # Master Admin User
    KC_ADMIN_REALM: str = os.getenv('KC_ADMIN_REALM')
    KC_ADMIN_USERNAME: str = os.getenv('KC_ADMIN_USERNAME')
    KC_ADMIN_PASSWORD: str = os.getenv('KC_ADMIN_PASSWORD')

    # App Admin User
    KC_APP_REALM: str = os.getenv('KC_APP_REALM')
    KC_APP_ADMIN_USER: str = os.getenv('KC_APP_ADMIN_USER')
    KC_APP_ADMIN_PASSWORD: str = os.getenv('KC_APP_ADMIN_PASSWORD')

    main_logger.info(f'Finished loading environment variables')

    ##
    # Create connection for initial user
    kc_conn_temp = KeycloakOpenIDConnection(
                            server_url = KC_URL,
                            username = KC_INITIAL_USERNAME,
                            password = KC_INITIAL_PASSWORD,
                            realm_name = KC_ADMIN_REALM,
                            client_id = KC_CLIENT_ID,
                            client_secret_key = "",
                            verify = True
                        )
    kc_admin_temp = KeycloakAdmin(connection=kc_conn_temp)

    try:
        # Create Master Admin User
        kc_realms.createAdminIfNotExists(
            kc_admin = kc_admin_temp,
            username = KC_ADMIN_USERNAME,
            password = KC_ADMIN_PASSWORD,
            create_realm = True
        )
    
    except keycloak.KeycloakPostError as e:
        main_logger.info("Initial user does not exist")

    ##
    # Create connection for master admin user
    kc_conn_master = KeycloakOpenIDConnection(
                            server_url = KC_URL,
                            username = KC_ADMIN_USERNAME,
                            password = KC_ADMIN_PASSWORD,
                            realm_name = KC_ADMIN_REALM,
                            client_id = KC_CLIENT_ID,
                            client_secret_key = "",
                            verify = True
                        )
    kc_admin_master = KeycloakAdmin(connection=kc_conn_master)

    # Delete initial kc user
    kc_realms.deleteUserIfExists(kc_admin_master, KC_INITIAL_USERNAME)

    # Create app realm
    kc_realms.createRealmIfNotExists(kc_admin_master, KC_APP_REALM)

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

    # Create app admin user
    kc_realms.createAdminIfNotExists(
        kc_admin = kc_admin_app,
        username = KC_APP_ADMIN_USER,
        password = KC_APP_ADMIN_PASSWORD
    )

    sys.exit()