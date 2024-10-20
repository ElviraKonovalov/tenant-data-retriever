from abc import ABC, abstractmethod
from tenant import TenantData

class TenantPortal(ABC):

    @abstractmethod
    def get_tenant_data(self, username: str, password: str) -> TenantData:
        """
        abstract method to retrieve tenant data
        """
        pass

    @abstractmethod
    def get_mock_tenant_data(self) -> TenantData:
        """
        abstract method to return mock tenant data
        """
        pass
