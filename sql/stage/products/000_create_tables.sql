SET search_path TO stage;

CREATE TABLE raw_products
(
	product_name       TEXT NOT NULL,
	product_alt_name   TEXT,
	product_type       TEXT,
	vendor_name        TEXT,
	role				TEXT,
	region             TEXT,
	roast_level        TEXT,
	origin_type        TEXT,
	varietal           TEXT,
	altitude_meters    INT,
	processing_method  TEXT,
	material           TEXT,
	volume             INT,
	clay_type          TEXT,
	pour_speed         INT,
	color              TEXT,
	tea_type           TEXT,
	cultivar           TEXT,
	is_active          BOOLEAN,
	notes              TEXT
);

CREATE TABLE products
(
	product_name       TEXT NOT NULL,
	product_alt_name    TEXT,
	product_type       TEXT,
	vendor_name        TEXT,
	role				TEXT,
	region             TEXT,
	is_active          BOOLEAN,
	notes              TEXT
);

-- subtype stage tables
CREATE TABLE IF NOT EXISTS products_tea
(
	product_name      TEXT NOT NULL,
	product_alt_name    TEXT,
	vendor_name       TEXT,
	tea_type          TEXT,
	cultivar          TEXT,
	altitude_meters   TEXT,
	processing_method TEXT
);

CREATE TABLE IF NOT EXISTS products_coffee
(
	product_name      TEXT NOT NULL,
	product_alt_name    TEXT,
	vendor_name       TEXT,
	roast_level       TEXT,
	origin_type       TEXT,
	varietal          TEXT,
	altitude_meters   INT,
	processing_method TEXT
);

CREATE TABLE IF NOT EXISTS products_equipment
(
	product_name TEXT NOT NULL,
	product_alt_name    TEXT,
	vendor_name  TEXT,
	material     TEXT,
	volume       INT,
	clay_type    TEXT,
	pour_speed   INT,
	color        TEXT
);