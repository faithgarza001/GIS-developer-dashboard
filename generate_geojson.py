import json

geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Python Point"},
            "geometry": {
                "type": "Point",
                "coordinates": [-97.7431, 30.2672]  # Austin, TX
            }
        }
    ]
}

with open("python_point.geojson", "w") as f:
    json.dump(geojson, f, indent=2)

print("✅ GeoJSON file created: python_point.geojson")
