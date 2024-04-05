{% if is_buildkit_enabled() %}# syntax=docker/dockerfile:1.4{% endif %}
###### Minimal image with base system requirements for most stages
FROM docker.io/ubuntu:20.04 as minimal

ENV DEBIAN_FRONTEND=noninteractive
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked{% endif %} \
    apt update && \
    apt install -y curl git-core language-pack-en python3 python3-pip python3-venv \
    build-essential libcairo2 libffi-dev libmysqlclient-dev libxml2-dev libxslt-dev libjpeg-dev libssl-dev
ENV LC_ALL en_US.UTF-8

ARG APP_USER_ID=1000
RUN if [ "$APP_USER_ID" = 0 ]; then echo "app user may not be root" && false; fi
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

###### Git-clone enterprise-access repo
ARG ENTERPRISE_ACCESS_REPOSITORY='{{ ENTERPRISE_ACCESS_REPOSITORY }}'
ARG ENTERPRISE_ACCESS_VERSION='{{ ENTERPRISE_ACCESS_REPOSITORY_VERSION }}'
RUN mkdir -p /openedx/enterprise-access && \
    git clone $ENTERPRISE_ACCESS_REPOSITORY --branch $ENTERPRISE_ACCESS_VERSION --depth 1 /openedx/enterprise-access
WORKDIR /openedx/enterprise-access

# Setup empty yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV ENTERPRISE_ACCESS_CFG /openedx/config.yml

# Install python venv
RUN python3 -m venv ../venv/
ENV PATH="/openedx/venv/bin:$PATH"

RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install \
    # https://pypi.org/project/setuptools/
    # https://pypi.org/project/pip/
    # https://pypi.org/project/wheel/
    setuptools==67.7.2 pip==23.1.2. wheel==0.40.0

# Install python requirements
# This is identical to "make production-requirements" but it was split in multiple
# instructions to benefit from docker image caching
# Install base requirements
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install -r requirements.txt
{% for extra_requirement in ENTERPRISE_ACCESS_EXTRA_PIP_REQUIREMENTS %}RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install '{{ extra_requirement }}'
{% endfor %}

# Install extra requirements
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install \
    # Use redis as a django cache https://pypi.org/project/django-redis/
    django-redis==5.2.0

FROM minimal AS enterprise-access-worker-dev

{{ patch("enterprise-access-worker-dockerfile-post-python-requirements") }}

ENV DJANGO_SETTINGS_MODULE enterprise_access.settings.tutor.celery_production
CMD celery --app=enterprise_access.celery:app worker -Q enterprise_access.default --loglevel=info

FROM minimal AS enterprise-access

# Install uwsgi
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install \
    # uwsgi server https://pypi.org/project/uWSGI/
    uwsgi==2.0.21


{{ patch("enterprise-access-dockerfile-post-python-requirements") }}

# Collect static assets
COPY --chown=app:app assets.py ./enterprise_access/settings/assets.py
RUN DJANGO_SETTINGS_MODULE=enterprise_access.settings.assets make static

# Run production server
ENV DJANGO_SETTINGS_MODULE enterprise_access.settings.tutor.production
EXPOSE 8000
CMD uwsgi \
    --static-map /static=/openedx/enterprise-access/enterprise_access/assets \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=2 \
    --buffer-size=8192 \
    --wsgi-file enterprise_access/wsgi.py
