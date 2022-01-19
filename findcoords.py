from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
import folium

locator = Nominatim(user_agent="my_user_agent")
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

def coords(file):
        df = pd.read_csv(file)
        df.columns = df.columns.str.lower()
        df['location'] = df['address'].apply(geocode)
        df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
        df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)
        df = df.drop('location', 1)
        df=df.drop('point',1)
        df=df.drop('altitude',1)
        df.to_csv('file_withcoords.csv', encoding='utf-8')
    
def show_in_map(file):
    df=pd.read_csv(file)
    df.columns = df.columns.str.lower()
    lat = list(df["latitude"])
    lon = list(df["longitude"])
    addr = list(df["address"])
    
    html = """
    Address: %s<br>
    Lattitude: %s <br>
    Longitude: %s 
    """
    map = folium.Map(tiles="Stamen Terrain")
    fgv = folium.FeatureGroup(name = "Locations")

    for lt, ln, adr in zip(lat, lon, addr):
        try:
            iframe = folium.IFrame(html=html % (addr, lat, lon), width=200, height=100)
            fgv.add_child(folium.CircleMarker(location=[lt, ln],
                                        popup=folium.Popup(iframe),
                                        fill=True, color = 'grey', fill_opacity=0.7))
        except:
            pass
    map.add_child(fgv)
    map.add_child(folium.LayerControl())

    map.save("templates/Map_html_coords.html")