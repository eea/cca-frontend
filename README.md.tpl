# <%= name %>

[![Release](https://img.shields.io/github/v/release/eea/<%= name %>?sort=semver)](https://github.com/eea/<%= name %>/releases)
[![Pipeline](https://ci.eionet.europa.eu/buildStatus/icon?job=volto%2F<%= name %>%2Fmaster&subject=master)](https://ci.eionet.europa.eu/view/Github/job/volto/job/<%= name %>/job/master/lastBuild/display/redirect)
[![Pipeline](https://ci.eionet.europa.eu/buildStatus/icon?job=volto%2F<%= name %>%2Fdevelop&subject=develop)](https://ci.eionet.europa.eu/view/Github/job/volto/job/<%= name %>/job/develop/lastBuild/display/redirect)
[![Release pipeline](https://ci.eionet.europa.eu/buildStatus/icon?job=volto%2F<%= name %>%2F0.0.0&build=last&subject=release%20v0.0.0%20pipeline)](https://ci.eionet.europa.eu/view/Github/job/volto/job/<%= name %>/job/0.0.0/lastBuild/display/redirect/)


## Documentation

A training on how to create your own website using Volto is available as part of the Plone training at [https://training.plone.org/5/volto/index.html](https://training.plone.org/5/volto/index.html).


## Getting started

1. Install `nvm`

        touch ~/.bash_profile
        curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash

        source ~/.bash_profile
        nvm version

1. Install latest `NodeJS 16.x`:

        nvm install 16
        nvm use 16
        node -v
        v16.16.2

1. Install `yarn`

        curl -o- -L https://yarnpkg.com/install.sh | bash
        yarn -v

1. Clone:

        git clone https://github.com/eea/<%= name %>.git
        cd <%= name %>

1. Install

        yarn build

1. Start backend

        docker-compose up -d
        docker-compose logs -f

1. Start frontend

        yarn start:prod

1. See application at http://localhost:3000

## Automated @eeacms dependencies upgrades

All the addon dependencies that are located in the dependencies section of `package.json` file that belong to @eeacms and have a `MAJOR.MINOR.PATCH` version are automatically upgraded on the release of a new version of the addon. This upgrade is done directly on the `develop` branch.

Exceptions from automated upgrades ( see https://docs.npmjs.com/cli/v8/configuring-npm/package-json#dependencies for dependency configuration examples ) :
* All github or local paths
* Any version intervals ( `^version` or `>version` or `MAJOR.MINOR.x` etc )

## Release

See [release](https://github.com/eea/ims-frontend/tree/master/RELEASE.md)

## Production

We use [Docker](https://www.docker.com/), [Rancher](https://rancher.com/) and [Jenkins](https://jenkins.io/) to deploy this application in production.

### Deploy

* Within `Rancher > Catalog > EEA`

### Upgrade

* Within your Rancher environment click on the `Upgrade available` yellow button next to your stack.

* Confirm the upgrade

* Or roll-back if something went wrong and abort the upgrade procedure.
