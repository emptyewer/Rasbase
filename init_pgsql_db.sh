find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
/Applications/Postgres.app/Contents/Versions/9.6/bin/psql<<EOL
DROP DATABASE rasbase;
CREATE DATABASE rasbase;
CREATE USER piper WITH PASSWORD 'ubiquitin';
GRANT ALL PRIVILEGES ON DATABASE rasbase to piper;
\q
EOL

python manage.py makemigrations
python manage.py migrate
python manage.py shell<<EOF
execfile('load_genes.py')
execfile('load_baits_vectors.py')
EOF

# python manage.py createsuperuser
