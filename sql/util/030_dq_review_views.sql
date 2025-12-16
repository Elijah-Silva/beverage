SET SEARCH_PATH = util;

CREATE OR REPLACE VIEW util.session_batch_dq_review AS
SELECT
	sbi.session_code,
	sbi.product_name,
	sbi.vendor_name,
	sbi.quantity_used,
	CASE
		WHEN sbi.quantity_used IS NULL OR sbi.quantity_used <= 0 THEN 'QTY_NON_POSITIVE'
		END AS dq_reason
FROM stage.session_batch_inventory sbi
WHERE sbi.quantity_used IS NULL
   OR sbi.quantity_used <= 0;

