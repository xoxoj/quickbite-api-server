#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from imposm.parser import OSMParser
import psycopg2
import io, json, codecs
from pprint import pprint
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

# import rethinkdb as r
# from rethinkdb.errors import RqlRuntimeError, RqlDriverError

# app = Flask(__name__)
# app.debug = True
nodes = {}
restaurants = 0
class HighwayCounter(object):
	#var conn
	#try:
	restaurants = 0
	conn = psycopg2.connect("dbname='foodjinn' user='postgres' host='127.0.0.1' port='5432' password='postgres'")
	conn.set_client_encoding('UTF8')

	#conn = psycopg2.connect("dbname='foodjinnGeo' user='postgres' host='192.168.33.10' port='5430' password='postgres'")
	#except:
	    #print("I am unable to connect to the database")

	def nodes(self, nodes):		
		jsonOutput = codecs.open('jsonOutput.json', 'a', 'utf-8')
		cur = self.conn.cursor() 
		for osmid, tags, coords in nodes:
			#print(osmid)
			
			data = {
				"osmid": osmid,
				"lon": coords[0],
				"lat": coords[1],
				"tags": tags
				#name' : self.name,
				#'amenity' : self.amenity,		
				#'country' : self.country
				#'postalcode' : tags[u'addr:postcode']
			}
			# restaurants
			matchingRestaurants = u'restaurant' in tags.values()
			matchingCafes = u'cafe' in tags.values()
			matchingPubs = u'pub' in tags.values()
			matchingbars = u'bar' in tags.values()


			if matchingRestaurants | matchingCafes| matchingPubs | matchingbars:
				#print(osmid)
				#data.tags = data.tags.replace('"', '\\"')
				jsonString = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8")
	  			# .replace('"', '\\"')
				self.restaurants+=1
				#matchingRestaurants = None
				try:
					cur.execute("INSERT INTO locations (id,data) VALUES (%s,%s)",(self.restaurants,jsonString))
					self.conn.commit()
				except Exception, e:
					jsonOutput.write('\n')
					jsonOutput.write("error occured: "+str(e))
					#jsonOutput.write(json.dumps(jsonString, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8"))
				
			# if (matchingCafes is not None):
			# 	data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8").decode('unicode-escape')
			# 	jsonOutput.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8").decode('unicode-escape'))
			# 	jsonOutput.write('\n')
			# 	self.restaurants+=1
			# 	#cur.execute("INSERT INTO locationsTest (id,data) VALUES (%s,%s)",(self.restaurants,data))
			# if (matchingPubs is not None):
			# 	data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8").decode('unicode-escape')
			# 	jsonOutput.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8").decode('unicode-escape'))
			# 	jsonOutput.write('\n')
			# 	self.restaurants+=1
			# 	#cur.execute("INSERT INTO locationsTest (id,data) VALUES (%s,%s)",(self.restaurants,data))
			# if (matchingbars is not None):
			# 	data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8").decode('unicode-escape')
			# 	jsonOutput.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), encoding="utf-8").decode('unicode-escape'))
			# 	jsonOutput.write('\n')
			# 	#print(data)
			# 	self.restaurants+=1
				#cur.execute("INSERT INTO locationsTest (id,data) VALUES (%s,%s)",(self.restaurants,data))
			#query = "INSERT INTO locationsTest (data) VALUES (%s)"
			#inserted = r.db('foodjinn').table('locations').insert(data).run()


		#print(self.restaurants) # = r.db('foodjinn').table('locations').count().run()			
		# self.conn.commit()
		# cur.close()
		# self.conn.close()

counter = HighwayCounter()
#p = OSMParser(concurrency=8, ways_callback=counter.nodes)
p = OSMParser(concurrency=8, nodes_callback=counter.nodes)
p.parse('berlin-latest.osm.pbf')    
