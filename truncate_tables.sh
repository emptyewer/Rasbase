/Applications/Postgres.app/Contents/Versions/9.6/bin/psql -p5432 -d "rasbase"<<EOL
\dt
TRUNCATE db_experiment, db_enrichment, db_error, db_nonselectedjunctionstat, db_selectedjunctionstat CASCADE;
\q
EOL
