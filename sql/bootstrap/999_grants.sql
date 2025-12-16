DO $$
DECLARE s text;
BEGIN
  FOR s IN SELECT schema_name 
           FROM information_schema.schemata
           WHERE schema_name NOT IN ('information_schema','pg_catalog') LOOP
    EXECUTE format('GRANT USAGE ON SCHEMA %I TO elijah', s);
    EXECUTE format('GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA %I TO elijah', s);
    EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA %I GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO elijah', s);
  END LOOP;
END$$;

