from glob import glob
import os
import pkg_resources
import typing as t

from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__
from tutormfe.hooks import MFE_APPS, MFE_ATTRS_TYPE

from .__about__ import __version__

if __version_suffix__:
    __version__ += "-" + __version_suffix__

HERE = os.path.abspath(os.path.dirname(__file__))
REPO_NAME = "enterprise-catalog"
APP_NAME = "enterprise-catalog"
MFE_NAME = "learner-portal-enterprise"

config = {
    "unique": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 24|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "BACKEND_OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}open-craft/openedx-enterprise-catalog:{{ ENTERPRISE_CATALOG_VERSION }}",
        "WORKER_DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}open-craft/openedx-enterprise-catalog-worker:{{ ENTERPRISE_CATALOG_VERSION }}",
        "HOST": "enterprise-catalog.{{ LMS_HOST }}",
        "EXTRA_PIP_REQUIREMENTS": [],
        "MYSQL_DATABASE": "enterprisecatalog",
        "MYSQL_USERNAME": "enterprisecatalog",
        "OAUTH2_KEY": "enterprise-catalog",
        "OAUTH2_KEY_DEV": "enterprise-catalog-dev",
        "OAUTH2_KEY_SSO": "enterprise-catalog-sso",
        "OAUTH2_KEY_SSO_DEV": "enterprise-catalog-sso-dev",
        "BACKEND_OAUTH2_KEY": "enterprise-backend",
        "BACKEND_OAUTH2_KEY_DEV": "enterprise-backend-dev",
        "CACHE_REDIS_DB": "{{ OPENEDX_CACHE_REDIS_DB }}",
        "REPOSITORY": "https://github.com/openedx/enterprise-catalog.git",
        "REPOSITORY_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
        "ALGOLIA_APP_ID": "",
        "ALGOLIA_SEARCH_API_KEY": "",
        "ALGOLIA_INDEX_NAME": "",
        "ALGOLIA_INDEX_NAME_JOBS": "",
    },
}

@MFE_APPS.add()
def _add_enterprise_catalog_mfe_apps(
    apps: dict[str, MFE_ATTRS_TYPE]
) -> dict[str, MFE_ATTRS_TYPE]:
    apps.update(
        {
            MFE_NAME: {
                "repository": "https://github.com/openedx/frontend-app-learner-portal-enterprise.git",
                "port": 8734,
                "version": "master",
            },
        }
    )
    return apps

# Initialization tasks
init_tasks = ("mysql", "lms", "enterprise-catalog")
for service in init_tasks:
    with open(
        os.path.join(
            pkg_resources.resource_filename("tutorenterprisecatalog", "templates"),
            "enterprisecatalog",
            "tasks",
            service,
            "init",
        ),
        encoding="utf8",
    ) as fi:
        tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item(
            (
                service,
                fi.read(),
            )
        )

# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorenterprisecatalog", "templates")
)
# Render the "build" and "apps" folders
tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("enterprisecatalog/build", "plugins"),
        ("enterprisecatalog/apps", "plugins"),
    ],
)

# Image management
tutor_hooks.Filters.IMAGES_BUILD.add_items(
    [
        (
            "enterprise-catalog-worker",
            ("plugins", "enterprisecatalog", "build", "enterprisecatalog"),
            "{{ ENTERPRISE_CATALOG_WORKER_DOCKER_IMAGE }}",
            ("--target=enterprise-catalog-worker-dev",),
        ),
        (
            "enterprise-catalog",
            ("plugins", "enterprisecatalog", "build", "enterprisecatalog"),
            "{{ ENTERPRISE_CATALOG_DOCKER_IMAGE }}",
            (),
        ),
    ]
)
tutor_hooks.Filters.IMAGES_PULL.add_items(
    [
        (
            "enterprise-catalog",
            "{{ ENTERPRISE_CATALOG_DOCKER_IMAGE }}",
        ),
        (
            "enterprise-catalog-worker",
            "{{ ENTERPRISE_CATALOG_WORKER_DOCKER_IMAGE }}",
        )
    ]
)
tutor_hooks.Filters.IMAGES_PUSH.add_items(
    [
        (
            "enterprise-catalog",
            "{{ ENTERPRISE_CATALOG_DOCKER_IMAGE }}",
        ),
        (
            "enterprise-catalog-worker",
            "{{ ENTERPRISE_CATALOG_WORKER_DOCKER_IMAGE }}",
        )
    ]

)

tag = "{{ DOCKER_REGISTRY }}open-craft/openedx-" + MFE_NAME + "-dev:{{ MFE_VERSION }}"
tutor_hooks.Filters.IMAGES_BUILD.add_item(
    (
        f"{MFE_NAME}-dev",
        ("plugins", "mfe", "build", "mfe"),
        tag,
        (f"--target={MFE_NAME}-dev",),
    )
)
tutor_hooks.Filters.IMAGES_PULL.add_item((f"{MFE_NAME}-dev", tag))
tutor_hooks.Filters.IMAGES_PUSH.add_item((f"{MFE_NAME}-dev", tag))

# Automount /openedx/enterprise-catalog folder from the container
@tutor_hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_enterprise_catalog(
    mounts: list[tuple[str, str]], name: str
) -> list[tuple[str, str]]:
    if name == REPO_NAME:
        mounts.append((APP_NAME, "/openedx/enterprise-catalog"))
    return mounts


# Bind-mount repo at build-time, both for prod and dev images
@tutor_hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _mount_enterprise_catalog_on_build(
    mounts: list[tuple[str, str]], host_path: str
) -> list[tuple[str, str]]:
    path_basename = os.path.basename(host_path)
    if path_basename == REPO_NAME:
        mounts.append((APP_NAME, f"{APP_NAME}-src"))
        mounts.append((f"{APP_NAME}-dev", f"{APP_NAME}-src"))
    return mounts

# Load patches from files
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorenterprisecatalog", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )

# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"ENTERPRISE_CATALOG_{key}", value) for key, value in config.get("defaults", {}).items()]
)
tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"ENTERPRISE_CATALOG_{key}", value) for key, value in config.get("unique", {}).items()]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config.get("overrides", {}).items())
)

@tutor_hooks.Filters.APP_PUBLIC_HOSTS.add()
def _print_enterprise_catalog_public_hosts(
    hosts: list[str], context_name: t.Literal["local", "dev"]
) -> list[str]:
    if context_name == "dev":
        hosts += ["{{ ENTERPRISE_CATALOG_HOST }}:8160"]
    else:
        hosts += ["{{ ENTERPRISE_CATALOG_HOST }}"]
    return hosts
