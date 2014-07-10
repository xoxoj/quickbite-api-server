# run this as postgres user, eg:
# imposm-psqldb > create_db.sh; sudo su postgres; sh ./create_db.sh
set -xe
createuser --no-superuser --no-createrole --createdb postgres
createdb -E UTF8 -O postgres foodjinn
createlang plpgsql foodjinn
psql -d foodjinn -f /path/to/postgis.sql 				# <- CHANGE THIS PATH
psql -d foodjinn -f /path/to/spatial_ref_sys.sql 			# <- CHANGE THIS PATH
psql -d foodjinn -f /usr/local/lib/python2.7/dist-packages/imposm/900913.sql
echo "ALTER TABLE geometry_columns OWNER TO postgres;" | psql -d foodjinn
echo "ALTER TABLE spatial_ref_sys OWNER TO postgres;" | psql -d foodjinn
echo "ALTER USER postgres WITH PASSWORD 'osm';" |psql -d foodjinn
echo "host	foodjinn	postgres	127.0.0.1/32	md5" >> /path/to/pg_hba.conf 	# <- CHANGE THIS PATH
set +x
echo "Done. Don't forget to restart postgresql!"
