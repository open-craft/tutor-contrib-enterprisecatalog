from ..devstack import *

{% include "licensemanager/apps/settings/partials/common.py" %}

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ LICENSE_MANAGER_OAUTH2_KEY_DEV }}"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "{{ LICENSE_MANAGER_OAUTH2_SECRET }}"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://lms:8000/oauth2"

SOCIAL_AUTH_EDX_OAUTH2_KEY = "{{ LICENSE_MANAGER_OAUTH2_KEY_SSO_DEV }}"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "{{ LICENSE_MANAGER_OAUTH2_SECRET_SSO }}"
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "http://{{ LMS_HOST }}:8000"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = SOCIAL_AUTH_EDX_OAUTH2_ISSUER + "/logout"

LMS_BASE_URL = "http://{{ LMS_HOST }}:8000"
ENTERPRISE_LEARNER_PORTAL_BASE_URL = "http://{{ MFE_HOST }}:8734/learner-portal-enterprise"
ENTERPRISE_CATALOG_URL = "http://{{ ENTERPRISE_CATALOG_HOST }}:8160"

CORS_ORIGIN_WHITELIST = list(CORS_ORIGIN_WHITELIST)
{% for app_name, app in iter_mfes() %}
{% if app_name in ["learner-portal-enterprise", "admin-portal-enterprise"] %}
CORS_ORIGIN_WHITELIST.append("http://{{ MFE_HOST }}:{{ app['port'] }}")
CSRF_TRUSTED_ORIGINS.append("http://{{ MFE_HOST }}:{{ app['port'] }}")
{% endif %}
{% endfor %}

{{ patch("license-manager-development-settings") }}
