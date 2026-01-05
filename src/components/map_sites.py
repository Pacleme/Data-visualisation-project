import pandas as pd
import folium
import regex

def process_sites_data():
    raw_sites_data = pd.read_csv("data/raw/paris-2024-sites-de-competition.csv",delimiter=';')
    
    cleaned_sites_data = raw_sites_data[["Nom_Site", "Sports", "point_geo"]]
    cleaned_sites_data.insert(cleaned_sites_data.shape[1], 'Nb_sports', cleaned_sites_data['Sports'].apply(lambda x: len(x.split(","))))
    cleaned_sites_data.insert(cleaned_sites_data.shape[1], 'link', cleaned_sites_data['Nom_Site'].apply(lambda x: regex.sub('[^A-Za-z0-9_]+', '', x.replace(" ","_"))) + ".html")


    cleaned_sites_data.to_csv("data/cleaned/paris-2024-sites-de-competition.csv", index=False, sep=';')

def link(str, linkk):
    return f'<a href="{linkk}">{str}</a>'

def map_sites():
    sites_data = pd.read_csv("data/cleaned/paris-2024-sites-de-competition.csv",delimiter=';')

    coords = (48.7190835,2.4609723)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=9)

    for i, row in sites_data.iterrows():
        # folium.Marker(
        #     location=row['point_geo'].split(","), 
        #     popup=row['Sports'],
        #     icon=folium.Icon(color='blue')
        # ).add_to(map)

        folium.CircleMarker(
            location=row['point_geo'].split(","),
            radius=row['Nb_sports'] * 5,
            popup=link(row['Sports'],row['link']),
            # color=cm(color),
            fill=True,
            # fill_color=cm(color)
        ).add_to(map)

    map.save(outfile="map_sites.html")

def testFolium():
    # Create map
    coords = (48.8398094,2.5840685)
    map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=15)

    # Add PoI
    folium.Marker(location=coords, popup="ESIEE Paris").add_to(map)

    map.save(outfile='map_test.html')

if __name__ == "__main__":
    print("map_sites module")

    # process_sites_data()
    map_sites()
    # testFolium()