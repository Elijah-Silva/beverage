SET SEARCH_PATH = core;

CREATE TABLE extractions
(
	extract_id        INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	session_id        INT  NOT NULL,
	session_code      UUID NOT NULL,
	extraction_number INT  NOT NULL CHECK (extraction_number BETWEEN 1 AND 99),
	extraction_time   INT  NOT NULL CHECK (extraction_time BETWEEN 1 AND 999999),
	water_temperature INT  NOT NULL CHECK (water_temperature BETWEEN 1 AND 999),
	quantity_output             NUMERIC,    CHECK (quantity_output >= 1),
	notes      TEXT,
	FOREIGN KEY (session_id) REFERENCES sessions (session_id)
		ON UPDATE RESTRICT
		ON DELETE CASCADE,
	UNIQUE (session_code, extraction_number)
);