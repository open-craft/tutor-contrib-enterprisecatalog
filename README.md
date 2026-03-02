# enterprise-catalog, license-manager, enterprise-access and enterprise-subsidy plugin for [Tutor](https://docs.tutor.overhang.io)

## Installation

```sh
pip install git+https://github.com/open-craft/tutor-contrib-enterprisecatalog
```

## Usage

```sh
# This plugin depends on discovery, ecommerce and mfe tutor plugins
tutor plugins enable discovery ecommerce mfe enterprise-catalog
# Build required images
tutor images build enterprise-catalog enterprise-catalog-worker license-manager license-manager-worker license-manager-bulk-enrollment-worker enterprise-access enterprise-access-worker enterprise-subsidy mfe
# Finally start tutor using
# Development
tutor dev launch
# Production/local
tutor local launch
```

## Configuration

Below configuration variables are required for this plugin to function.

```yaml
ALGOLIA_APP_ID: **********
ALGOLIA_INDEX_NAME: enterprise-catalog
ALGOLIA_REPLICA_INDEX_NAME: enterprise-catalog-alternate
ALGOLIA_INDEX_NAME_JOBS: ''
ALGOLIA_SEARCH_API_KEY: ********************************
```

### Enterprise Subsidy

 *Enterprise Subsidy* doesn't have release branches. So, the plugin clones from the `main` branch by defaults. For reproducible builds, set the `ENTERPRISE_SUBSIDY_REPOSITORY_COMMIT` to a commit hash.

### Enterprise MFEs

This plugin adds 2 MFEs to the stack:
* [frontend-app-learner-portal-enterprise](https://github.com/openedx/frontend-app-learner-portal-enterprise)
* [frontend-app-admin-portal](https://github.com/openedx/frontend-app-admin-portal)

#### Choosing the right version

These are pinned to specific branches of OpenCraft's forks. They should be replaced with the upstream repo or your own fork. For eg.,

```python
from tutormfe.hooks import MFE_APPS

@MFE_APPS.add()
def _replace_mfes(mfes):
    mfes["enterprise"] = {
        "repository": "https://github.com/openedx/frontend-app-learner-portal-enterprise.git",
        "port": 8734,
        "version": "main"
    }
    mfes["admin-enterprise"] = {
        "repository": "https://github.com/openedx/frontend-app-admin-portal.git",
        "port": 1991,
        "version": "main"
    }
    return mfes
```

#### Customizing the MFE build

These MFEs differ from the others supported by *tutor-mfe* in 2 aspects:

1. The do not support the `frontend-plugin-framework`.
2. They do not support [runtime configuration](https://docs.openedx.org/projects/edx-platform/en/latest/references/docs/lms/djangoapps/mfe_config_api/docs/decisions/0001-mfe-config-api.html) for some aspects of their functionality.

To compensate for these differences the plugin exposes the following values that can be set in `config.yml` of your instance:

* `ENTERPRISE_LEARNER_PORTAL_BUILD_ENV`, `ENTERPRISE_ADMIN_PORTAL_BUILD_ENV` - these can be set to `dev` or `prod` and default to `prod`. So, if you are running the services locally using `tutor dev`, make sure to set these in your `config.yml` file to `dev`.
* `ENTERPRISE_LEARNER_PORTAL_BUILD_ENV_EXTRAS`, `ENTERPRISE_ADMIN_PORTAL_BUILD_ENV_EXTRAS` - these take a dict of values that are typically found in the `.env` files of these MFEs. These must be used to set things like `FEATURE_*` flags.

Set these values in your `config.yml` file, run `tutor config save` and then rebuild mfe tutor image using `tutor images build mfe` for changes to be included in the MFE build. 

#### Example

```yaml
ENTERPRISE_LEARNER_PORTAL_BUILD_ENV: dev
ENTERPRISE_LEARNER_PORTAL_BUILD_ENV_EXTRAS:
  FEATURE_CONTENT_HIGHLIGHTS: false
```

## Developing MFE's using Tutor

> [!NOTE]
> There are 2 MFEs added by this plugin - frontend-app-learner-portal-enterprise, frontend-app-admin-portal.
> They are mapped to the app names `enterprise` and `admin-enterprise` respectively. Replace `<mfe-app>` with
> either of those 2 values in the instructions below.

1. Clone the MFE repo, checkout to your branch and run `npm ci` to have dependencies installed.
2. Add a Tutor mount to the repo in the format `tutor mounts add <mfe-app>:/local/path/frontend-app:/openedx/app`. E.g.,
    ```sh
    tutor mounts add enterprise:/home/user/repos/frontend-app-learner-portal-enterprise:/openedx/app
    ```
3. Update Tutor config `tutor config save`
4. Build the images `tutor images build mfe <mfe-app>-dev`.
5. Restart the services
    ```
    tutor dev stop mfe
    tutor dev start mfe <mfe-app>
    ```
6. Logs can be monitored using `tutor dev logs <mfe-app>`.

## Tutor CLI Commands

The enterprise services use the LMS OAuth for log in. However, the staff and superuser user previleges are not transferred automatically. This limits Django Admin access and requires explicitly marking a user as staff. This can be accomplished by running the `enterprise-make-staff` command provided by the plugin **after** the LMS login by the user.

For the command's exact inputs, run `tutor local do enterprise-make-staff --help`.

## Sample data for testing

For settings up an initial test enterprise with some learners and related data run

```sh
tutor dev exec lms ./manage.py lms seed_enterprise_devstack_data
```

## Service URLs

While developing locally the services can be accessed from the following URLs

* http://discovery.local.openedx.io:8381/
* http://ecommerce.local.openedx.io:8130/courses/
* http://enterprise-catalog.local.openedx.io:8160/login/
* http://enterprise-access.local.openedx.io:8270/login/
* http://enterprise-subsidy.local.openedx.io:8280/login/
* http://license-manager.local.openedx.io:8170/login/
* http://apps.local.openedx.io:8734/enterprise/
* http://apps.local.openedx.io:1991/admin-enterprise/


## License

This software is licensed under the terms of the AGPLv3.
