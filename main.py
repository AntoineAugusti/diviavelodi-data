import divia_api
from divia_api import DiviaAPI
from divia_api.velodi import update_source as update_source
from cachetools import cached, TTLCache

import math
import datetime
import csv


@cached(cache=TTLCache(ttl=30, maxsize=math.inf))
def cached_update_source():
    return update_source()


divia_api.velodi.update_source = cached_update_source

date = datetime.datetime.now().replace(microsecond=0).isoformat()

data = []
velodi_api = DiviaAPI().velodi
for station in velodi_api.stations:
    availability = station.check()
    data.append(
        {
            "date": date,
            "id_station": station.code,
            "nom_station": station.friendly_name,
            "nb_velos": availability.bikes,
            "nb_places": availability.docks,
        }
    )

with open("data/data.csv", "a+") as f:
    writer = csv.DictWriter(f, data[0].keys(), lineterminator="\n")
    if f.tell() == 0:
        writer.writeheader()
    writer.writerows(data)
