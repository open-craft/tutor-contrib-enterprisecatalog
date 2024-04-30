SECRET_KEY = "{{ ENTERPRISE_CATALOG_SECRET_KEY }}"
ALLOWED_HOSTS = [
    "enterprise-catalog",
    "{{ ENTERPRISE_CATALOG_HOST }}",
    "{{ ENTERPRISE_ACCESS_HOST }}",
    "{{ LMS_HOST }}",
    "{{ LICENSE_MANAGER_HOST }}",
]

PLATFORM_NAME = "{{ PLATFORM_NAME }}"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "{{ ENTERPRISE_CATALOG_MYSQL_DATABASE }}",
        "USER": "{{ ENTERPRISE_CATALOG_MYSQL_USERNAME }}",
        "PASSWORD": "{{ ENTERPRISE_CATALOG_MYSQL_PASSWORD }}",
        "HOST": "{{ MYSQL_HOST }}",
        "PORT": "{{ MYSQL_PORT }}",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "KEY_PREFIX": "enterprise-catalog",
        "LOCATION": "redis://{% if REDIS_USERNAME and REDIS_PASSWORD %}{{ REDIS_USERNAME }}:{{ REDIS_PASSWORD }}{% endif %}@{{ REDIS_HOST }}:{{ REDIS_PORT }}/{{ ENTERPRISE_CATALOG_CACHE_REDIS_DB }}",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "{{ SMTP_HOST }}"
EMAIL_PORT = "{{ SMTP_PORT }}"
EMAIL_HOST_USER = "{{ SMTP_USERNAME }}"
EMAIL_HOST_PASSWORD = "{{ SMTP_PASSWORD }}"
EMAIL_USE_TLS = {{ SMTP_USE_TLS }}


# Get rid of the "local" handler
if "local" in LOGGING["handlers"]:
    LOGGING["handlers"].pop("local")
for logger in LOGGING["loggers"].values():
    if "local" in logger["handlers"]:
        logger["handlers"].remove("local")
# Decrease verbosity of algolia logger
LOGGING["loggers"]["algoliasearch_django"] = {"level": "WARNING"}

OAUTH_API_TIMEOUT = 5
{% set jwt_rsa_key | rsa_import_key %}{{ JWT_RSA_PRIVATE_KEY }}{% endset %}
import json
JWT_AUTH["JWT_ISSUER"] = "{{ JWT_COMMON_ISSUER }}"
JWT_AUTH["JWT_AUDIENCE"] = "{{ JWT_COMMON_AUDIENCE }}"
JWT_AUTH["JWT_SECRET_KEY"] = "{{ JWT_COMMON_SECRET_KEY }}"

JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "{{ jwt_rsa_key.e|long_to_base64 }}",
                "n": "{{ jwt_rsa_key.n|long_to_base64 }}",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "{{ JWT_COMMON_ISSUER }}",
        "AUDIENCE": "{{ JWT_COMMON_AUDIENCE }}",
        "SECRET_KEY": "{{ OPENEDX_SECRET_KEY }}"
    }
]

EDX_DRF_EXTENSIONS = {
    'OAUTH2_USER_INFO_URL': '{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/oauth2/user_info',
}

CELERY_BROKER_TRANSPORT = "redis"
CELERY_BROKER_HOSTNAME ="{{ REDIS_HOST }}:{{ REDIS_PORT }}"
CELERY_BROKER_VHOST = "{{ OPENEDX_CELERY_REDIS_DB }}"
CELERY_BROKER_USER = "{{ REDIS_USERNAME }}"
CELERY_BROKER_PASSWORD = "{{ REDIS_PASSWORD }}"
CELERY_BROKER_URL = "{}://{}:{}@{}/{}".format(
    CELERY_BROKER_TRANSPORT,
    CELERY_BROKER_USER,
    CELERY_BROKER_PASSWORD,
    CELERY_BROKER_HOSTNAME,
    CELERY_BROKER_VHOST
)

{{ patch("enterprise-catalog-common-settings") }}
