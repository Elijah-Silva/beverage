SET SEARCH_PATH = stage;

-- Seed country codes
INSERT INTO extractions (
	session_code,
	extraction_number,
	extraction_time,
	water_temperature,
	notes
)
SELECT
	session_code::UUID,
	extraction_number::NUMERIC::INT,
	extraction_time::NUMERIC::INT,
	water_temperature::NUMERIC::INT,
	NULLIF(TRIM(notes),'')
FROM raw.extractions;

