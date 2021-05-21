import os


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_IP = os.getenv('POSTGRES_IP')
DATABASE_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db/auth_db'

SECRET_KEY = os.getenv('SECRET_KEY')

# Name of role that is used by services to access internal functions
# JWT token for this role has no expiration time
SUPERUSER_ROLE_NAME = 'super'
