from abc import ABC, abstractmethod
from tenant import TenantData
import requests

class TenantPortal(ABC):

    @abstractmethod
    def create_session(self) -> requests.Session:
        """
        abstract method to create a session with the tenant portal
        """
        pass

    @abstractmethod
    def login(self, session: requests.Session, username: str, password: str) -> requests.Response:
        """
        abstract method to log in to the tenant portal
        """
        pass

    @abstractmethod
    def get_redirection_url(self, login_response: requests.Response) -> str:
        """
        abstract method to extract the redirection url from the login response
        """
        pass

    @abstractmethod
    def get_antiforgery_token(self, session: requests.Session, redirection_url: str) -> str:
        """
        abstract method to handle redirection and extract the antiforgery token
        """
        pass

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
