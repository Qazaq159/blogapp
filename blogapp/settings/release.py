from .base import *


DEBUG = False

CORS_ALLOWED_ORIGINS = [
    'http://info-box.kz',
]


AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = get_env_variable('AWS_S3_ENDPOINT_URL')

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'info-box-storage'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# for static files
STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# for media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
