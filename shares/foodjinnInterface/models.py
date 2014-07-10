from sqlalchemy import Column, Integer, String, Float
from foodjinnInterface.database import Base
from sqlalchemy import func
from sqlalchemy.types import UserDefinedType
from collections import OrderedDict
import json
from sqlalchemy.types import TypeDecorator, VARCHAR


class Geometry(UserDefinedType):

    def get_col_spec(self):
        return "GEOMETRY"

    def bind_expression(self, bindvalue):
        return func.ST_GeomFromText(bindvalue, type_=self)

    def column_expression(self, col):
        return func.ST_AsText(col, type_=self)


class JsonType(TypeDecorator):

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value:
            return unicode(json.dumps(value))
        else:
            return {}

    def process_result_value(self, value, dialect):
        if value:
            return json.loads(value)
        else:
            return {}


class Location(Base):
  __tablename__ = 'locations'
  id = Column(Integer, primary_key=True)
  data = Column(JsonType)
  # way = Column(Geometry)

  def __init__(self, data):
    self.data = data

  @property
  def serialize(self):
    return {
        'osm_id': self.osm_id,
        'name': self.name,
        'cuisine': self.cuisine,
        'amenity': self.amenity,
        'housenumber': self.housenumber,
        'housename': self.housename,
        'suburb': self.suburb,
        'street': self.street,
        'postcode': self.postcode,
        'distance': self.distance
       }

  def __repr__(self):
   '<Entry %r>' % (self.data)


class Rating(Base):
  __tablename__ = 'ratings'
  id = Column(Integer, autoincrement=1, primary_key=True)
  locationid = Column(Integer)
  rating = Column(Float)
  installationid = Column(String)

  def __init__(self,locationId,rating,installationId):
    # self.id = id	 
    self.locationid = locationId
    self.rating = rating
    self.installationid = installationId

     
