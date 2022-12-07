#!/usr/bin/env bash
set -Ex

if [ -z "$API_PATH" ]; then
  API_PATH="http://localhost:8080/Plone"
fi

if [ -z "$INTERNAL_API_PATH" ]; then
  INTERNAL_API_PATH="http://backend:8080/Plone"
fi

function apply_rebuild {
  mkdir -p /opt/frontend/src/addons
  find /opt/frontend/ -not -user node -exec chown node {} \+
  RAZZLE_API_PATH=VOLTO_API_PATH RAZZLE_INTERNAL_API_PATH=VOLTO_INTERNAL_API_PATH gosu node yarn develop
  RAZZLE_API_PATH=VOLTO_API_PATH RAZZLE_INTERNAL_API_PATH=VOLTO_INTERNAL_API_PATH gosu node yarn
  RAZZLE_API_PATH=VOLTO_API_PATH RAZZLE_INTERNAL_API_PATH=VOLTO_INTERNAL_API_PATH gosu node yarn build
  find /opt/frontend/ -not -user node -exec chown node {} \+
}

function apply_path {
    mainjs=./build/server.js
    bundlejs=./build/public/static/js/*.js
    test -f $mainjs

    echo "Check that we have API_PATH and API vars"
    test -n "$API_PATH"

    echo "Changing built files inplace"
    gosu node sed -i "s#VOLTO_API_PATH#${API_PATH}#g" $mainjs
    gosu node sed -i "s#VOLTO_API_PATH#${API_PATH}#g" $bundlejs
    gosu node sed -i "s#VOLTO_INTERNAL_API_PATH#${INTERNAL_API_PATH}#g" $mainjs
    gosu node sed -i "s#VOLTO_INTERNAL_API_PATH#${INTERNAL_API_PATH}#g" $bundlejs

    echo "Zipping JS Files"
    gosu node gzip -fk $mainjs
}

# Should we re-build
test -n "$REBUILD" && apply_rebuild

# Should we monkey patch?
test -n "$API_PATH" && apply_path

# Sentry
gosu node ./create-sentry-release.sh

echo "Starting Volto"

if [[ "$1" == "yarn"* ]]; then
  exec gosu node "$@"
fi

exec "$@"
