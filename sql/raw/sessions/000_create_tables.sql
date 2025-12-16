SET SEARCH_PATH = raw;

CREATE TABLE sessions (
    session_code            TEXT,
    brewing_method_name     TEXT,
    rating                  TEXT,
    water_type              TEXT,
    session_type            TEXT,
    session_date            TEXT,
    favorite_flag           TEXT,
    session_location_name   TEXT,
    location_name           TEXT,
    grind_size              TEXT,
    notes                   TEXT
);

CREATE TABLE session_batch_inventory (
    session_code    TEXT,
    product_name    TEXT,
    vendor_name     TEXT,
	production_date TEXT,
    quantity_used   TEXT,
	quantity_output TEXT,
    unit            TEXT
);