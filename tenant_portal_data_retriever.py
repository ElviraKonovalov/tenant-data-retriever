import argparse
import logging
from tenant_portal import TenantPortal
from click_pay import ClickPay
from tenant_database import DatabaseManager
from typing import Type, Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TENANT_PORTAL_CLASSES: Dict[str, Type[TenantPortal]] = {
    'click_pay': ClickPay
}
VALID_TENANT_PORTALS = list(TENANT_PORTAL_CLASSES.keys())

def main(tenant_portal_name: str, username: str, password: str) -> None:
    try:
        db_manager = DatabaseManager('tenants_portal.db')
        logging.info("database manager initialized successfully")
    except Exception as e:
        logging.error(f"failed to initialize the database manager: {e}")
        return 
    
    # retrieves tenant data from the specified portal
    try:
        tenant_portal_class: Type[TenantPortal] = TENANT_PORTAL_CLASSES.get(tenant_portal_name)
        if tenant_portal_class is None:
            raise ValueError(f"invalid tenant portal name: {tenant_portal_name}")

        tenant_portal_instance: TenantPortal = tenant_portal_class()
        tenant_data = tenant_portal_instance.get_tenant_data(username, password)
        logging.info("retrieved tenant data successfully")
    except ValueError as e:
        logging.error(f"invalid tenant portal specified: {e}")
        return
    except Exception as e:
        logging.error(f"failed to retrieve tenant data from portal: {e}")
        return

    # saves tenant data to the database
    try:
        db_manager.save_tenant_data_to_db(tenant_data)
        logging.info("tenant data saved successfully")
    except Exception as e:
        logging.error(f"failed to save tenant data to the database: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tenant_portal', type=str, choices=VALID_TENANT_PORTALS, help='the name of the tenant portal. valid options: click_pay')
    parser.add_argument('username', type=str, help='the username to log in to the tenant portal.')
    parser.add_argument('password', type=str, help='the password to log in to the tenant portal.')
    args = parser.parse_args()

    main(args.tenant_portal, args.username, args.password)
    # example usage: python3 tenant_portal_data_retriever.py 'click_pay' 'email' 'password'
