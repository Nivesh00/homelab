import logging, keycloak

from keycloak import KeycloakAdmin
from typing import Any

main_logger = logging.getLogger('main')

def deleteUserIfExists(
    kc_admin: KeycloakAdmin,
    username: str = None,
    user_id: str = None
    ) -> None:
    """
    Look for a user and delete it if it exists
    :param kc-admin: Keycloak admin client
    :param username: username of the user
    :param user_id: id of the user
    """

    if user_id == None:
        user_id = kc_admin.get_user_id(username)
    
    try:
        user = kc_admin.get_user(user_id)
    except keycloak.KeycloakGetError as e:
        main_logger.info("User does not exist, skipping delete")
        return

    kc_admin.delete_user(user_id)

    main_logger.info("Successfully deleted user")
    
    return

def createAdminIfNotExists(
    kc_admin: KeycloakAdmin,
    username: str,
    password: str,
    create_realm: bool = False
    ) -> None:
    """
    Create user, set password and assign realm roles if user does not already exists, otherwise return without doing anything
    :param kc_admin: Keycloak admin client
    :param username: username of the new user
    :param password: password of the new user
    :param create_realm: True if user should be able to create realm
    """

    # Get all real roles and look for admin and create-realm
    admin_realm_roles_list: list[dict] = []
    realm_roles_list: list[dict] = kc_admin.get_realm_roles(brief_representation=False)

    # Create list of realm roles
    for realm_role in realm_roles_list:
        realm_role_name: str = realm_role['name']
        if realm_role_name == 'admin':
            admin_realm_roles_list.append(realm_role)
        if realm_role_name == 'create-realm' and create_realm:
            admin_realm_roles_list.append(realm_role)

    try:
        # Create user
        user_id: str = kc_admin.create_user(
            payload = {
                'username': username,
                'enabled': True,
                'emailVerified': True,
            },
            exist_ok = False
        )
        main_logger.info(f'User successfully created')

        # Set user password
        kc_admin.set_user_password(user_id, password, temporary=False)
        main_logger.info(f'User password successfully set')

        # Assign realm roles
        kc_admin.assign_realm_roles(user_id, admin_realm_roles_list)
        main_logger.info(f'Realm roles successfully assigned')

    except keycloak.KeycloakPostError as e:
        main_logger.info(f'User already exists, skipping creating')
        return

    return

def createRealmIfNotExists(
    kc_admin: KeycloakAdmin,
    realm_name: str
    ) -> None:
    """
    Create a realm if it does not already exists
    :param kc_admin: Keycloak admin client
    :param realm_name: Name of the realm to be created
    """
    
    try:
        kc_admin.get_realm(realm_name)
    except keycloak.KeycloakGetError as e:
        main_logger.info("Realm does not exist yet, creating it...")
        pass

    try:
        kc_admin.create_realm(
            {
                'realm': realm_name,
                'displayName': realm_name,
                'enabled': True
            },
        skip_exists = False)
        main_logger.info("Finished creating new realm")
    except keycloak.KeycloakPostError as e:
        main_logger.info("Realm already exists, skipping creating")

    return
