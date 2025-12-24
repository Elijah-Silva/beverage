SET SEARCH_PATH = stage;

INSERT INTO extractions (
	session_code,
	extraction_number,
	extraction_time,
	water_temperature,
	quantity_output,
	notes
)
SELECT
	session_code::UUID,
	extraction_number::NUMERIC::INT,
	extraction_time::NUMERIC::INT,
	water_temperature::NUMERIC::INT,
	quantity_output::NUMERIC,
	NULLIF(TRIM(notes),'')
FROM raw.extractions;

