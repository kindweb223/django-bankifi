from os import environ

SECRET_KEY = environ.get('SECRET_KEY')

DEBUG =False

#  Set Up Send Grid For Email
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD')
EMAIL = environ.get('EMAIL')
EMAIL_MAIN = EMAIL
DEFAULT_FROM_EMAIL=EMAIL
ADMINS = (
    ('Kenny', EMAIL),
)

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_HOST = environ.get('AWS_S3_HOST')

# Google Maps using easy_maps
EASY_MAPS_GOOGLE_MAPS_API_KEY = environ.get('EASY_MAPS_GOOGLE_MAPS_API_KEY')

# Open Banking Project Sandbox
OAUTH_CLIENT_KEY = environ.get('OAUTH_CLIENT_KEY')
OAUTH_CLIENT_SECRET = environ.get('OAUTH_CLIENT_SECRET')

# RBS Keys
RBS_PRIMARY_SUB_KEY = environ.get('RBS_PRIMARY_SUB_KEY')

# Nordea Keys
NORDEA_CLIENT_KEY = environ.get('NORDEA_CLIENT_KEY')
NORDEA_CLIENT_SECRET = environ.get('NORDEA_CLIENT_SECRET')

# Xero
XERO_CLIENT_KEY = environ.get('XERO_CLIENT_KEY')
XERO_CLIENT_SECRET = environ.get('XERO_CLIENT_SECRET')
