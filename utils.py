import os
import sys

import fiona
from fiona.crs import from_epsg


class GaoDeKeys:
    keypath = os.path.join(os.path.dirname(__file__), "gaode_web_keys")
    if os.path.exists(keypath):
        print(f"{keypath}文件不存在")
        sys.exit(-1)

    with open(keypath) as kf:
        keys = [k.strip() for k in kf.readlines()]

    if not keys:
        print(f"{keypath}文件为空")
        sys.exit(-1)

    idx = 0

    @classmethod
    def get(cls):
        cls.idx = (cls.idx + 1) % len(cls.keys)
        return cls.keys[cls.idx]


def polyline2mulitpolygon(polyline):
    plines = polyline.split("|")
    coords = []
    for line in plines:
        subcoords = []
        ps = line.split(";")
        for p in ps:
            lng, lat = p.split(",")
            subcoords.append((float(lng), float(lat)))
        subcoords.append(subcoords[0])
        coords.append([subcoords])
    return {
        "type": "MultiPolygon",
        "coordinates": coords
    }


class DistShpSchema:
    China = {
        "geometry": "MultiPolygon",
        "properties": {
            "code": "str",
            "name": "str",
            "center": "str"
        }
    }

    Prov = {
        "geometry": "MultiPolygon",
        "properties": {
            "code": "str",
            "name": "str",
            "center": "str"
        }
    }

    City = {
        "geometry": "MultiPolygon",
        "properties": {
            "code": "str",
            "name": "str",
            "center": "str",
            "prov_name": "str",
            "prov_code": "str"
        }
    }

    County = {
        "geometry": "MultiPolygon",
        "properties": {
            "code": "str",
            "name": "str",
            "center": "str",
            "prov_name": "str",
            "prov_code": "str",
            "city_name": "str",
            "city_code": "str"
        }
    }


class DistShp:

    def __init__(self, filepath, schema, crs=from_epsg(4326)):
        self.shp = fiona.open(filepath, "w", crs=crs, driver="ESRI Shapefile", schema=schema, encoding="utf-8")

    def write(self, record):
        self.shp.write(record)

    def close(self):
        self.shp.close()
