import os.path
import sys
import requests
from collections import OrderedDict
from utils import polyline2mulitpolygon, DistShp, DistShpSchema, GaoDeKeys

if len(sys.argv) < 2:
    print('''用法: python3 main.py [outdir]
        outdir: 生成shp存储目录''')
    sys.exit(-1)

outdir = sys.argv[1]

if not os.path.exists(outdir):
    print("ERROR:", f"{outdir}不存在")
    sys.exit(-1)

query_url = f"https://restapi.amap.com/v3/config/district?subdistrict=1&extensions=all"

rsp = requests.get(query_url, params={
    "key": GaoDeKeys.get(),
    "keywords": "100000"
}).json()

if rsp["infocode"] != "10000":
    print("ERROR:", rsp["infocode"])
    sys.exit(-1)

china = rsp["districts"][0]
center, polyline = china["center"], china["polyline"]
geom = polyline2mulitpolygon(polyline)
shp = DistShp(os.path.join(outdir, "china.shp"), DistShpSchema.China)
shp.write({
    "geometry": geom,
    "properties": OrderedDict({
        "code": china["adcode"],
        "name": china["name"],
        "center": china["center"]
    })
})
shp.close()


provs = china["districts"]
citys = []

shp = DistShp(os.path.join(outdir, "prov.shp"), DistShpSchema.Prov)

for item in provs:
    rsp = requests.get(query_url, params={
        "key": GaoDeKeys.get(),
        "keywords": item["adcode"]
    }).json()

    if rsp["infocode"] != "10000":
        print("ERROR:", rsp["infocode"])
        sys.exit(-1)

    prov = rsp["districts"][0]
    geom = polyline2mulitpolygon(prov["polyline"])
    shp.write({
        "geometry": geom,
        "properties": OrderedDict({
            "code": prov["adcode"],
            "name": prov["name"],
            "center": prov["center"]
        })
    })

    for city in prov["districts"]:
        city["prov_name"] = item["name"]
        city["prov_code"] = item["adcode"]

    citys = citys + prov["districts"]

shp.close()


countys = []

shp = DistShp(os.path.join(outdir, "city.shp"), DistShpSchema.City)

for item in citys:
    rsp = requests.get(query_url, params={
        "key": GaoDeKeys.get(),
        "keywords": item["adcode"]
    }).json()

    if rsp["infocode"] != "10000":
        print("ERROR:", rsp["infocode"])
        sys.exit(-1)

    city = rsp["districts"][0]
    geom = polyline2mulitpolygon(city["polyline"])
    shp.write({
        "geometry": geom,
        "properties": OrderedDict({
            "code": item["adcode"],
            "name": item["name"],
            "center": item["center"],
            "prov_name": item["prov_name"],
            "prov_code": item["prov_code"]
        })
    })
    for county in city["districts"]:
        county["prov_name"] = item["prov_name"]
        county["prov_code"] = item["prov_code"]
        county["city_name"] = item["name"]
        county["city_code"] = item["adcode"]

    countys = countys + city["districts"]

shp.close()


shp = DistShp(os.path.join(outdir, "county.shp"), DistShpSchema.County)
for item in countys:
    rsp = requests.get(query_url, params={
        "key": GaoDeKeys.get(),
        "keywords": item["adcode"]
    }).json()

    if rsp["infocode"] != "10000":
        print("ERROR:", rsp["infocode"])
        sys.exit(-1)

    county = rsp["districts"][0]
    geom = polyline2mulitpolygon(county["polyline"])
    shp.write({
        "geometry": geom,
        "properties": OrderedDict({
            "code": item["adcode"],
            "name": item["name"],
            "center": item["center"],
            "prov_name": item["prov_name"],
            "prov_code": item["prov_code"],
            "city_name": item["city_name"],
            "city_code": item["city_code"]
        })
    })
shp.close()
