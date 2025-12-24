SET SEARCH_PATH = raw;

-- Seed country codes
COPY extractions (session_code, extraction_number, extraction_time, water_temperature, quantity_output, notes)
FROM '/home/elijah/beverage/data/raw/extractions.csv'
DELIMITER ',' CSV HEADER;