#!/bin/bash
# https://docs.docker.com/compose/startup-order/

set -e

host="$1"
shift
cmd="$@"

until psql -h "$host" -U "postgres" -c '\l'; do
  >&2 echo "Server is unavailable - sleeping"
  sleep 1
done

>&2 echo "Server is up - executing command"
exec $cmd
