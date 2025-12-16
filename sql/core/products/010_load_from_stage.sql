SET SEARCH_PATH = core;

INSERT INTO core.products (
	product_name,
	product_alt_name,
	product_type_id,
	vendor_id,
	role_id,
	region,
	is_active,
	notes
)
SELECT
	p.product_name,
	p.product_alt_name,
	pt.product_type_id,
	cv.vendor_id,
	r.role_id,
	p.region,
	p.is_active,
	p.notes
FROM stage.products    p
JOIN core.vendors      cv
	ON cv.vendor_name = p.vendor_name
JOIN ref.product_types pt
	ON pt.product_type_name = p.product_type
JOIN ref.roles 			r
	ON r.role_name = p.role;

-- product coffee details
INSERT INTO core.product_coffee_details (
	product_id,
	roast_level,
	origin_type,
	varietal_id,
	altitude_meters,
	processing_method_id
)
SELECT
	p.product_id,
	pc.roast_level,
	pc.origin_type,
	var.varietal_id,
	pc.altitude_meters,
	pm.processing_method_id
FROM stage.products_coffee  pc
JOIN core.vendors           cv
	ON cv.vendor_name = pc.vendor_name
JOIN ref.product_types      pt
	ON pt.product_type_name = 'Coffee'
JOIN ref.varietals          var
	ON var.varietal_name = pc.varietal
JOIN ref.processing_methods pm
	ON pm.processing_method_name = pc.processing_method
JOIN core.products          p
	ON p.product_name = pc.product_name
	AND p.vendor_id = cv.vendor_id
	AND p.product_type_id = pt.product_type_id;

-- product tea details
INSERT INTO core.product_tea_details (
	product_id,
	tea_type,
	cultivar,
	altitude_meters,
	processing_method_id
)
SELECT
	p.product_id,
	pt.tea_type,
	pt.cultivar,
	pt.altitude_meters,
	pm.processing_method_id
FROM stage.products_tea     pt
JOIN core.vendors           cv
	ON cv.vendor_name = pt.vendor_name
JOIN ref.product_types      prt
	ON prt.product_type_name = 'Tea'
JOIN ref.processing_methods pm
	ON pm.processing_method_name = pt.processing_method
JOIN core.products          p
	ON p.product_name = pt.product_name
	AND p.vendor_id = cv.vendor_id
	AND p.product_type_id = prt.product_type_id;

-- product equipment details
INSERT INTO core.product_equipment_details (
	product_id,
	material_id,
	volume,
	clay_type_id,
	pour_speed,
	color
)
SELECT
	p.product_id,
	m.material_id,
	pe.volume,
	ct.clay_type_id,
	pe.pour_speed,
	pe.color
FROM stage.products_equipment pe
JOIN core.vendors             cv
	ON cv.vendor_name = pe.vendor_name
JOIN ref.product_types        prt
	ON prt.product_type_name = 'Equipment'
JOIN ref.materials            m
	ON m.material_name = pe.material
LEFT JOIN ref.clay_types      ct
	ON ct.clay_type_name = pe.clay_type
JOIN core.products            p
	ON p.product_name = pe.product_name
	AND p.vendor_id = cv.vendor_id
	AND p.product_type_id = prt.product_type_id;