import os

DB_NAME = os.getenv('FRANK_DB', 'default_db_name')
DB_USER = os.getenv('', 'default_db_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'default_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')

# Example of how to use the configuration


def get_database_connection():
    connection_string = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    return connection_string


# Usage
if __name__ == "__main__":
    print(get_database_connection())
