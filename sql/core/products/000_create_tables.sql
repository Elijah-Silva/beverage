SET search_path TO core;

CREATE TABLE products
(
	product_id         INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	product_name       TEXT    NOT NULL,
	product_alt_name   TEXT    NOT NULL,
	product_type_id    INT     NOT NULL,
	vendor_id          INT     NOT NULL,
	role_id				INT		NOT NULL,
	region             TEXT,
	is_active          BOOLEAN NOT NULL DEFAULT TRUE,
	created_date       DATE    NOT NULL DEFAULT NOW(),
	last_modified_date DATE    NOT NULL DEFAULT NOW(),
	notes              TEXT,
	FOREIGN KEY (product_type_id) REFERENCES ref.product_types (product_type_id),
	FOREIGN KEY (vendor_id) REFERENCES vendors (vendor_id),
	UNIQUE (product_name, vendor_id)
);

CREATE TABLE product_coffee_details
(
	product_id           INT PRIMARY KEY REFERENCES products (product_id),
	roast_level          TEXT NOT NULL CHECK (roast_level IN ('Light', 'Medium', 'Medium Dark', 'Dark', 'Espresso')),
	origin_type          TEXT NOT NULL CHECK (origin_type IN ('Single', 'Multi')),
	varietal_id          INT,
	altitude_meters      INT CHECK (altitude_meters >= 0),
	processing_method_id INT,
	FOREIGN KEY (varietal_id) REFERENCES ref.varietals (varietal_id),
	FOREIGN KEY (processing_method_id) REFERENCES ref.processing_methods (processing_method_id)
);

CREATE TABLE product_equipment_details
(
	product_id   INT PRIMARY KEY REFERENCES products (product_id),
	material_id  INT  NOT NULL,
	volume       INT,
	clay_type_id INT,
	pour_speed   INT,
	color        TEXT NOT NULL,
	FOREIGN KEY (material_id) REFERENCES ref.materials (material_id),
	FOREIGN KEY (clay_type_id) REFERENCES ref.clay_types (clay_type_id)
);

CREATE TABLE product_tea_details
(
	product_id           INT PRIMARY KEY REFERENCES products (product_id),
	tea_type             TEXT NOT NULL CHECK (tea_type IN
	                                          ('Green', 'White', 'Yellow', 'Yancha', 'Oolong', 'Black', 'Puer (Shou)',
	                                           'Puer (Sheng)', 'Hei Cha', 'Herbal')),
	cultivar             TEXT,
	altitude_meters      TEXT,
	processing_method_id INT,
	FOREIGN KEY (processing_method_id) REFERENCES ref.processing_methods (processing_method_id)
);