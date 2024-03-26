from ..production import *

{% include "enterprisecatalog/apps/settings/partials/common.py" %}

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ ENTERPRISE_CATALOG_OAUTH2_KEY }}"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "{{ ENTERPRISE_CATALOG_OAUTH2_SECRET }}"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://lms:8000/oauth2"

SOCIAL_AUTH_EDX_OAUTH2_KEY = "{{ ENTERPRISE_CATALOG_OAUTH2_KEY_SSO }}"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "{{ ENTERPRISE_CATALOG_OAUTH2_SECRET_SSO }}"
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = SOCIAL_AUTH_EDX_OAUTH2_ISSUER + "/logout"

SOCIAL_AUTH_REDIRECT_IS_HTTPS = {% if ENABLE_HTTPS %}True{% else %}False{% endif %}

LMS_BASE_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"
DISCOVERY_SERVICE_API_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ DISCOVERY_HOST }}/api/v1/"
ECOMMERCE_BASE_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ ECOMMERCE_HOST }}"
ENTERPRISE_LEARNER_PORTAL_BASE_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ MFE_HOST }}/learner-portal-enterprise"

{{ patch("enterprise-catalog-production-settings") }}
