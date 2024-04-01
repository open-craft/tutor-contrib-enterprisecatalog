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

catalog_config = {
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
    # Include information to be used by loop below
    "repo_name": "enterprise-catalog",
    "app_name": "enterprise-catalog",
    "init_tasks": ("mysql", "lms", "enterprise-catalog"),
    "templates_dir": "enterprisecatalog",
}

license_manager_config = {
    "unique": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 24|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}open-craft/openedx-license-manager:{{ LICENSE_MANAGER_VERSION }}",
        "WORKER_DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}open-craft/openedx-license-manager-worker:{{ LICENSE_MANAGER_VERSION }}",
        "BULK_ENROLLMENT_WORKER_DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}open-craft/openedx-license-manager-bulk-enrollment-worker:{{ LICENSE_MANAGER_VERSION }}",
        "HOST": "license-manager.{{ LMS_HOST }}",
        "EXTRA_PIP_REQUIREMENTS": [],
        "MYSQL_DATABASE": "licensemanager",
        "MYSQL_USERNAME": "licensemanager",
        "OAUTH2_KEY": "license-manager",
        "OAUTH2_KEY_DEV": "license-manager-dev",
        "OAUTH2_KEY_SSO": "license-manager-sso",
        "OAUTH2_KEY_SSO_DEV": "license-manager-sso-dev",
        "CACHE_REDIS_DB": "{{ OPENEDX_CACHE_REDIS_DB }}",
        "REPOSITORY": "https://github.com/openedx/license-manager.git",
        "REPOSITORY_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
    },
    # Include information to be used by loop below
    "repo_name": "license-manager",
    "app_name": "license-manager",
    "init_tasks": ("mysql", "lms", "license-manager"),
    "templates_dir": "licensemanager",
}

access_config = {
    "unique": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 24|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}open-craft/openedx-enterprise-access:{{ ENTERPRISE_ACCESS_VERSION }}",
        "WORKER_DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}open-craft/openedx-enterprise-access-worker:{{ ENTERPRISE_ACCESS_VERSION }}",
        "HOST": "enterprise-access.{{ LMS_HOST }}",
        "EXTRA_PIP_REQUIREMENTS": [],
        "MYSQL_DATABASE": "enterpriseaccess",
        "MYSQL_USERNAME": "enterpriseaccess",
        "OAUTH2_KEY": "enterprise-access",
        "OAUTH2_KEY_DEV": "enterprise-access-dev",
        "OAUTH2_KEY_SSO": "enterprise-access-sso",
        "OAUTH2_KEY_SSO_DEV": "enterprise-access-sso-dev",
        "CACHE_REDIS_DB": "{{ OPENEDX_CACHE_REDIS_DB }}",
        "REPOSITORY": "https://github.com/openedx/enterprise-access.git",
        "REPOSITORY_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
    },
    # Include information to be used by loop below
    "repo_name": "enterprise-access",
    "app_name": "enterprise-access",
    "init_tasks": ("mysql", "lms", "enterprise-access"),
    "templates_dir": "enterpriseaccess",
}

subsidy_config = {
    "unique": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 24|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}open-craft/openedx-enterprise-subsidy:{{ ENTERPRISE_SUBSIDY_VERSION }}",
        "HOST": "enterprise-subsidy.{{ LMS_HOST }}",
        "EXTRA_PIP_REQUIREMENTS": [],
        "MYSQL_DATABASE": "enterprisesubsidy",
        "MYSQL_USERNAME": "enterprisesubsidy",
        "OAUTH2_KEY": "enterprise-subsidy",
        "OAUTH2_KEY_DEV": "enterprise-subsidy-dev",
        "OAUTH2_KEY_SSO": "enterprise-subsidy-sso",
        "OAUTH2_KEY_SSO_DEV": "enterprise-subsidy-sso-dev",
        "CACHE_REDIS_DB": "{{ OPENEDX_CACHE_REDIS_DB }}",
        "REPOSITORY": "https://github.com/openedx/enterprise-subsidy.git",
        "REPOSITORY_VERSION": "main",
    },
    # Include information to be used by loop below
    "repo_name": "enterprise-subsidy",
    "app_name": "enterprise-subsidy",
    "init_tasks": ("mysql", "lms", "enterprise-subsidy"),
    "templates_dir": "enterprisesubsidy",
}

# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorenterprisecatalog", "templates")
)

configurations = [
    ("ENTERPRISE_CATALOG_", catalog_config),
    ("LICENSE_MANAGER_", license_manager_config),
    ("ENTERPRISE_ACCESS_", access_config),
    ("ENTERPRISE_SUBSIDY_", subsidy_config),
]

for prefix, config in configurations:
    # Add configuration entries
    tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
        [(f"{prefix}{key}", value) for key, value in config.get("defaults", {}).items()]
    )
    tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
        [(f"{prefix}{key}", value) for key, value in config.get("unique", {}).items()]
    )
    tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(list(config.get("overrides", {}).items()))

    # Render the "build" and "apps" folders
    tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
        [
            (f"{config['templates_dir']}/build", "plugins"),
            (f"{config['templates_dir']}/apps", "plugins"),
        ],
    )

    # Initialization tasks
    for service in config["init_tasks"]:
        with open(
            os.path.join(
                pkg_resources.resource_filename("tutorenterprisecatalog", "templates"),
                config["templates_dir"],
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


# Automount /openedx/enterprise-catalog folder from the container
@tutor_hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_repositories(mounts: list[tuple[str, str]], name: str) -> list[tuple[str, str]]:
    repos = {config["repo_name"]: config["app_name"] for _, config in configurations}
    if name in repos:
        mounts.append((repos[name], f"/openedx/{name}"))
    return mounts


# Bind-mount repo at build-time, both for prod and dev images
@tutor_hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _mount_repositories_on_build(
    mounts: list[tuple[str, str]], host_path: str
) -> list[tuple[str, str]]:
    repos = {config["repo_name"]: config["app_name"] for _, config in configurations}
    path_basename = os.path.basename(host_path)
    if path_basename in repos:
        mounts.append((repos[path_basename], f"{repos[path_basename]}-src"))
        mounts.append((f"{repos[path_basename]}-dev", f"{repos[path_basename]}-src"))
    return mounts


@tutor_hooks.Filters.APP_PUBLIC_HOSTS.add()
def _print_apps_public_hosts(
    hosts: list[str], context_name: t.Literal["local", "dev"]
) -> list[str]:
    if context_name == "dev":
        hosts += [
            "{{ ENTERPRISE_CATALOG_HOST }}:8160",
            "{{ LICENSE_MANAGER_HOST }}:8170",
            "{{ ENTERPRISE_ACCESS_HOST }}:8270",
            "{{ ENTERPRISE_SUBSIDY_HOST }}:8280",
        ]
    else:
        hosts += [
            "{{ ENTERPRISE_CATALOG_HOST }}",
            "{{ LICENSE_MANAGER_HOST }}",
            "{{ ENTERPRISE_ACCESS_HOST }}",
            "{{ ENTERPRISE_SUBSIDY_HOST }}",
        ]
    return hosts


# Image management
tutor_hooks.Filters.IMAGES_BUILD.add_items(
    [
        # Enterprise catalog images
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
        # License manager images
        (
            "license-manager-worker",
            ("plugins", "licensemanager", "build", "licensemanager"),
            "{{ LICENSE_MANAGER_WORKER_DOCKER_IMAGE }}",
            ("--target=license-manager-worker-dev",),
        ),
        (
            "license-manager-bulk-enrollment-worker",
            ("plugins", "licensemanager", "build", "licensemanager"),
            "{{ LICENSE_MANAGER_BULK_ENROLLMENT_WORKER_DOCKER_IMAGE }}",
            ("--target=license-manager-bulk-enrollment-worker-dev",),
        ),
        (
            "license-manager",
            ("plugins", "licensemanager", "build", "licensemanager"),
            "{{ LICENSE_MANAGER_DOCKER_IMAGE }}",
            (),
        ),
        # Enterprise access images
        (
            "enterprise-access-worker",
            ("plugins", "enterpriseaccess", "build", "enterpriseaccess"),
            "{{ ENTERPRISE_ACCESS_WORKER_DOCKER_IMAGE }}",
            ("--target=enterprise-access-worker-dev",),
        ),
        (
            "enterprise-access",
            ("plugins", "enterpriseaccess", "build", "enterpriseaccess"),
            "{{ ENTERPRISE_ACCESS_DOCKER_IMAGE }}",
            (),
        ),
        # Enterprise subsidy image
        (
            "enterprise-subsidy",
            ("plugins", "enterprisesubsidy", "build", "enterprisesubsidy"),
            "{{ ENTERPRISE_SUBSIDY_DOCKER_IMAGE }}",
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
        ),
        (
            "license-manager",
            "{{ LICENSE_MANAGER_DOCKER_IMAGE }}",
        ),
        (
            "license-manager-worker",
            "{{ LICENSE_MANAGER_WORKER_DOCKER_IMAGE }}",
        ),
        (
            "license-manager-bulk-enrollment-worker",
            "{{ LICENSE_MANAGER_BULK_ENROLLMENT_WORKER_DOCKER_IMAGE }}",
        ),
        (
            "enterprise-access",
            "{{ ENTERPRISE_ACCESS_DOCKER_IMAGE }}",
        ),
        (
            "enterprise-access-worker",
            "{{ ENTERPRISE_ACCESS_WORKER_DOCKER_IMAGE }}",
        ),
        (
            "enterprise-subsidy",
            "{{ ENTERPRISE_SUBSIDY_DOCKER_IMAGE }}",
        ),
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
        ),
        (
            "license-manager",
            "{{ LICENSE_MANAGER_DOCKER_IMAGE }}",
        ),
        (
            "license-manager-worker",
            "{{ LICENSE_MANAGER_WORKER_DOCKER_IMAGE }}",
        ),
        (
            "license-manager-bulk-enrollment-worker",
            "{{ LICENSE_MANAGER_BULK_ENROLLMENT_WORKER_DOCKER_IMAGE }}",
        ),
        (
            "enterprise-access",
            "{{ ENTERPRISE_ACCESS_DOCKER_IMAGE }}",
        ),
        (
            "enterprise-access-worker",
            "{{ ENTERPRISE_ACCESS_WORKER_DOCKER_IMAGE }}",
        ),
        (
            "enterprise-subsidy",
            "{{ ENTERPRISE_SUBSIDY_DOCKER_IMAGE }}",
        ),
    ]
)

MFES = {
    "learner-portal-enterprise": {
        "repository": "https://github.com/openedx/frontend-app-learner-portal-enterprise.git",
        "port": 8734,
        "version": "master",
    },
    # npm install fails due to corrupted file dependency
    # https://github.com/openedx/frontend-app-admin-portal/blob/7e36288a6a6a26d74ac96cf4b11b92d2238fc3e3/package.json#L49
    # "admin-portal-enterprise": {
    #     "repository": "https://github.com/openedx/frontend-app-admin-portal.git",
    #     "port": 1991,
    #     "version": "master",
    # },
}


@MFE_APPS.add()
def _add_enterprise_catalog_mfe_apps(apps: dict[str, MFE_ATTRS_TYPE]) -> dict[str, MFE_ATTRS_TYPE]:
    apps.update(MFES)
    return apps


for mfe_name in MFES:
    tag = "{{ DOCKER_REGISTRY }}open-craft/openedx-" + mfe_name + "-dev:{{ MFE_VERSION }}"
    tutor_hooks.Filters.IMAGES_BUILD.add_item(
        (
            f"{mfe_name}-dev",
            ("plugins", "mfe", "build", "mfe"),
            tag,
            (f"--target={mfe_name}-dev",),
        )
    )
    tutor_hooks.Filters.IMAGES_PULL.add_item((f"{mfe_name}-dev", tag))
    tutor_hooks.Filters.IMAGES_PUSH.add_item((f"{mfe_name}-dev", tag))


# Load patches from files
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorenterprisecatalog", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
