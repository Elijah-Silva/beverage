SET SEARCH_PATH = util;

CREATE VIEW util.recent_sessions AS
WITH get_brew_quantity AS
	     (SELECT
		      sbi.session_id,
		      sbi.quantity_used
	      FROM core.session_batch_inventory sbi
	      JOIN core.batch_inventory         bi
		      USING (batch_inventory_id)
	      JOIN core.products                p
		      USING (product_id)
	      WHERE role_id IN (
			SELECT role_id
			FROM ref.roles
			WHERE role_name IN ( 'Tea Dose', 'Espresso Dose')))
SELECT
	s.session_id                AS id,
	TO_CHAR(s.session_date, 'YYYY-MM-DD HH24:MI') AS date,
	s.session_type              AS category,
	bm.brewing_method_name      AS brew,
	(SELECT
		 STRING_AGG(product_alt_name, ', ') AS ingredient
	 FROM core.session_batch_inventory sbi
	 JOIN core.batch_inventory         bi
		 USING (batch_inventory_id)
	 JOIN core.products                p
		 USING (product_id)
	 WHERE role_id IN (SELECT
		                   role_id
	                   FROM ref.roles
	                   WHERE role_name IN ('Espresso Dose', 'Tea Dose'))
	   AND session_id = s.session_id),
	s.rating,
	gbq.quantity_used           AS input,
	s.grind_size                AS grind,
	e.extraction_time           AS time,
	e.water_temperature         AS temp
	/*
	(SELECT
		 STRING_AGG(product_alt_name, ', ') AS equipment
	 FROM core.session_batch_inventory sbi
	 JOIN core.batch_inventory         bi
		 USING (batch_inventory_id)
	 JOIN core.products                p
		 USING (product_id)
	 WHERE role_id IN (SELECT
		                   role_id
	                   FROM ref.roles
	                   WHERE role_name NOT IN ('Espresso Dose', 'Tea Dose'))
	   AND session_id = s.session_id)
	s.notes                     AS session_notes,
	e.notes                     AS extraction_notes
	*/
FROM core.sessions              s
LEFT JOIN core.extractions      e
	USING (session_code)
LEFT JOIN get_brew_quantity gbq
	ON gbq.session_id = s.session_id
JOIN ref.brewing_methods        bm
	USING (brewing_method_id);


SELECT *
FROM util.recent_sessions
ORDER BY date ASC;