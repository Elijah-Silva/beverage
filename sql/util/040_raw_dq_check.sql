SELECT EXISTS(SELECT 1 FROM util.raw_vendor_dq_review) AS has_raw_vendors_dq_issues \gset
SELECT EXISTS(SELECT 1 FROM util.raw_sessions_dq_review) AS has_raw_sessions_dq_issues \gset
SELECT EXISTS(SELECT 1 FROM util.raw_orders_dq_review) AS has_raw_orders_dq_issues \gset
SELECT EXISTS(SELECT 1 FROM util.raw_session_batch_inv_dq_review) AS has_raw_session_batch_inv_dq_issues \gset
SELECT EXISTS(SELECT 1 FROM util.raw_order_items_dq_review) AS has_raw_order_items_dq_issues \gset
SELECT EXISTS(SELECT 1 FROM util.raw_locations_dq_review) AS has_raw_locations_dq_issues \gset
SELECT EXISTS(SELECT 1 FROM util.raw_products_dq_review) AS has_raw_products_dq_issues \gset
SELECT EXISTS(SELECT 1 FROM util.raw_extractions_dq_review) AS has_raw_extractions_dq_issues \gset

\if :has_raw_extractions_dq_issues
  \echo '|    ⚠️  DQ issues found in raw "extractions"'
  SELECT * FROM util.raw_extractions_dq_review;
\else
  \echo '|    ✅ No DQ issues in raw "extractions"'
\endif

\if :has_raw_products_dq_issues
  \echo '|    ⚠️  DQ issues found in raw "products"'
  SELECT * FROM util.raw_products_dq_review;
\else
  \echo '|    ✅ No DQ issues in raw "products"'
\endif

\if :has_raw_locations_dq_issues
  \echo '|    ⚠️  DQ issues found in raw "locations"'
  SELECT * FROM util.raw_locations_dq_review;
\else
  \echo '|    ✅ No DQ issues in raw "locations"'
\endif

\if :has_raw_order_items_dq_issues
  \echo '|    ⚠️  DQ issues found in raw "order items"'
  SELECT * FROM util.raw_order_items_dq_review;
\else
  \echo '|    ✅ No DQ issues in raw "order items"'
\endif

\if :has_raw_session_batch_inv_dq_issues
  \echo '|    ⚠️  DQ issues found in raw "session batch inv"'
  SELECT * FROM util.raw_session_batch_inv_dq_review;
\else
  \echo '|    ✅ No DQ issues in raw "session batch inv"'
\endif

\if :has_raw_orders_dq_issues
  \echo '|    ⚠️  DQ issues found in raw "orders"'
  SELECT * FROM util.raw_orders_dq_review;
\else
  \echo '|    ✅ No DQ issues in raw "orders"'
\endif

\if :has_raw_vendors_dq_issues
  \echo '|    ⚠️  DQ issues found in raw "vendors"'
  SELECT * FROM util.raw_vendor_dq_review;
\else
  \echo '|    ✅ No DQ issues in raw "vendors"'
\endif

\if :has_raw_sessions_dq_issues
  \echo '|    ⚠️  DQ issues found in raw "sessions"'
  SELECT * FROM util.raw_sessions_dq_review;
\else
  \echo '|    ✅ No DQ issues in raw "sessions"'
\endif

DO $$
BEGIN
    IF EXISTS(SELECT 1 FROM util.raw_vendor_dq_review)
       OR EXISTS(SELECT 1 FROM util.raw_sessions_dq_review)
       OR EXISTS(SELECT 1 FROM util.raw_orders_dq_review)
       OR EXISTS(SELECT 1 FROM util.raw_session_batch_inv_dq_review)
       OR EXISTS(SELECT 1 FROM util.raw_order_items_dq_review)
       OR EXISTS(SELECT 1 FROM util.raw_locations_dq_review)
       OR EXISTS(SELECT 1 FROM util.raw_products_dq_review)
       OR EXISTS(SELECT 1 FROM util.raw_extractions_dq_review)
    THEN RAISE EXCEPTION 'Raw DQ issues found';
    END IF;
END $$;