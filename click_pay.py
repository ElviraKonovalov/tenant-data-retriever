from tenant_portal import TenantPortal
from tenant import TenantData
import requests
from bs4 import BeautifulSoup
import logging

class ClickPay(TenantPortal):

    def get_tenant_data(self, username: str, password: str) -> TenantData:
        '''
        extracts data directly from the clickPay portal
        '''
        # creates session and log in
        session = self.create_session()
        login_response = self.login(session, username, password)

        # handles redirection and extracts antiforgery token
        redirection_url = self.get_redirection_url(login_response)
        antiforgery_token = self.get_antiforgery_token(session, redirection_url)

        # sets the token in the session headers
        session.headers['Antiforgerytoken'] = antiforgery_token

        # access restricted data for units and profile
        units = self.get_user_units(session)
        profile = self.get_user_profile(session)

        tenant_data = self.extract_tenant_data(units, profile)
        return tenant_data

    def extract_tenant_data(self, units: dict, profile: dict) -> TenantData:
        address = self.format_address(units)
        email = profile.get("Email")
        phone_number = profile.get("Phone")
        property_management_company = units.get("LLCName")

        tenant_data = TenantData(
            address=address,
            email=email,
            phone_number=phone_number,
            property_management_company=property_management_company
        )
        return tenant_data

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
        login_response = session.post(login_url, json=login_data)

        if not login_response.ok:
            logging.error(f"login failed for user: {username}, http status code: {login_response.status_code}")
            raise RuntimeError(f"login failed for user: {username}")

        try:
            result = login_response.json().get("Result", {}).get("Result")
            if result == "Fail":
                logging.error(f"login failed for user: {username}, response indicates failure: {login_response.text}")
                raise RuntimeError(f"login failed for user: {username}, server response indicates failure")
        except ValueError as e:
            logging.error(f"failed to parse login response json for user: {username}. error: {e}")
            raise RuntimeError(f"login response could not be parsed as json for user: {username}")

        logging.info(f"login successful for user: {username}")

        return login_response

    def get_redirection_url(self, login_response: requests.Response) -> str:
        '''extracts the redirection URL from the login response'''
        redirection_url = login_response.json().get("Result", {}).get("RedirectionURL")

        if redirection_url is None:
            logging.error("redirection url is missing")
            raise RuntimeError("redirection url is missing")

        return f"https://www.clickpay.com/{redirection_url}"

    def get_antiforgery_token(self, session: requests.Session, redirection_url: str) -> str:
        '''handles redirection and extracts the antiforgery token from the page'''
        redirect_response = session.get(redirection_url).text
        soup = BeautifulSoup(redirect_response, 'html.parser')
        antiforgery_token = soup.find('input', {'id': "antiForgeryToken"})['value']

        if antiforgery_token is None:
            logging.error("antiforgery token is missing")
            raise RuntimeError("antiforgery token is missing")

        return antiforgery_token

    def get_user_units(self, session: requests.Session) -> dict:
        '''gets the users units data'''
        units = self.get_data(session, request_type="get_user_units", IncludeDisabledInfo=1).get("Units")
        return units
    
    def get_user_profile(self, session: requests.Session) -> dict:
        '''gets the users profile data'''
        profile = self.get_data(session, request_type="get_my_profile")
        return profile

    def get_data(self, session: requests.Session, request_type: str, **extra_params) -> dict:
        '''makes a generalized request to the get data endpoint'''
        get_data_url = "https://www.clickpay.com/MobileService/Service.asmx/get_data_allow_impersonation_json"
        payload = {
            "RequestType": request_type,
        }
        # includes any extra parameters like 'IncludeDisabledInfo'
        payload.update(extra_params)
        data_response = session.post(get_data_url, json=payload)
        return data_response.json().get("Result", {})

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
        '''mock data for step 1'''
        return {
            'address': '4 Privet Drive, Little Whinging, Surrey',
            'email': 'harrypotter@gmail.com',
            'phone_number': '(605) 475-6961',
            'property_management_company': 'Ocean Prime'
        }
