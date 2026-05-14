#!/bin/sh
set -e

cd /backend

MANAGE_PY="${DJANGO_MANAGE_PY:-app/manage.py}"

is_enabled() {
  case "$1" in
    1|true|TRUE|yes|YES|on|ON) return 0 ;;
    *) return 1 ;;
  esac
}

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

if [ "$#" -gt 0 ]; then
  exec "$@"
fi

exec python "$MANAGE_PY" runserver 0.0.0.0:8000
