SET SEARCH_PATH = util;

-- PSQL Script
SELECT EXISTS(SELECT 1 FROM util.session_batch_fk_review) AS has_fk_sessions_batch_inv_issues \gset
SELECT EXISTS(SELECT 1 FROM util.vendors_fk_review) AS has_fk_vendors_issues \gset
SELECT EXISTS(SELECT 1 FROM util.sessions_fk_review) AS has_fk_sessions_issues \gset
SELECT EXISTS(SELECT 1 FROM util.locations_fk_review) AS has_fk_locations_issues \gset
SELECT EXISTS(SELECT 1 FROM util.extractions_fk_review) AS has_fk_extractions_issues \gset
SELECT EXISTS(SELECT 1 FROM util.products_fk_review) AS has_fk_products_issues \gset
SELECT EXISTS(SELECT 1 FROM util.products_coffee_fk_review) AS has_fk_products_coffee_issues \gset
SELECT EXISTS(SELECT 1 FROM util.products_tea_fk_review) AS has_fk_products_tea_issues \gset
SELECT EXISTS(SELECT 1 FROM util.products_equipment_fk_review) AS has_fk_products_equipment_issues \gset
SELECT EXISTS(SELECT 1 FROM util.orders_fk_review) AS has_fk_orders_issues \gset
SELECT EXISTS(SELECT 1 FROM util.order_items_fk_review) AS has_fk_order_items_issues \gset
SELECT EXISTS(SELECT 1 FROM util.product_countries_fk_review) AS has_fk_product_countries_issues \gset

\if :has_fk_sessions_batch_inv_issues
  \echo '|    ⚠️  FK issues found in "session_batch_inventory"'
  SELECT * FROM util.session_batch_fk_review;
\else
  \echo '|    ✅ No FK issues in "session_batch_inventory"'
\endif

\if :has_fk_vendors_issues
  \echo '|    ⚠️  FK issues found in "vendors"'
  SELECT * FROM util.vendors_fk_review;
\else
  \echo '|    ✅ No FK issues in "vendors"'
\endif

\if :has_fk_locations_issues
  \echo '|    ⚠️  FK issues found in "locations"'
  SELECT * FROM util.locations_fk_review;
\else
  \echo '|    ✅ No FK issues in "locations"'
\endif

\if :has_fk_sessions_issues
  \echo '|    ⚠️  FK issues found in "sessions"'
  SELECT * FROM util.sessions_fk_review;
\else
  \echo '|    ✅ No FK issues in "sessions"'
\endif

\if :has_fk_extractions_issues
  \echo '|    ⚠️  FK issues found in "extractions"'
  SELECT * FROM util.extractions_fk_review;
\else
  \echo '|    ✅ No FK issues in "extractions"'
\endif

\if :has_fk_products_issues
  \echo '|    ⚠️  FK issues found in "products"'
  SELECT * FROM util.products_fk_review;
\else
  \echo '|    ✅ No FK issues in "products"'
\endif

\if :has_fk_products_coffee_issues
  \echo '|    ⚠️  FK issues found in "products coffee"'
  SELECT * FROM util.products_coffee_fk_review;
\else
  \echo '|    ✅ No FK issues in "products coffee"'
\endif

\if :has_fk_products_tea_issues
  \echo '|    ⚠️  FK issues found in "products tea"'
  SELECT * FROM util.products_tea_fk_review;
\else
  \echo '|    ✅ No FK issues in "products tea"'
\endif

\if :has_fk_products_equipment_issues
  \echo '|    ⚠️  FK issues found in "products equipment"'
  SELECT * FROM util.products_equipment_fk_review;
\else
  \echo '|    ✅ No FK issues in "products equipment"'
\endif

\if :has_fk_orders_issues
  \echo '|    ⚠️  FK issues found in "orders"'
  SELECT * FROM util.orders_fk_review;
\else
  \echo '|    ✅ No FK issues in "orders"'
\endif

\if :has_fk_order_items_issues
  \echo '|    ⚠️  FK issues found in "order items"'
  SELECT * FROM util.order_items_fk_review;
\else
  \echo '|    ✅ No FK issues in "order items"'
\endif

\if :has_fk_product_countries_issues
  \echo '|    ⚠️  FK issues found in "product countries"'
  SELECT * FROM util.product_countries_fk_review;
\else
  \echo '|    ✅ No FK issues in "product countries"'
\endif

DO $$
BEGIN
    IF EXISTS(SELECT 1 FROM util.session_batch_fk_review)
       OR EXISTS(SELECT 1 FROM util.vendors_fk_review)
       OR EXISTS(SELECT 1 FROM util.sessions_fk_review)
       OR EXISTS(SELECT 1 FROM util.locations_fk_review)
       OR EXISTS(SELECT 1 FROM util.extractions_fk_review)
       OR EXISTS(SELECT 1 FROM util.products_fk_review)
       OR EXISTS(SELECT 1 FROM util.products_coffee_fk_review)
       OR EXISTS(SELECT 1 FROM util.products_tea_fk_review)
       OR EXISTS(SELECT 1 FROM util.products_equipment_fk_review)
       OR EXISTS(SELECT 1 FROM util.orders_fk_review)
       OR EXISTS(SELECT 1 FROM util.order_items_fk_review)
       OR EXISTS(SELECT 1 FROM util.product_countries_fk_review)
    THEN RAISE EXCEPTION 'FK issues found';
    END IF;
END $$;