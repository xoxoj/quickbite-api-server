
# shell script to run uWsgi in bg
begin;
	uwsgi --socket 127.0.0.1:4242 --module runserver --callable app --processes 4 --threads 2 --stats 0.0.0.0:9191
end;
# uwsgi --socket 0.0.0.0:4242 --wsgi-file runserver.py --module runserver --callable app --buffer-size 65535 --processes 4 --threads 2 --stats 0.0.0.0:9191

# uwsgi --http 0.0.0.0:4242 --master --module runserver --callable app --buffer-size 65535 --processes 4 --threads 2 --stats 0.0.0.0:9191

#uwsgi --socket 0.0.0.0:5000 --wsgi-file runserver.py --callable app --processes 4 --threads 2 --stats 0.0.0.0:9191

#uwsgi -s /tmp/uwsgi.sock --wsgi-file runserver.py --callable app --processes 4 --threads 2 --stats 0.0.0.0:9191

#uwsgi -s /tmp/uwsgi.sock --module runserver --callable app

#uwsgi --socket 127.0.0.1:4242 --module runserver --callable app

#    location / { try_files $uri @[app]; }
#    location @[app] {
#        uwsgi_pass 127.0.0.1:4242;
#        include uwsgi_params;
#    }