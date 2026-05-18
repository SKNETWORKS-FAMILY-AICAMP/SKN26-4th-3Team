#!/bin/sh
# @file docker-entrypoint.sh
# @role
# Starts the backend container by running Django setup tasks and launching the development server.

set -e

cd /backend

MANAGE_PY="${DJANGO_MANAGE_PY:-app/manage.py}"

# Treat common truthy strings as enabled so docker-compose environment values
# can switch startup tasks on and off without changing this script.
is_enabled() {
  case "$1" in
    1|true|TRUE|yes|YES|on|ON) return 0 ;;
    *) return 1 ;;
  esac
}

# Fail fast when the database schema is behind the Django models. This catches
# skipped migrations before startup tasks try to read or write missing tables.
verify_db_schema() {
  python "$MANAGE_PY" shell <<'PY'
from django.apps import apps
from django.db import connection

existing_tables = set(connection.introspection.table_names())
managed_tables = {
    model._meta.db_table
    for model in apps.get_models()
    if model._meta.managed
}
missing_tables = sorted(managed_tables - existing_tables)

if missing_tables:
    print("ERROR: Database schema is out of sync with Django models.")
    print("Missing table(s): " + ", ".join(missing_tables))
    print("Run: python app/manage.py migrate --noinput")
    raise SystemExit(1)

print("Database schema check passed.")
PY
}

if [ -n "${BACKEND_STARTUP_DELAY:-}" ] && [ "${BACKEND_STARTUP_DELAY}" != "0" ]; then
  sleep "$BACKEND_STARTUP_DELAY"
fi

# Startup tasks are individually gated for CI, tests, and local debugging. The
# default path keeps the development container self-initializing.
if is_enabled "${BACKEND_RUN_MAKEMIGRATIONS:-true}"; then
  python "$MANAGE_PY" makemigrations perfumes
fi

if is_enabled "${BACKEND_RUN_MIGRATE:-true}"; then
  python "$MANAGE_PY" migrate --noinput
fi

if is_enabled "${BACKEND_VERIFY_DB_SCHEMA:-true}"; then
  verify_db_schema
fi

if is_enabled "${LOAD_PERFUMES_ON_STARTUP:-true}"; then
  python "$MANAGE_PY" load_perfumes
fi

if is_enabled "${PERFUME_IMAGE_SYNC_ON_STARTUP:-true}"; then
  python "$MANAGE_PY" extract_perfume_images
fi

if is_enabled "${PINECONE_INDEX_ON_STARTUP:-true}"; then
  python "$MANAGE_PY" index_to_pinecone --use-local-cache
fi

if [ "$#" -gt 0 ]; then
  exec "$@"
fi

# No explicit command was provided, so run Django's development server.
exec python "$MANAGE_PY" runserver 0.0.0.0:8000

# ----------------------------------------------------------------
# Update History
# 2026-05-18: git diff 기준 @file/@role header, startup task gate/schema check/server 실행 흐름 주석, EOF footer 추가. (worker: @nobrain711)
# 2026-05-15: chore(backend): setup Pinecone infrastructure and update config. (author: @Gloveman)
# 2026-05-13: feat(perfumes): persist perfume image assets. (author: @nobrain711)
# 2026-05-13: fix(django): guard migrate schema drift. (author: @nobrain711)
# ----------------------------------------------------------------

# EOF: docker-entrypoint.sh
