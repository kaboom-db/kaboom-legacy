# Not needed if you don't use PGSQL
export KABOOM_DB_NAME=''
export KABOOM_DB_USER=''
export KABOOM_DB_PASS=''
export KABOOM_DB_HOST=''
export KABOOM_DB_PORT=''

# Django Secret Key. This needs to be generated on first setup.
export KABOOM_DJ_SECRET_KEY='<secret_key>'

# Needed if you want to use AWS S3 for file uploads
export KABOOM_AWS_ACCESS_KEY=''
export KABOOM_AWS_SECRET_ACCESS_KEY=''
export KABOOM_AWS_BUCKET_NAME=''
export KABOOM_AWS_S3_SIGNATURE_VERSION='s3v4'
export KABOOM_AWS_S3_REGION_NAME=''
export KABOOM_AWS_S3_FILE_OVERWRITE=False
export KABOOM_AWS_DEFAULT_ACL=None
export KABOOM_AWS_S3_VERIFY=True
export KABOOM_AWS_QUERYSTRING_AUTH=False

# Needed if you want to send emails via SendGrid
export KABOOM_SENDGRID_APIKEY=''
export KABOOM_EMAIL_HOST='smtp.sendgrid.net'
export KABOOM_EMAIL_HOST_USER=''
export KABOOM_EMAIL_PORT=587
# If using SendGrid, this email needs to have permissions in your SendGrid account.
export KABOOM_DEFAULT_FROM_EMAIL=''