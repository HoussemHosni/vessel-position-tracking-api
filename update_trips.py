from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sqlite3
import random
import os

def generate_map():
    """
        this function fetch the current vessels positions database
        and generate an updated chart where each trip has a diffrent colour
    """
    conn = sqlite3.connect("data.db")
    df = pd.read_sql_query("SELECT * FROM vessels_positions", conn)
    vessels_ids = df["vessel_id"].unique()
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF),range(n)))
    colors_list = get_colors(len(vessels_ids))

    fig = plt.figure(figsize=(35,35))

    m = Basemap(projection='mill',
            llcrnrlat = -90,
            urcrnrlat = 90,
            llcrnrlon = -180,
            urcrnrlon = 180,
            resolution = 'c')

    m.drawcoastlines()

    m.drawparallels(np.arange(-90,90,10),labels=[True,False,False,False])
    m.drawmeridians(np.arange(-180,180,30),labels=[0,0,0,1])

    for i, vessel_id in enumerate(vessels_ids):
        df_i = df[df["vessel_id"]==vessel_id]
        sites_lat_y = df_i['latitude'].tolist()
        sites_lon_x = df_i['longitude'].tolist()
        m.scatter(sites_lon_x,sites_lat_y,latlon=True, s=10, marker='o', alpha=1, edgecolor=colors_list[i], linewidth=2, zorder=50, label=f"vessel_id ={vessel_id}")

    plt.legend(loc="lower left", fontsize=30)
    plt.title('Vessels Trips', fontsize=50)
    plt.xlabel('longitude', fontsize=35)
    plt.ylabel('latitude', fontsize=35)
    os.remove('static/img/map.png')
    plt.savefig('static/img/map.png')