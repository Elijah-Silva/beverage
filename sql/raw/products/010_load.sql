SET SEARCH_PATH = raw;

-- Seed country codes
COPY products (product_name, product_alt_name, product_type, vendor_name, role, region, roast_level, origin_type, varietal,
               altitude_meters, processing_method, material, volume, clay_type, pour_speed, color, tea_type,
               cultivar, is_active, notes)
	FROM '/home/elijah/beverage/data/raw/products.csv'
	DELIMITER ',' CSV HEADER;