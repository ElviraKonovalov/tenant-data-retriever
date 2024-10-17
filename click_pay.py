from tenant_portal import TenantPortal
from tenant import Tenant

class ClickPay(TenantPortal):

    def get_tenant_data(self, username: str, password: str) -> Tenant:
        '''
        TODO: write a function to extarct the data directly from the click pay website
        use mock data for now
        '''
        tenant: Tenant = {
            'address': '4 Privet Drive, Little Whinging, Surrey',
            'email': 'harrypotter@gmail.com',
            'phone_number': '(605) 475-6961',
            'property_management_company': 'Ocean Prime'

        }
        return tenant

