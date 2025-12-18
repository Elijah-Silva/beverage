SET search_path TO stage;

-- freshen
TRUNCATE stage.raw_products;
TRUNCATE stage.products;
TRUNCATE stage.products_tea;
TRUNCATE stage.products_coffee;
TRUNCATE stage.products_equipment;

-- 1) Clean + cast from raw into a staging buffer (stage.raw_products)
INSERT INTO stage.raw_products (
	product_name,
	product_alt_name,
	product_type,
	vendor_name,
	role,
	region,
	roast_level,
	origin_type,
	varietal,
	altitude_meters,
	processing_method,
	material,
	volume,
	clay_type,
	pour_speed,
	color,
	tea_type,
	cultivar,
	is_active,
	notes
)
SELECT
	TRIM(product_name),
	TRIM(product_alt_name),
	TRIM(product_type),
	TRIM(vendor_name),
	TRIM(role),
	TRIM(region),
	TRIM(roast_level),
	TRIM(origin_type),
	TRIM(varietal),
	altitude_meters::NUMERIC::INT,
	TRIM(processing_method),
	TRIM(material),
	volume::NUMERIC::INT,
	TRIM(clay_type),
	pour_speed::NUMERIC::INT,
	TRIM(color),
	TRIM(tea_type),
	TRIM(cultivar),
	is_active::BOOLEAN,
	TRIM(notes)
FROM raw.products;

-- 2) Slim main stage table (for core.products)
INSERT INTO stage.products (
	product_name,
	product_alt_name,
	product_type,
	vendor_name,
	role,
	region,
	is_active,
	notes
)
SELECT
	product_name,
	product_alt_name,
	product_type,
	vendor_name,
	role,
	region,
	is_active,
	notes
FROM stage.raw_products;

-- 3) Route to subtypes (match the same UPPER convention)
-- TEA
INSERT INTO stage.products_tea (
	product_name,
	product_alt_name,
	vendor_name,
	tea_type,
	cultivar,
	altitude_meters,
	processing_method
)
SELECT
	product_name,
	product_alt_name,
	vendor_name,
	tea_type,
	cultivar,
	altitude_meters,
	processing_method
FROM stage.raw_products
WHERE product_type = 'Tea';

-- COFFEE
INSERT INTO stage.products_coffee (
	product_name,
	product_alt_name,
	vendor_name,
	roast_level,
	origin_type,
	varietal,
	altitude_meters,
	processing_method
)
SELECT
	product_name,
	product_alt_name,
	vendor_name,
	roast_level,
	origin_type,
	varietal,
	altitude_meters,
	processing_method
FROM stage.raw_products
WHERE product_type = 'Coffee';

-- EQUIPMENT
INSERT INTO stage.products_equipment (
	product_name,
	product_alt_name,
	vendor_name,
	material,
	volume,
	clay_type,
	pour_speed,
	color
)
SELECT
	product_name,
	product_alt_name,
	vendor_name,
	material,
	volume,
	clay_type,
	pour_speed,
	color
FROM stage.raw_products
WHERE product_type = 'Equipment';
