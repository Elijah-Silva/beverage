SET SEARCH_PATH = raw;

CREATE TABLE products (
    product_name        TEXT,
	product_alt_name    TEXT,
    product_type        TEXT,
    vendor_name         TEXT,
    role                TEXT,
    region              TEXT,
    roast_level         TEXT,
    origin_type         TEXT,
    varietal            TEXT,
    altitude_meters     TEXT,
    processing_method   TEXT,
    material            TEXT,
    volume              TEXT,
    clay_type           TEXT,
    pour_speed          TEXT,
    color               TEXT,
    tea_type            TEXT,
    cultivar            TEXT,
    is_active           TEXT,
    notes               TEXT

    /*
    -- ingest metadata (critical!)
    ingest_id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_file         TEXT NOT NULL,
    source_rownum       INT  NOT NULL,
    ingested_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    load_batch_id       TEXT NOT NULL
     */
);