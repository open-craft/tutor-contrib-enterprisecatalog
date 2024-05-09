# syntax=docker/dockerfile:1.4
###### Minimal image with base system requirements for most stages
FROM docker.io/ubuntu:20.04 as minimal

ENV DEBIAN_FRONTEND=noninteractive
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y curl git-core language-pack-en python3 python3-pip python3-venv \
    build-essential libcairo2 libffi-dev libmysqlclient-dev libxml2-dev libxslt-dev libjpeg-dev libssl-dev \
    pkg-config
ENV LC_ALL en_US.UTF-8

ARG APP_USER_ID=1000
RUN if [ "$APP_USER_ID" = 0 ]; then echo "app user may not be root" && false; fi
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

###### Git-clone enterprise-subsidy repo
ARG ENTERPRISE_SUBSIDY_REPOSITORY='{{ ENTERPRISE_SUBSIDY_REPOSITORY }}'
ARG ENTERPRISE_SUBSIDY_VERSION='{{ ENTERPRISE_SUBSIDY_REPOSITORY_VERSION }}'
RUN mkdir -p /openedx/enterprise-subsidy && \
    git clone $ENTERPRISE_SUBSIDY_REPOSITORY --branch $ENTERPRISE_SUBSIDY_VERSION --depth 1 /openedx/enterprise-subsidy
WORKDIR /openedx/enterprise-subsidy

# Setup empty yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV ENTERPRISE_SUBSIDY_CFG /openedx/config.yml

# Install python venv
RUN python3 -m venv ../venv/
ENV PATH="/openedx/venv/bin:$PATH"

RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install \
    # https://pypi.org/project/setuptools/
    # https://pypi.org/project/pip/
    # https://pypi.org/project/wheel/
    setuptools==67.7.2 pip==23.1.2. wheel==0.40.0

# Install python requirements
# This is identical to "make production-requirements" but it was split in multiple
# instructions to benefit from docker image caching
# Install base requirements
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install -r requirements.txt
{% for extra_requirement in ENTERPRISE_SUBSIDY_EXTRA_PIP_REQUIREMENTS %}RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install '{{ extra_requirement }}'
{% endfor %}

# Install extra requirements
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install \
    # Use redis as a django cache https://pypi.org/project/django-redis/
    django-redis==5.2.0

FROM minimal AS enterprise-subsidy

# Install uwsgi
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install \
    # uwsgi server https://pypi.org/project/uWSGI/
    uwsgi==2.0.21


{{ patch("enterprise-subsidy-dockerfile-post-python-requirements") }}

# Collect static assets
COPY --chown=app:app assets.py ./enterprise_subsidy/settings/assets.py
RUN DJANGO_SETTINGS_MODULE=enterprise_subsidy.settings.assets make static

# Run production server
ENV DJANGO_SETTINGS_MODULE enterprise_subsidy.settings.tutor.production
EXPOSE 8000
CMD uwsgi \
    --static-map /static=/openedx/enterprise-subsidy/enterprise_subsidy/assets \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=2 \
    --buffer-size=8192 \
    --wsgi-file enterprise_subsidy/wsgi.py
