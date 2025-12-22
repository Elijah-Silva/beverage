#!/usr/bin/env bash
set -euo pipefail
exec >> /var/log/beverage/run_all.log 2>&1
trap 'echo -e "Subject: run_all.sh Failed\n\nFailed at line $LINENO\nSee /var/log/beverage/run_all.log for details" | msmtp elijah.silva@icloud.com' ERR

echo "=== $(date) ===" >> /var/log/beverage/run_all.log

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PSQL="psql -d beverage -v ON_ERROR_STOP=1 -q"

echo " -----------------------------------------------------"
echo "|                                                     |"
echo "| 🚀 Rebuilding and seeding database...               |"
echo "|                                                     |"

$PSQL -f "$SQL_DIR/bootstrap/000_create_schemas.sql"

# reference tables
$PSQL -f "$SQL_DIR/ref/000_ref_tables.sql"
$PSQL -f "$SQL_DIR/ref/010_seed_static_lookups.sql"
$PSQL -f "$SQL_DIR/ref/020_seed_country_codes.sql"
$PSQL -f "$SQL_DIR/ref/030_seed_currency_codes.sql"
$PSQL -f "$SQL_DIR/ref/040_seed_processing_methods.sql"
$PSQL -f "$SQL_DIR/ref/050_seed_varietals.sql"

# raw schema tables
$PSQL -f "$SQL_DIR/raw/vendors/000_create_tables.sql"
$PSQL -f "$SQL_DIR/raw/vendors/010_load.sql"
$PSQL -f "$SQL_DIR/raw/locations/000_create_tables.sql"
$PSQL -f "$SQL_DIR/raw/locations/010_load.sql"
$PSQL -f "$SQL_DIR/raw/products/000_create_tables.sql"
$PSQL -f "$SQL_DIR/raw/products/010_load.sql"
$PSQL -f "$SQL_DIR/raw/orders/000_create_tables.sql"
$PSQL -f "$SQL_DIR/raw/orders/010_load.sql"
$PSQL -f "$SQL_DIR/raw/order_items/000_create_tables.sql"
$PSQL -f "$SQL_DIR/raw/order_items/010_load.sql"
$PSQL -f "$SQL_DIR/raw/sessions/000_create_tables.sql"
$PSQL -f "$SQL_DIR/raw/sessions/010_load.sql"
$PSQL -f "$SQL_DIR/raw/extractions/000_create_tables.sql"
$PSQL -f "$SQL_DIR/raw/extractions/010_load.sql"

# data checks
echo "|❔ Checking raw data files..."
$PSQL -f "$SQL_DIR/util/010_dq_raw_review_views.sql"
$PSQL -f "$SQL_DIR/util/040_raw_dq_check.sql"
echo "|"

# stage schema tables
$PSQL -f "$SQL_DIR/stage/vendors/000_create_tables.sql"
$PSQL -f "$SQL_DIR/stage/vendors/010_load_from_raw.sql"
$PSQL -f "$SQL_DIR/stage/locations/000_create_tables.sql"
$PSQL -f "$SQL_DIR/stage/locations/010_load_from_raw.sql"
$PSQL -f "$SQL_DIR/stage/products/000_create_tables.sql"
$PSQL -f "$SQL_DIR/stage/products/010_load_from_raw.sql"
$PSQL -f "$SQL_DIR/stage/orders/000_create_tables.sql"
$PSQL -f "$SQL_DIR/stage/orders/010_load_from_raw.sql"
$PSQL -f "$SQL_DIR/stage/order_items/000_create_tables.sql"
$PSQL -f "$SQL_DIR/stage/order_items/010_load_from_raw.sql"
$PSQL -f "$SQL_DIR/stage/sessions/000_create_tables.sql"
$PSQL -f "$SQL_DIR/stage/sessions/010_load_from_raw.sql"
$PSQL -f "$SQL_DIR/stage/extractions/000_create_tables.sql"
$PSQL -f "$SQL_DIR/stage/extractions/010_load_from_raw.sql"

# core schema tables
$PSQL -f "$SQL_DIR/core/vendors/000_create_tables.sql"
$PSQL -f "$SQL_DIR/core/vendors/010_load_from_stage.sql"
$PSQL -f "$SQL_DIR/core/locations/000_create_tables.sql"
$PSQL -f "$SQL_DIR/core/locations/010_load_from_stage.sql"
$PSQL -f "$SQL_DIR/core/products/000_create_tables.sql"
$PSQL -f "$SQL_DIR/core/products/010_load_from_stage.sql"
$PSQL -f "$SQL_DIR/core/junctions/000_create_tables.sql"
$PSQL -f "$SQL_DIR/core/junctions/010_load_tables.sql"
$PSQL -f "$SQL_DIR/core/orders/000_create_tables.sql"
$PSQL -f "$SQL_DIR/core/orders/010_load_from_stage.sql"
$PSQL -f "$SQL_DIR/core/order_items/000_create_tables.sql"
$PSQL -f "$SQL_DIR/core/order_items/010_load_from_stage.sql"
$PSQL -f "$SQL_DIR/core/sessions/000_create_tables.sql"
$PSQL -f "$SQL_DIR/core/sessions/010_load_from_stage.sql"
$PSQL -f "$SQL_DIR/core/extractions/000_create_tables.sql"
$PSQL -f "$SQL_DIR/core/extractions/010_load_from_stage.sql"
$PSQL -f "$SQL_DIR/core/inventory/000_create_tables.sql"
$PSQL -f "$SQL_DIR/core/inventory/010_load_from_orders.sql"

$PSQL -f "$SQL_DIR/bootstrap/999_grants.sql"

# util tables
$PSQL -f "$SQL_DIR/util/020_fk_review_views.sql"
$PSQL -f "$SQL_DIR/util/030_dq_review_views.sql"
echo "|❔ Checking foreign key integrity..."
$PSQL -f "$SQL_DIR/util/050_check_fq_issues.sql"
echo "|"
echo "|❔ Checking data quality issues..."
$PSQL -f "$SQL_DIR/util/060_check_dq_issues.sql"

# database rebuilt text
echo "|                                                     |"
echo "| 💯 Database rebuilt and seeded successfully.        |"
echo "|                                                     |"
echo " -----------------------------------------------------"
echo ""

$PSQL -f "$SQL_DIR/util/100_inv_view.sql"

# recent session table
echo "----------------------"
echo "-- Recent sessions  --"
echo ""
$PSQL -f "$SQL_DIR/util/110_session_view.sql" | { head -n 2; tail -n 5; }
