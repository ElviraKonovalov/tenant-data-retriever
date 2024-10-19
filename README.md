# tenant-data-retriever
A python application to interact with different tenant portals, retrieve tenant data and store the data in a local SQLite database.

## Usage
To retrieve teannt data, use the following command:  
```python3 tenant_portal_data_retriever.py <tenant_portal> <username> <password>```  
Example:  
```python3 tenant_portal_data_retriever.py 'click_pay' your_email@gmail.com your_password```  

## Configuration
You may need to add your tenant portals and implement new subclasses of `TenantPortal` to handle their specific logic.
Modify the `TENANT_PORTAL_CLASSES` dictionary in `tenant_portal_data_retriever.py` to add new tenant portal implementations.

## Supported Tenant Portals
**ClickPay:** A fully implemented example that interacts with the ClickPay portal, handles login, extracts antiforgery tokens, and retrieves tenant data.

## Project Structure
- `tenant_portal_data_retriever.py`: The main script to run the application.  
- `tenant_portal.py`: Abstract base class defining the interface for tenant portals.  
- `click_pay.py`: Implementation of the TenantPortal class for the ClickPay tenant portal.  
- `tenant_database.py`: Manages database operations using SQLite.  
- `tenant.py`: Defines the TenantData structure used for tenant information.  
