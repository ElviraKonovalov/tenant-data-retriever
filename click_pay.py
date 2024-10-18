from tenant_portal import TenantPortal
from tenant import TenantData
import requests
from bs4 import BeautifulSoup
import logging

class ClickPay(TenantPortal):

    def get_tenant_data(self, username: str, password: str) -> TenantData:
        '''
        TODO: write a function to extarct the data directly from the click pay website
        use mock data for now
        '''
        # step 1: creates a session and log in
        session = self.create_session()
        login_response = self.login(session, username, password)

        if login_response.ok:
            logging.info("logged in successfully!")
            # print("logged in successfully!")

            # step 2: handles redirection and extract antiforgery token
            redirection_url = self.get_redirection_url(login_response)
            antiforgery_token = self.get_antiforgery_token(session, redirection_url)

            # step 3: sets the token in the session headers
            session.headers['Antiforgerytoken'] = antiforgery_token

            # step 4: access protected data for units and profile
            units = self.get_protected_data(session, request_type="get_user_units", IncludeDisabledInfo=1).get("Units")
            profile = self.get_protected_data(session, request_type="get_my_profile")
            print(units)
            # extracts required information
            address = self.format_address(units)
            email = profile.get("Email")
            phone_number = profile.get("Phone")
            property_management_company = units.get("LLCName")
            
            logging.info(f"formatted address: {address}")
            # print(f"formatted address: {address}")
        else:
            logging.info("login failed")
            return None

        # returns tenant data
        tenant = {
            'address': address,
            'email': email,
            'phone_number': phone_number,
            'property_management_company': property_management_company
        }
        print(tenant)
        return tenant

    def create_session(self) -> requests.Session:
        '''creates a session with the appropriate headers'''
        session = requests.Session()
        session.headers['content-type'] = "text/plain; charset=UTF-8"
        return session

    def login(self, session: requests.Session, username: str, password: str) -> requests.Response:
        '''logs into ClickPay using the provided username and password'''
        login_url = "https://www.clickpay.com/MobileService/Service.asmx/login"
        login_data = {
            'username': username,
            'password': password,
            'validateUsername': True
        }
        return session.post(login_url, json=login_data)

    def get_redirection_url(self, login_response: requests.Response) -> str:
        '''extracts the redirection URL from the login response'''
        redirection_url = login_response.json().get("Result", {}).get("RedirectionURL")
        return f"https://www.clickpay.com/{redirection_url}"

    def get_antiforgery_token(self, session: requests.Session, redirection_url: str) -> str:
        '''handles redirection and extracts the antiforgery token from the page'''
        redirect_response = session.get(redirection_url).text
        soup = BeautifulSoup(redirect_response, 'html.parser')
        antiforgery_token = soup.find('input', {'id': "antiForgeryToken"})['value']
        return antiforgery_token

    def get_protected_data(self, session: requests.Session, request_type: str, **extra_params) -> dict:
        '''makes a generalized request to any protected endpoint'''
        protected_url = "https://www.clickpay.com/MobileService/Service.asmx/get_data_allow_impersonation_json"
        payload = {
            "RequestType": request_type,
        }
        # includes any extra parameters like 'IncludeDisabledInfo'
        payload.update(extra_params)
        protected_response = session.post(protected_url, json=payload)
        return protected_response.json().get("Result", {})

    def format_address(self, units: dict) -> str:
        '''formats the tenants address based on the unit data'''
        street_number = units.get("StreetNumber")
        street_name = units.get("StreetName")
        street_type_name = units.get("StreetTypeName")
        apt_number = units.get("AptNumber")
        city = units.get("City")
        zip_code = units.get("Zip")
        state = units.get("State")

        address = (
            f"{street_number} {street_name} {street_type_name}, "
            f"Apt {apt_number}, {city}, {state} {zip_code}"
        )
        return address

    def get_mock_tenant_data(self) -> TenantData:
        return {
            'address': '4 Privet Drive, Little Whinging, Surrey',
            'email': 'harrypotter@gmail.com',
            'phone_number': '(605) 475-6961',
            'property_management_company': 'Ocean Prime'
        }
