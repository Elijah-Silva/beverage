-- raw/vendors/010_dq_raw_review_views.sql
-- One-liner checks returning: check_name, issue_count

SET SEARCH_PATH = util;

-- vendors
CREATE OR REPLACE VIEW util.raw_vendor_dq_review AS
SELECT *
FROM (
	SELECT
	    issue_type,
	    COUNT(*) AS issue_count
	FROM raw.vendors
	CROSS JOIN LATERAL (
	    VALUES
	        ('MISSING_VENDOR_NAME', vendor_name IS NULL),
	        ('MISSING_COUNTRY_CODE', country_code IS NULL),
	        ('MISSING_CURRENCY_CODE', currency_code IS NULL)
	) AS checks(issue_type, is_null)
	WHERE is_null
	GROUP BY issue_type

    UNION ALL

    SELECT 'DUPLICATE_VENDOR_NAME_COUNTRY_CODE', COUNT(*)
    FROM (
        SELECT vendor_name, country_code
        FROM raw.vendors
        GROUP BY vendor_name, country_code
        HAVING COUNT(*) > 1
    ) d

) AS issues
WHERE issue_count >= 1;

-- sessions
CREATE OR REPLACE VIEW util.raw_sessions_dq_review AS
SELECT *
FROM (
	SELECT
	    issue_type,
	    COUNT(*) AS issue_count
	FROM raw.sessions
	CROSS JOIN LATERAL (
	    VALUES
	        ('MISSING_SESSION_CODE', session_code IS NULL),
	        ('MISSING_BREWING_METHOD', brewing_method_name IS NULL),
	        ('MISSING_RATING', rating IS NULL),
	        ('MISSING_WATER_TYPE', water_type IS NULL),
	        ('MISSING_SESSION_TYPE', session_type IS NULL),
	        ('MISSING_SESSION_DATE', session_date IS NULL),
	        ('MISSING_FAVORITE_FLAG', favorite_flag IS NULL),
	        ('MISSING_SESSION_LOCATION', session_location_name IS NULL),
	        ('MISSING_LOCATION_NAME', location_name IS NULL)
	) AS checks(issue_type, is_null)
	WHERE is_null
	GROUP BY issue_type
) AS issues
WHERE issue_count >= 1;

-- sessions batch inventory
CREATE OR REPLACE VIEW util.raw_session_batch_inv_dq_review AS
SELECT *
FROM (
	SELECT
	    issue_type,
	    COUNT(*) AS issue_count
	FROM raw.session_batch_inventory
	CROSS JOIN LATERAL (
	    VALUES
	        ('MISSING_SESSION_CODE', session_code IS NULL),
	        ('MISSING_PRODUCT_NAME', product_name IS NULL),
	        ('MISSING_VENDOR_NAME', vendor_name IS NULL),
	        ('MISSING_QUANITTY_USED', quantity_used IS NULL),
	        ('MISSING_UNIT', unit IS NULL)
	) AS checks(issue_type, is_null)
	WHERE is_null
	GROUP BY issue_type
) AS issues
WHERE issue_count >= 1;

-- extractions
CREATE OR REPLACE VIEW util.raw_extractions_dq_review AS
SELECT *
FROM (
	SELECT
	    issue_type,
	    COUNT(*) AS issue_count
	FROM raw.extractions
	CROSS JOIN LATERAL (
	    VALUES
	        ('MISSING_SESSION_CODE', session_code IS NULL),
	        ('MISSING_EXTRACTION_NUMBER', extraction_number IS NULL),
	        ('MISSING_EXTRACTION_TIME', extraction_time IS NULL),
	        ('MISSING_WATER_TEMPERATURE', water_temperature IS NULL)
	) AS checks(issue_type, is_null)
	WHERE is_null
	GROUP BY issue_type
) AS issues
WHERE issue_count >= 1;

-- orders
CREATE OR REPLACE VIEW util.raw_orders_dq_review AS
SELECT *
FROM (
	SELECT
	    issue_type,
	    COUNT(*) AS issue_count
	FROM raw.orders
	CROSS JOIN LATERAL (
	    VALUES
	        ('MISSING_VENDOR_NAME', vendor_name IS NULL),
	        ('MISSING_ORDER_DATE', order_date IS NULL),
	        ('MISSING_ORDER_NUMBER', order_number IS NULL),
	        ('MISSING_SHIPPING_COST', shipping_cost IS NULL),
	        ('MISSING_TOTAL_COST', total_cost IS NULL),
	        ('MISSING_ORDER_STATUS', order_status IS NULL)
	) AS checks(issue_type, is_null)
	WHERE is_null
	GROUP BY issue_type
) AS issues
WHERE issue_count >= 1;

-- orders
CREATE OR REPLACE VIEW util.raw_order_items_dq_review AS
SELECT *
FROM (
	SELECT
	    issue_type,
	    COUNT(*) AS issue_count
	FROM raw.order_items
	CROSS JOIN LATERAL (
	    VALUES
	        ('MISSING_ORDER_NUMBER', order_number IS NULL),
	        ('MISSING_PRODUCT_NAME', product_name IS NULL),
	        ('MISSING_UNIT_PRICE', unit_price IS NULL),
	        ('MISSING_SUBTOTAL', subtotal IS NULL)
	) AS checks(issue_type, is_null)
	WHERE is_null
	GROUP BY issue_type
) AS issues
WHERE issue_count >= 1;

-- locations
CREATE OR REPLACE VIEW util.raw_locations_dq_review AS
SELECT *
FROM (
	SELECT
	    issue_type,
	    COUNT(*) AS issue_count
	FROM raw.locations
	CROSS JOIN LATERAL (
	    VALUES
	        ('MISSING_LOCATION_NAME', location_name IS NULL),
	        ('MISSING_ADDRESS', address IS NULL),
	        ('MISSING_CITY', city IS NULL),
            ('MISSING_STATE', state IS NULL),
	        ('MISSING_COUNTRY_CODE', country_code IS NULL),
	        ('MISSING_LATITUDE', latitude IS NULL),
	        ('MISSING_LONGITUDE', longitude IS NULL)
	) AS checks(issue_type, is_null)
	WHERE is_null
	GROUP BY issue_type
) AS issues
WHERE issue_count >= 1;

-- products
CREATE OR REPLACE VIEW util.raw_products_dq_review AS
SELECT *
FROM (
	SELECT
	    issue_type,
	    COUNT(*) AS issue_count
	FROM raw.products
	CROSS JOIN LATERAL (
	    VALUES
	        ('MISSING_PRODUCT_NAME', product_name IS NULL),
	        ('MISSING_TYPE', product_type IS NULL),
	        ('MISSING_VENDOR', vendor_name IS NULL),
            ('MISSING_ACTIVE_STATUS', is_active IS NULL),
			('MISSING_ROLE', role IS NULL)
	) AS checks(issue_type, is_null)
	WHERE is_null
	GROUP BY issue_type
) AS issues
WHERE issue_count >= 1;