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

def decode_geometry(obj,geom):
    coordinates = []
    obj['coordinates'] = coordinates
    obj['type'] = geom.type
    if geom.type == 'Point':
        coordinates.append(geom.point.x)
        coordinates.append(geom.point.y)
    elif geom.type in ('MultiPoint','LineString'):
        for coord_array in geom.coord_array:
            array = []
            for point in coord_array.points:
                array.append([point.x,point.y])
            coordinates.extend(array)
    elif geom.type in ('MultiLineString','Polygon'):
        for multi_array in geom.multi_array:
            seq = []
            for coord_array in multi_array.arrays:
                array = []
                for point in coord_array.points:
                    array.append([point.x,point.y])
                seq.append(array)
            coordinates.extend(seq)
    elif geom.type in ('MultiPolygon'):
        top = []
        for multi_array in geom.multi_array:
            seq = []
            for coord_array in multi_array.arrays:
                array = []
                for point in coord_array.points:
                    array.append([point.x,point.y])
                seq.append(array)
            top.append(seq)
        coordinates.extend(top)

def decode(message):
    obj = {'type':message.type}
    if message.type == 'FeatureCollection':
        for feature in message.features:
            decode_feature(message,feature)
    elif message.type == 'Feature':
        decode_feature(message,obj)
    elif message.type in geometry_types:
        if message.type == 'GeometryCollection':
            for geometry in message.geometries:
                decode_geometry(obj,geometry)
        else:
            decode_geometry(obj,message.geometries[0])
    open('out.json').write(json.dumps(obj))

if __name__ == "__main__":
    #filename = sys.argv[1]
    filename = 'message.pbf'
    data = open(filename,'rb').read()
    message = geojson_pb2.object()
    message.ParseFromString(data)
    print message
    decode(message)
