# enterprise-catalog, license-manager, enterprise-access and enterprise-subsidy plugin for [Tutor](https://docs.tutor.overhang.io)

## Installation

```sh
pip install git+https://github.com/open-craft/tutor-contrib-enterprisecatalog
```

## Usage

Set below variable in `config.yml` if running tutor-nightly as [enterprise-access](https://github.com/openedx/enterprise-access) does not have a `master` branch.
```yaml
ENTERPRISE_ACCESS_REPOSITORY_VERSION: main
```

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

## Troubleshooting

The `tutor-ecommerce` plugin deploys two MFEs, i.e., [frontend-app-ecommerce](https://github.com/openedx/frontend-app-ecommerce.git) & [frontend-app-payment](https://github.com/openedx/frontend-app-payment.git) and the git URL used in the palm version points to `edx` organisation which should be replaced with `openedx`. If you face this error while building images, please replace the `edx` organisation slug with `openedx` as shown [here](https://github.com/overhangio/tutor-ecommerce/commit/0a619ca3701244bd367741aa6459d2cded14a09d).

```log
enterprise-catalog-1  | django.db.utils.OperationalError: (1045, "Access denied for user 'enterprisecatalog'@'172.18.0.21' (using password: YES)")
```
If you see above error while running `tutor dev launch`, try again and it should work. We don't know the root cause of this issue yet.

## Configuration

Below configuration variables are required for this plugin to function.

```yaml
ALGOLIA_APP_ID: **********
ALGOLIA_INDEX_NAME: enterprise-catalog
ALGOLIA_INDEX_NAME_JOBS: ****
ALGOLIA_SEARCH_API_KEY: ********************************
```

While using tutor in development mode, please add LMS_BASE_URL variable with appropriate host and port, for example:

```bash
LMS_BASE_URL: http://local.overhang.io:8000
```

Then rebuild mfe tutor image using `tutor images build mfe` and launch tutor in dev mode using `tutor dev launch`. This is workaround is required until the utility function called [getProxyLoginUrl](https://github.com/openedx/frontend-enterprise/blob/83e8405e8768c8ea5d87dd40164d8266cb4ee7f0/packages/logistration/src/utils.js#L20) from `frontend-app-logistration` component reads `LMS_BASE_URL` from env instead of making use of mfe_config.

## License

This software is licensed under the terms of the AGPLv3.
