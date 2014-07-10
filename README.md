API server for the quickbite App.

This project contains 3 parts:

Part 0: Vagrant dev environment. I didn't want my local linux box to be dumping ground for the project, so I created a Vagrant box to sandbox the execution of the server. The server contains Postgresql 9.3 instance, Python uWsgi and Nginx reverse proxy. The end result is I can access the Flask server and Postgres DB through my local network while creating my app on another machine. The environment is portable and there is also an Ansible script (which I need to push). With Ansible+Vagrant I can create sandboxed dev servers on the fly and from scratch in any folder.

Part 1: Import job to parse the OpenStreetMap protobuf file and store it's data into Postgresql database. It uses Imposm parser, PostGIS library and Json datatypes in Postgres 9.3.

Part 2: Flask App. It's a RESTful server running inside the vagrant dev box and providing location, rating and other entities needed for the client.


It's a Pre-Alpha radioactive unstable isotope.
