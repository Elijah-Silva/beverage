SET SEARCH_PATH = util;

-- PSQL Script
SELECT EXISTS(SELECT 1 FROM util.session_batch_dq_review) AS has_dq_issues \gset

\if :has_dq_issues
  \echo '|'
  \echo '|    ⚠️  DQ issues found in "session_batch_inventory"'
  SELECT * FROM util.session_batch_dq_review;
\else
  \echo '|    ✅ No DQ issues in "session_batch_inventory"'
\endif

DO $$
BEGIN
    IF EXISTS(SELECT 1 FROM util.session_batch_dq_review)
    THEN RAISE EXCEPTION 'DQ issues found';
    END IF;
END $$;