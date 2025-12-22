SET SEARCH_PATH = util;



-- vendors
CREATE OR REPLACE VIEW util.vendors_fk_review AS
SELECT
	sv.vendor_name,
	sv.country_code,
	sv.currency_code,
	CASE
		WHEN cv.vendor_id IS NULL THEN 'NO_MATCH_VENDOR'
		WHEN cc.country_code_id IS NULL THEN 'NO_MATCH_COUNTRY_CODE'
		WHEN currc.currency_code_id IS NULL THEN 'NO_MATCH_CURRENCY_CODE'
		ELSE 'OTHER'
		END AS reason
FROM stage.vendors           sv
LEFT JOIN core.vendors       cv
	ON cv.vendor_name = sv.vendor_name
LEFT JOIN ref.country_codes  cc
	ON cc.country_code = sv.country_code
LEFT JOIN ref.currency_codes currc
	ON currc.currency_code = sv.currency_code
WHERE cv.vendor_id IS NULL
   OR cc.country_code_id IS NULL
   OR currc.currency_code_id IS NULL;

-- locations
CREATE OR REPLACE VIEW util.locations_fk_review AS
SELECT
	l.country_code,
	CASE
		WHEN cc.country_code_id IS NULL THEN 'NO_MATCH_COUNTRY'
		ELSE 'OTHER'
		END AS reason
FROM stage.locations        l
LEFT JOIN ref.country_codes cc
	ON cc.country_code = l.country_code
WHERE cc.country_code_id IS NULL;

-- products
CREATE OR REPLACE VIEW util.products_fk_review AS
SELECT
    cp.product_id,
    p.product_name,
    p.product_type,
    p.vendor_name,
    CASE
        WHEN r.role_id IS NULL THEN 'NO_MATCH_ROLE'
        WHEN cv.vendor_id IS NULL THEN 'NO_MATCH_VENDOR'
        WHEN pt.product_type_id IS NULL THEN 'NO_MATCH_PRODUCT_TYPE'
        ELSE 'OTHER'
    END AS reason
FROM stage.products         p
LEFT JOIN ref.roles r
    ON r.role_name = p.role
LEFT JOIN core.vendors      cv
    ON cv.vendor_name = p.vendor_name
LEFT JOIN ref.product_types pt
    ON pt.product_type_name = p.product_type
LEFT JOIN core.products     cp
    ON p.product_name = cp.product_name
    AND cp.vendor_id = cv.vendor_id
    AND cp.product_type_id = pt.product_type_id
WHERE cp.product_id IS NULL;

-- products_coffee
CREATE OR REPLACE VIEW util.products_coffee_fk_review AS
SELECT
	p.product_id,
	pc.product_name,
	pc.vendor_name,
	pc.varietal,
	pc.processing_method,
	CASE
		WHEN var.varietal_id IS NULL THEN 'NO_MATCH_VARIETAL'
		WHEN pm.processing_method_id IS NULL THEN 'NO_MATCH_PROCESSING_METHOD'
		ELSE 'OTHER'
		END AS reason
FROM stage.products_coffee       pc
JOIN core.vendors                cv
	ON cv.vendor_name = pc.vendor_name
JOIN ref.product_types           pt
	ON pt.product_type_name = 'Coffee'
LEFT JOIN ref.varietals          var
	ON var.varietal_name = pc.varietal
LEFT JOIN ref.processing_methods pm
	ON pm.processing_method_name = pc.processing_method
JOIN core.products               p
	ON p.product_name = pc.product_name
	AND p.vendor_id = cv.vendor_id
	AND p.product_type_id = pt.product_type_id
WHERE var.varietal_id IS NULL
   OR pm.processing_method_id IS NULL;

-- products_tea
CREATE OR REPLACE VIEW util.products_tea_fk_review AS
SELECT
	p.product_id,
	pt.product_name,
	pt.vendor_name,
	pt.processing_method,
	CASE
		WHEN pm.processing_method_id IS NULL THEN 'NO_MATCH_PROCESSING_METHOD'
		ELSE 'OTHER'
		END AS reason
FROM stage.products_tea          pt
JOIN core.vendors                cv
	ON cv.vendor_name = pt.vendor_name
JOIN ref.product_types           ptt
	ON ptt.product_type_name = 'Tea'
LEFT JOIN ref.processing_methods pm
	ON pm.processing_method_name = pt.processing_method
JOIN core.products               p
	ON p.product_name = pt.product_name
	AND p.vendor_id = cv.vendor_id
	AND p.product_type_id = ptt.product_type_id
WHERE pm.processing_method_id IS NULL;

-- products_equipment
CREATE OR REPLACE VIEW util.products_equipment_fk_review AS
SELECT
	p.product_id,
	pe.product_name,
	pe.vendor_name,
	pe.material,
	pe.clay_type,
	CASE
		WHEN m.material_id IS NULL THEN 'NO_MATCH_MATERIAL'
		--WHEN ct.clay_type_id IS NULL THEN 'NO_MATCH_CLAY_TYPE'
		ELSE 'OTHER'
		END AS reason
FROM stage.products_equipment pe
JOIN core.vendors             cv
	ON cv.vendor_name = pe.vendor_name
JOIN ref.product_types        prt
	ON prt.product_type_name = 'Equipment'
LEFT JOIN ref.materials       m
	ON m.material_name = pe.material
LEFT JOIN ref.clay_types      ct
	ON ct.clay_type_name = pe.clay_type
JOIN core.products            p
	ON p.product_name = pe.product_name
	AND p.vendor_id = cv.vendor_id
	AND p.product_type_id = prt.product_type_id
WHERE m.material_id IS NULL;
   --OR ct.clay_type_id IS NULL;

-- orders
CREATE OR REPLACE VIEW util.orders_fk_review AS
SELECT
	o.vendor_name,
	o.order_date,
	o.order_number,
	o.order_status,
	CASE
		WHEN v.vendor_id IS NULL THEN 'NO_MATCH_VENDOR'
		WHEN os.order_status_id IS NULL THEN 'NO_MATCH_ORDER_STATUS'
		ELSE 'OTHER'
		END AS reason
FROM stage.orders          o
LEFT JOIN core.vendors     v
	ON v.vendor_name = o.vendor_name
LEFT JOIN ref.order_status os
	ON os.order_status_name = o.order_status
WHERE v.vendor_id IS NULL
   OR os.order_status_id IS NULL;

-- order items
CREATE OR REPLACE VIEW util.order_items_fk_review AS
SELECT
	oi.order_number,
	oi.product_name,
	CASE
		WHEN o.order_id IS NULL THEN 'NO_MATCH_ORDER'
		WHEN p.product_id IS NULL THEN 'NO_MATCH_PRODUCT'
		ELSE 'OTHER'
		END AS reason
FROM stage.order_items  oi
LEFT JOIN core.orders   o
	ON o.order_number = oi.order_number
LEFT JOIN core.products p
	ON p.product_name = oi.product_name
	AND p.vendor_id = o.vendor_id
WHERE o.order_id IS NULL
   OR p.product_id IS NULL;

-- product countries
CREATE OR REPLACE VIEW util.product_countries_fk_review AS
WITH get_country_names
	     AS
	     (SELECT
		      product_id,
		      TRIM(UNNEST(STRING_TO_ARRAY(p.region, ','))) AS country_name
	      FROM core.products p)
SELECT
	gcn.product_id,
	p.product_name,
	gcn.country_name,
	CASE
		WHEN cc.country_code_id IS NULL THEN 'NO_MATCH_COUNTRY'
		ELSE 'OTHER'
		END AS reason
FROM ref.country_codes       cc
RIGHT JOIN get_country_names gcn
	ON gcn.country_name = cc.country_name
JOIN core.products           p
	ON p.product_id = gcn.product_id
WHERE cc.country_code_id IS NULL;

-- session_batch_inventory
CREATE OR REPLACE VIEW util.session_batch_fk_review AS
SELECT
	sbi.session_code,
	sbi.product_name,
	sbi.vendor_name,
	CASE
		WHEN v.vendor_id IS NULL THEN 'NO_MATCH_VENDOR'
		WHEN s.session_id IS NULL THEN 'NO_MATCH_SESSION'
		WHEN p.product_id IS NULL THEN 'NO_MATCH_PRODUCT'
		WHEN bi.batch_inventory_id IS NULL THEN 'NO_MATCH_BATCH_INVENTORY'
		WHEN bi.production_date IS NULL THEN 'NO_MATCH_PRODUCTION_DATE'
		ELSE 'OTHER'
		END AS reason
FROM stage.session_batch_inventory sbi
LEFT JOIN core.vendors             v
	ON v.vendor_name = sbi.vendor_name
LEFT JOIN core.sessions            s
	ON s.session_code = sbi.session_code
LEFT JOIN core.products            p
	ON p.product_name = sbi.product_name AND p.vendor_id = v.vendor_id
LEFT JOIN core.batch_inventory     bi
	ON bi.product_id = p.product_id AND bi.production_date = sbi.production_date
WHERE p.product_type_id IN (SELECT
	                            product_type_id
                            FROM ref.product_types
                            WHERE product_type_name IN ('Coffee', 'Tea'))
	AND (v.vendor_id IS NULL
   OR s.session_id IS NULL
   OR p.product_id IS NULL
   OR bi.batch_inventory_id IS NULL
   OR bi.production_date IS NULL)

UNION ALL

SELECT
	sbi.session_code,
	sbi.product_name,
	sbi.vendor_name,
	CASE
		WHEN v.vendor_id IS NULL THEN 'NO_MATCH_VENDOR'
		WHEN s.session_id IS NULL THEN 'NO_MATCH_SESSION'
		WHEN p.product_id IS NULL THEN 'NO_MATCH_PRODUCT'
		WHEN bi.batch_inventory_id IS NULL THEN 'NO_MATCH_BATCH_INVENTORY'
		ELSE 'OTHER'
		END AS reason
FROM stage.session_batch_inventory sbi
LEFT JOIN core.vendors             v
	ON v.vendor_name = sbi.vendor_name
LEFT JOIN core.sessions            s
	ON s.session_code = sbi.session_code
LEFT JOIN core.products            p
	ON p.product_name = sbi.product_name AND p.vendor_id = v.vendor_id
LEFT JOIN core.batch_inventory     bi
	ON bi.product_id = p.product_id
WHERE p.product_type_id IN (SELECT
	                            product_type_id
                            FROM ref.product_types
                            WHERE product_type_name NOT IN ('Coffee', 'Tea'))
	AND (v.vendor_id IS NULL
   OR s.session_id IS NULL
   OR p.product_id IS NULL
   OR bi.batch_inventory_id IS NULL)

UNION ALL

select
	sbi.session_code,
	sbi.product_name,
	sbi.vendor_name,
	CASE
		WHEN p.product_id IS NULL THEN 'NO_MATCH_PRODUCT'
		ELSE 'OTHER'
		END AS reason
FROM stage.session_batch_inventory sbi
LEFT JOIN core.vendors             v
	ON v.vendor_name = sbi.vendor_name
LEFT JOIN core.sessions            s
	ON s.session_code = sbi.session_code
LEFT JOIN core.products            p
	ON p.product_name = sbi.product_name AND p.vendor_id = v.vendor_id
WHERE p.product_id IS NULL;

-- sessions
CREATE OR REPLACE VIEW util.sessions_fk_review AS
SELECT
	s.session_code,
	s.brewing_method_name,
	s.session_location_name,
	s.location_name,
	CASE
		WHEN bm.brewing_method_id IS NULL THEN 'NO_MATCH_BREWING_METHOD'
		WHEN sl.session_location_id IS NULL THEN 'NO_MATCH_SESSION_LOCATION'
		WHEN l.location_id IS NULL THEN 'NO_MATCH_LOCATION'
		ELSE 'OTHER'
		END AS reason
FROM stage.sessions             s
LEFT JOIN ref.brewing_methods   bm
	ON bm.brewing_method_name = s.brewing_method_name
LEFT JOIN ref.session_locations sl
	ON sl.session_location_name = s.session_location_name
LEFT JOIN core.locations        l
	ON l.location_name = s.location_name
WHERE bm.brewing_method_id IS NULL
   OR sl.session_location_id IS NULL
   OR l.location_id IS NULL;

-- extractions
CREATE OR REPLACE VIEW util.extractions_fk_review AS
SELECT
	e.session_code,
	CASE
		WHEN s.session_id IS NULL THEN 'NO_MATCH_SESSSION'
		ELSE 'OTHER'
		END AS reason
FROM stage.extractions  e
LEFT JOIN core.sessions s
	ON s.session_code = e.session_code
WHERE s.session_id IS NULL;