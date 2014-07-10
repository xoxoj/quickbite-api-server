import simplejson
import json
import sys, traceback
from foodjinnInterface import app
from foodjinnInterface.database import db_session
from foodjinnInterface.models import Location
from foodjinnInterface.models import Rating
from flask import Flask, jsonify, request, abort, session, g, redirect, url_for, \
    abort, render_template, flash


@app.route('/home')
def home():
#   longitude = request.form['longitude']
# latitude = request.form['latitude']
# data = request.form['longitude']
# result = db_session.execute("select * from fn_getlocationsbycoordinates_forradius(:longitude,:latitude,:radius)", {'longitude': longitude,'latitude':latitude,'radius':600}, Location)
# result = db_session.execute("select * from planet_osm_point where osm_id
# = :id",{'id': 141813089},Location)
    return "Hello world"

# @app.route('/add', methods=['POST'])
# def add_entry():
#   if not session.get('logged_in'):
# 	abort(401)
#   entry = Entry(request.form['title'], request.form['text'])
#   db_session.add(entry)
#   db_session.commit()
#   flash('New entry was succesfully posted')
#   return redirect(url_for('show_entries'))

# @app.route('/remove/<entryid>')
# def remove_entry(entryid):
#   if not session.get('logged_in'):
# 	abort(401)

#   entry = Entry.query.filter_by(id = entryid).first()

#   db_session.delete(entry);
#   db_session.commit();
#   flash('Entry with Title:' + entry.title + ' was removed')
#   return redirect(url_for('show_entries'))
# @app.route('/displayByCoordinates', methods=['GET', 'POST'])
# def login():
#   error = None
#   if request.method == 'POST':
#     if not request.form['longitude']:
#       error = 'Invalid longitude'
#     elif not request.form['latitude']:
#       error = 'Invalid latitude'
#     else:
#       session['logged_in'] = True
#       flash('You were logged in')
#       longitude = request.form['longitude']
#       latitude = request.form['latitude']
# result = db_session.execute("select * from fn_getlocationsbycoordinates_forradius(:longitude,:latitude,:radius)", {'longitude': longitude,'latitude': latitude,'radius':600}, Location)
# return render_template('show_entries.html', entries=result)
#       return redirect(url_for('show_entries'))
#   return render_template('login.html', error=error)


@app.route('/locations', methods=['GET'])
def get_locations():
    suburb = request.args.get('suburb', None)
    longitude = request.args.get('longitude', None)
    latitude = request.args.get('latitude', None)

    # if (zipcode is not None):
      # entry = list(r.table('locations')
      #   .filter((r.row['tags']
      #     .contains('addr:postcode')) & (r.row['tags']['addr:postcode'] == zipcode))
      #       .run(g.rdb_conn))
      # return json.dumps(entry,sort_keys=True,indent=4,separators=(',',':'))
    if (longitude is not None and latitude is not None):
        result = db_session.execute("select * from fn_getlocationsbycoordinates_forradius(:longitude,:latitude,:radius) as location", {
                                    'longitude': longitude, 'latitude': latitude, 'radius': 1000}, Location).fetchall()
        data = [dict(zip(i.keys(), i.values())) for i in result]
        return (jsonify(locationList=data))
        # return(result)
    elif (suburb is not None):
        result = db_session.execute(
            "select * from fn_getlocationsbysuburb(:suburb) as location", {'suburb': suburb}, Location).fetchall()
        data = [dict(zip(i.keys(), i.values())) for i in result]
        return (jsonify(locationList=data))
    else:
        ''' default response '''
        return "No data returned"


@app.route('/suburbs', methods=['GET'])
def get_suburbs():
    city = request.args.get('city', None)

    # if (zipcode is not None):
        # entry = list(r.table('locations')
        #   .filter((r.row['tags']
        #     .contains('addr:postcode')) & (r.row['tags']['addr:postcode'] == zipcode))
        #       .run(g.rdb_conn))
        # return json.dumps(entry,sort_keys=True,indent=4,separators=(',',':'))
    if (city is not None):
        result = db_session.execute(
            "select * from fn_getdistinctsuburbs_bycity(lower(:city)) as suburb", {'city': city}).fetchall()
        data = [dict(zip(i.keys(), i.values())) for i in result]
        return (jsonify(suburbList=data))
        # return(result)
    else:
        ''' default response '''
        return "No data returned"


@app.route('/ratings', methods=['GET', 'POST'])
def setLocationRating():
    rating = request.args.get('rating', None)
    locationId = request.args.get('locationId', None)
    installationId = request.args.get('installationId', None)
    #print locationId + rating + installationId
    if (rating is not None and locationId is not None and installationId is not None):
        r = Rating(locationId, rating, installationId)
        # r.locationId + r.rating + r.installationId
        # return r.id
        try:
            db_session.add(r)
            db_session.commit()
            return "True"
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
    else:
        return "No data"
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#   error = None
#   if request.method == 'POST':
#     if request.form['longitude'] == None:
#       error = 'Invalid longitude'
#     elif request.form['latitude'] == None:
#       error = 'Invalid latitude'
#   else:
# return redirect(url_for('show_entries'))
#   return render_template('login.html', error=error)

# @app.route('/logout')
# def logout():
#   session.pop('logged_in', None)
#   flash('You were logged out')
#   return redirect(url_for('show_entries'))
