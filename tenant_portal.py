from abc import ABC, abstractmethod
from typing import TypedDict
from tenant import Tenant

class TenantPortal(ABC):

    @abstractmethod
    def get_tenant_data(self, username: str, password: str) -> Tenant:
        '''
        
        
        '''
        pass

