#!/bin/bash

set -e

# Get the absolute path for the root folder, so we can call this script from
# anywhere and it will work.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"

set -x

(cd $ROOT_DIR && python -m piccolo_admin.example.app) & (cd $ROOT_DIR/admin_ui && npm run dev)
