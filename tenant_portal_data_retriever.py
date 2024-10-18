
import argparse
import logging
from tenant_portal import TenantPortal
from click_pay import ClickPay
from tenant_database import DatabaseManager
from tenant import TenantData
from typing import Type

def tenant_portal_data_retriever(tenant_portal: str, username: str, password: str) -> None:
    try: 
        tenant_portal_classes: dict[str, Type[TenantPortal]] = {
            'click_pay': ClickPay
        }

        tenant_portal_class: Type[TenantPortal] = tenant_portal_classes.get(tenant_portal)
        tenant_portal: TenantPortal = tenant_portal_class()
        # tenant_portal: TenantPortal = ClickPay()
        tenant_data: TenantData = tenant_portal.get_tenant_data(username, password)
        # print(tenant_data)
        db_manager = DatabaseManager('tenants_portal.db')
        db_manager.save_tenant_data_to_db(tenant_data)
    except Exception as e:
        logging.error(f"could not retrieve data: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tenant_portal', type=str, choices=['click_pay'], help='the name of the tenant portal. Valid options: click_pay, ...')
    parser.add_argument('username', type=str, help='the username to login into the tenant portal')
    parser.add_argument('password', type=str, help='the password to login into the tenant portal')
    args = parser.parse_args()

    tenant_portal_data_retriever(args.tenant_portal, args.username, args.password)
    # python3 tenant_portal_data_retriever.py 'click_pay' 'email' 'password'