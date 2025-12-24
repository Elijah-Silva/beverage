SET SEARCH_PATH = raw;

CREATE TABLE extractions (
    session_code            TEXT,
    extraction_number       TEXT,
    extraction_time         TEXT,
    water_temperature       TEXT,
    quantity_output         TEXT,
    notes                   TEXT
);