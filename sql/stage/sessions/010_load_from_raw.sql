SET SEARCH_PATH = stage;

-- Seed country codes
INSERT INTO sessions (
	session_code,
	brewing_method_name,
	rating,
	water_type,
	session_type,
	session_date,
	favorite_flag,
	session_location_name,
	location_name,
	grind_size,
	notes
)
SELECT
	session_code::UUID,
	TRIM(brewing_method_name),
	rating::INT,
	TRIM(water_type),
	TRIM(session_type),
	session_date::TIMESTAMPTZ,
	favorite_flag::BOOLEAN,
	TRIM(session_location_name),
	TRIM(location_name),
	grind_size::NUMERIC,
	TRIM(notes)
FROM raw.sessions;


INSERT INTO session_batch_inventory (
	session_code,
	product_name,
	vendor_name,
	production_date,
	quantity_used,
	quantity_output,
	unit
)
SELECT
	session_code::UUID,
	TRIM(product_name),
	TRIM(vendor_name),
	production_date::DATE,
	quantity_used::NUMERIC,
	quantity_output::NUMERIC,
	TRIM(unit)
FROM raw.session_batch_inventory;