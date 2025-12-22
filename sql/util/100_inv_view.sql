SET SEARCH_PATH = util;

-- 1) Usage per batch (helper)
CREATE OR REPLACE VIEW util.v_usage_by_batch AS
SELECT
	sbi.batch_inventory_id,
	COALESCE(SUM(sbi.quantity_used), 0)::NUMERIC(12, 2) AS qty_used_g
FROM core.session_batch_inventory sbi
GROUP BY sbi.batch_inventory_id;

-- 2) Per-batch remaining (your view, simplified + safer)
CREATE OR REPLACE VIEW util.v_batch_inventory_remaining AS
SELECT
	--bi.batch_inventory_id,
	bi.product_id,
	p.product_name,
	bi.quantity_weight::NUMERIC(12, 2)                    AS initial_qty,
	COALESCE(ub.qty_used_g, 0)::NUMERIC(12, 2)            AS consumed_qty,
	GREATEST(bi.quantity_weight - COALESCE(ub.qty_used_g, 0), 0)::NUMERIC(12, 2)
	                                                      AS qty_remaining,
	(bi.quantity_weight - COALESCE(ub.qty_used_g, 0)) > 0 AS is_in_stock
--(bi.quantity_weight - COALESCE(ub.qty_used_g, 0)) < 0 AS is_overused
FROM core.batch_inventory       bi
JOIN core.products              p
	ON p.product_id = bi.product_id
LEFT JOIN util.v_usage_by_batch ub
	ON ub.batch_inventory_id = bi.batch_inventory_id
WHERE p.product_type_id IN (SELECT
	                            pt.product_type_id
                            FROM ref.product_types pt
                            WHERE pt.product_type_name IN ('Coffee', 'Tea'));

-- 3) Total sum across batches per product
CREATE OR REPLACE VIEW util.v_inventory_by_product AS
SELECT
	p.product_id,
	p.product_name,
	COUNT(*)                             AS batch_count,
	SUM(v.initial_qty)::NUMERIC(12, 2)   AS qty_received_g,
	SUM(v.consumed_qty)::NUMERIC(12, 2)  AS qty_used_g,
	SUM(v.qty_remaining)::NUMERIC(12, 2) AS qty_on_hand_g
FROM util.v_batch_inventory_remaining v
JOIN core.products                    p
	ON p.product_id = v.product_id
GROUP BY p.product_id, p.product_name
ORDER BY p.product_name;