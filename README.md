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

They differ from the other MFEs supported by *tutor-mfe* in 2 aspects:

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

## License

This software is licensed under the terms of the AGPLv3.
