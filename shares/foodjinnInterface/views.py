# -*- coding: utf-8 -*-

import simplejson
import json
import sys, traceback
from foodjinnInterface import app
from foodjinnInterface.database import db_session
from foodjinnInterface.models import Location
from foodjinnInterface.models import Rating
from flask import Flask, jsonify, request, abort, session, g, redirect, url_for, \
    abort, render_template, flash
from functools import wraps

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'f00dJ!nn'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/home', methods=['POST'])
@requires_auth
def home():
    locationId = request.form['locationId']
    return "parameter received: "+ locationId

@app.route('/locations', methods=['GET'])
@requires_auth
def get_locations():
    suburb = request.args.get('suburb', None)
    longitude = request.args.get('longitude', None)
    latitude = request.args.get('latitude', None)
    installationId = request.args.get('installationId',None)
    
    # if (zipcode is not None):
      # entry = list(r.table('locations')
      #   .filter((r.row['tags']
      #     .contains('addr:postcode')) & (r.row['tags']['addr:postcode'] == zipcode))
      #       .run(g.rdb_conn))
      # return json.dumps(entry,sort_keys=True,indent=4,separators=(',',':'))

    if (longitude is not None and latitude is not None and installationId is not None):
	result = db_session.execute("select * from fn_getlocationsbycoordinates_forradius(:longitude,:latitude,:radius,:installationId) as location", {
		    'longitude': longitude, 'latitude': latitude, 'radius': 1000, 'installationId': installationId}, Location).fetchall()
        data = [dict(zip(i.keys(), i.values())) for i in result]
        return (jsonify(locationList=data))
        # return(result)
    elif (suburb is not None and installationId is not None):
        result = db_session.execute(
			"select * from fn_getlocationsbysuburb(:suburb,:installationId) as location", {'suburb': suburb, 'installationId': installationId}, Location).fetchall()
        data = [dict(zip(i.keys(), i.values())) for i in result]
        return (jsonify(locationList=data))
    else:
        ''' default response '''
        return "No data returned"

@app.route('/suburbs', methods=['GET'])
@requires_auth
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
@requires_auth
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
            existingrating = db_session.query(Rating).filter(Rating.locationid==locationId).filter(Rating.installationid.like(installationId)).first()
            if existingrating:
            	db_session.delete(existingrating)
            db_session.add(r)
            db_session.commit()
	    result = db_session.execute("select fn_UpdateAverageRating(:locationid,:installationid) as location",{'locationid': locationId,'installationid': installationId})
            db_session.commit()
            data = [dict(zip(i.keys(),i.values())) for i in result]
            return (jsonify(locationList=data))  
        except:
            return "False"	
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
    else:
        return "No data"
