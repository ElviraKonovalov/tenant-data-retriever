import sqlite3
from tenant import Tenant
from contextlib import contextmanager
import logging

class DataBaseManager():
    def __init__(self, db_name:str):
        self.db_name = db_name

    @contextmanager
    def connect_to_db(self):
        '''
        using contextmanager to avoid repetitive connections to db
        '''
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
            conn.commit()
            logging.debug('database transaction committed')
        except sqlite3.Error as e:
            conn.rollback()
            logging.error(f"failed connecting to the database: {e}")
            # print(f"failed connecting to the database: {e}")
        finally:
            conn.close()
            logging.debug("closed database connection")
            # print("closed database connection")
        

    def create_tenants_table(self) -> None:
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
            # print(f"failed creating tenants table: {e}")

    def save_tenant_data_to_db(self, tenant_data: Tenant) -> None:
        try:
            self.create_tenants_table() # make sure table exists 
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
            logging.info('saved tenant data to tenants table successfully')
        except sqlite3.Error as e:
            logging.error(f"failed saving tenant data to tenants table: {e}")

if __name__ == '__main__':
    db_manager = DataBaseManager('tenants_portal.db')
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