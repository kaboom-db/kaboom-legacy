# Not needed if you don't use PGSQL
DB_NAME = ''
DB_USER = ''
DB_PASS = ''
DB_HOST = ''
DB_PORT = ''

# Django Secret Key. This needs to be generated on first setup.
DJ_SECRET_KEY = '<secret_key>'

# Needed if you want to use AWS S3 for file uploads
AWS_ACCESS_KEY = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_BUCKET_NAME = ''
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = ''
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
AWS_QUERYSTRING_AUTH = False

# Needed if you want to send emails via SendGrid
SENDGRID_APIKEY = ''
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = '' # In some cases, this may have to be 'apikey'
EMAIL_PORT = 587
# If using SendGrid, this email needs to have permissions in your SendGrid account.
DEFAULT_FROM_EMAIL = ''