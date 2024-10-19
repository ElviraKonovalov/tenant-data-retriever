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

## Running with Docker
You can also run the application using Docker.

### Prerequisites
Docker must be installed on your machine.  

### Building the Docker Image
First, clone the repository and navigate to the project directory:

```
git clone https://github.com/ElviraKonovalov/tenant-data-retriever.git  
cd tenant-data-retriever
```
  
Next, build the Docker image:  
```docker build -t tenant-portal-retriever .```
  
This command will create a Docker image named tenant-portal-retriever.

### Running the Docker Container
To run the Docker container, use the following command:  
`docker run -it tenant-portal-retriever <tenant_portal> <username> <password>`  
  
Replace:  
`<tenant_portal>` with the name of the tenant portal (e.g., click_pay)  
`<username>` with your actual username  
`<password>` with your actual password  
