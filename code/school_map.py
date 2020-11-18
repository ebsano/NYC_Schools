""" school_map.py

    Required packages:
    - flask
    - folium
    - pandas

    Usage:

    Start the flask server by running:

        $ python school_map.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import Flask

import pandas as pd
import folium
import requests
from folium.plugins import MarkerCluster

app = Flask(__name__)

url = 'https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_School_Distrcts/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson'
request = requests.get(url)
districts = request.json()
data = pd.read_pickle('../data/map_data.pkl')


@app.route('/')
def school_map():
    schools_map = folium.Map(location=[40.693943, -73.985880])

    # layer
    folium.Choropleth(
        geo_data=districts,
        fill_opacity=0.7,
        line_opacity=0.7
    ).add_to(schools_map)

    # add a marker for every shcool
    marker_cluster = MarkerCluster().add_to(schools_map) # create marker clusters

    # add schools 
    for i in range(data.shape[0]):
        location = [data['latitude'][i], data['longitude'][i]]
        tooltip = f"School:{data['school_name'][i]}. \n Click for info."
        
        folium.Marker(location, # adding more details to the popup screen using HTML
                    popup="""
                    <i>Mean Math Score: </i> <br> <b>{}</b> <br>
                    <i>Math Score Ranking Percentile: </i> <br> <b>{}</b> <br>
                    <i>Mean ELA Score: </i><b><br>{}</b><br>
                    <i>ELA Score Ranking Percentile: </i><b><br>{}</b><br>
                    <i>Percent Agreement to Question: 'I feel safe in my classes in this school': </i><b><br>{}</b><br>""".format(
                        round(data['mean_score_math'][i], 2),
                        round(data['mean_score_math'].rank(pct=True, ascending=False)[i] * 100, 2),
                        round(data['mean_score_math'][i], 2), 
                        round(data['mean_score_ela'].rank(pct=True, ascending=False)[i] * 100, 2), 
                        round(data['safe'][i], 2)), 
                    tooltip=tooltip).add_to(marker_cluster)

    return schools_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)