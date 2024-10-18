import sqlite3
from tenant import TenantData
from contextlib import contextmanager
import logging

class DatabaseManager():
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.create_tenants_table()  # ensures table exists on initialization

    @contextmanager
    def connect_to_db(self):
        '''
        using contextmanager to handle connections to db efficiently
        '''
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
            conn.commit()
            logging.debug('database transaction committed')
        except sqlite3.Error as e:
            conn.rollback()
            logging.error(f"database error occurred: {e}")
        finally:
            conn.close()
            logging.debug("closed database connection")
        
    def create_tenants_table(self) -> None:
        '''
        creates the tenants table if it doesnt already exist
        '''
        try:
            with self.connect_to_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tenants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT,
                    email TEXT,
                    phone_number TEXT,
                    property_management_company TEXT
                    )
                ''')
            logging.info('created tenants table successfully')
        except sqlite3.Error as e:
            logging.error(f"failed creating tenants table: {e}")

    def save_tenant_data_to_db(self, tenant_data: TenantData) -> None:
        '''
        inserts tenant data into the database
        '''
        try:
            with self.connect_to_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO tenants (address, email, phone_number, property_management_company)
                    VALUES (?, ?, ?, ?)
                ''', (
                    tenant_data.get('address'),
                    tenant_data.get('email'),
                    tenant_data.get('phone_number'),
                    tenant_data.get('property_management_company')
                ))
            logging.info('saved tenant data successfully')
        except sqlite3.Error as e:
            logging.error(f"failed to save tenant data: {e}")

if __name__ == '__main__':
    db_manager = DatabaseManager('tenants_portal.db')
    with db_manager.connect_to_db() as conn:
        cursor = conn.cursor()
    # print(conn)
    # cursor.execute("DROP TABLE tenants")
    
    # cursor.execute('''
    #                     CREATE TABLE IF NOT EXISTS tenants (
    #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                     address TEXT,
    #                     email TEXT,
    #                     phone_number TEXT,
    #                     property_management_company TEXT
    #                     )
    #                     ''')
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        cursor.execute('SELECT * FROM tenants')

        tables = cursor.fetchall()
        print(tables)