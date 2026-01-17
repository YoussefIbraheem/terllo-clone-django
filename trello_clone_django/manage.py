#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def create_database_if_not_exists():
    import MySQLdb
    print("connecting...")
    db = MySQLdb.connect(
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        port=int(os.getenv('DATABASE_PORT', 3306))
    )
    print(f"user {os.getenv('DATABASE_USER')} connected to MySQL server.")
    cursor = db.cursor()
    print(f"Creating database {os.getenv('DATABASE_NAME')} if not exists...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DATABASE_NAME')}")
    cursor.close()
    db.close()
    print("Database checked/created.")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trello_clone_django.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    create_database_if_not_exists()
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
