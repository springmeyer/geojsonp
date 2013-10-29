#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import struct
import geojson_pb2

geometry_types = ('Point',
                  'MultiPoint',
                  'LineString',
                  'MultiLineString',
                  'Polygon',
                  'MultiPolygon',
                  'GeometryCollection',
                 )

def encode_geometry(geometry,geom):
    geom.type = geometry['type']
    json_coords = geometry.get('coordinates')
    if json_coords and len(json_coords) > 0:
        if geom.type == 'Point':
            geom.point.x = json_coords[0]
            geom.point.y = json_coords[1]
        elif geom.type in ('MultiPoint','LineString'):
            array = geom.coord_array.add()
            for points in json_coords:
                point = array.points.add()
                point.x = points[0]
                point.y = points[1]
        elif geom.type in ('MultiLineString','Polygon'):
            multi_array = geom.multi_array.add()
            for seq in json_coords:
                array = multi_array.arrays.add()
                for points in seq:
                    point = array.points.add()
                    point.x = points[0]
                    point.y = points[1]
        elif geom.type in ('MultiPolygon'):
            for seq1 in json_coords:
                multi_array = geom.multi_array.add()
                for seq in seq1:
                    array = multi_array.arrays.add()
                    for points in seq:
                        point = array.points.add()
                        point.x = points[0]
                        point.y = points[1]

def encode_feature(message,feature):
    feat = message.features.add()
    feat.type = feature['type']
    geometry = feature.get('geometry')
    if geometry:
        geom_type = geometry['type']
        if geom_type == 'GeometryCollection':
            geometries = geometry.get('geometries')
            if geometries:
                for geometry in geometries:
                    geom = feat.geometries.add()
                    encode_geometry(geometry,geom)
        else:
            geom = feat.geometries.add()
            encode_geometry(geometry,geom)
    
    props = feature.get('properties')
    for _property in props:
        prop = feat.properties.add()
        prop.key = _property
        val = props[_property]
        if isinstance(val,unicode):
            prop.value.string_value = val
        elif isinstance(val,float):
            prop.value.double_value = val
        elif isinstance(val,int):
            prop.value.int_value = val
        elif isinstance(val,long):
            prop.value.int_value = val
        elif isinstance(val,bool):
            prop.value.bool_value = val


def encode(obj):
    message = geojson_pb2.object()
    message.type = obj['type']
    if message.type == 'FeatureCollection':
        features = obj.get('features')
        if features:
            for feature in features:
                encode_feature(message,feature)
    elif message.type == 'Feature':
        encode_feature(message,obj)
    elif message.type in geometry_types:
        if message.type == 'GeometryCollection':
            geometries = obj.get('geometries')
            if geometries:
                for geometry in geometries:
                    geom = message.geometries.add()
                    encode_geometry(geometry,geom)
        else:
            geom = message.geometries.add()
            encode_geometry(obj,geom)

             
    print message #.SerializeToString()
    open('message.pbf','wb').write(message.SerializeToString())

if __name__ == "__main__":
    filename = sys.argv[1]
    data = open(filename,'rb').read()
    json_object = json.loads(data)
    encode(json_object) 

