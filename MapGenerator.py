import folium
import json

# open your json file
with open("faisalabad_food_businesses.json", "r", encoding="utf-8") as f:
    restaurants = json.load(f)

# create map centered on Faisalabad
map = folium.Map(location=[31.418, 73.079], zoom_start=12)

# add markers
for r in restaurants:
    
    try:
        lat = float(r["latitude"])
        lon = float(r["longitude"])
        name = r["name"]
        address = r["address"]
        rating = r["rating"]

        popup_text = f"{name}<br>{address}<br>Rating: {rating}"

        folium.Marker(
            location=[lat, lon],
            popup=popup_text
        ).add_to(map)

    except:
        pass


# save map
map.save("restaurants_map.html")

print("Map created successfully!")