from tkinter.ttk import Entry

import numpy.compat
import pandas as pd
import folium
from tkinter import *

LATITUDE_COLUMN = 1
LONGITUDE_COLUMN = 2
CITY_NAME_COLUMN = 0


def convert_dtype_str(x):
    if not x:
        return ''
    try:
        return str(x)
    except:
        return ''


def convert_dtype_long(x):
    if not x:
        return 0
    try:
        return int(x)
    except:
        return 0


def convert_dtype_float(x):
    if not x:
        return 0.0
    try:
        return float(x)
    except:
        return 0.0



def close_window():
    global entry
    entry = E.get()
    root.destroy()



root = Tk()
E = Entry(root,width=60,background="white")
E.pack(anchor = CENTER)
B = Button(root, text = "Enter a City", command = close_window)
B.pack(anchor = S)
root.mainloop()



user_city = entry
cities = pd.read_csv('lib/uscities.csv',
                     converters={'Country': convert_dtype_str,
                                 'City': convert_dtype_str,
                                 'AccentCity': convert_dtype_str,
                                 'Region': convert_dtype_str,
                                 'Population': convert_dtype_long,
                                 'Latitude': convert_dtype_float,
                                 'Longitude': convert_dtype_float
                                 }

                     )

city_latitude = 39.9612
city_longitude = -82.9988

rowCount = 0
for rowData in cities.iterrows():

    city = rowData[1][CITY_NAME_COLUMN]
    if city == user_city:
        city_latitude = rowData[1][LATITUDE_COLUMN]
        city_longitude = rowData[1][LONGITUDE_COLUMN]

        print(city, city_latitude, city_longitude)

        break

# creating the map around user's city
loc_map = folium.Map(
    location=[city_latitude, city_longitude],
    width="100%",
    height="100%",
    zoom_control=2
)

if user_city == "atlanta":
    fileName = 'lib/FinalAtlanta.csv'
elif user_city == "new york":
    fileName = 'lib/ny_output.csv'

crimes = pd.read_csv(fileName,
                     converters={'city': convert_dtype_str,
                                 'crime': convert_dtype_str,
                                 'lat': convert_dtype_float,
                                 'long': convert_dtype_float})

# Add circle markers
folium.CircleMarker(location=[city_latitude, city_longitude], radius=[100]).add_to(loc_map)

count = 0
for crimeRowData in crimes.iterrows():

    if count == 100:
        crime = crimeRowData[1][1]
        count = 0

        if crime == 'theft':
            dangerLevel = 2
        elif crime == 'rape (or attempted)':
            dangerLevel = 4
        elif crime == 'accident':
            dangerLevel = 3
        elif crime == 'assault':
            dangerLevel = 4
        elif crime == 'murder':
            dangerLevel = 5
        elif crime == 'firearms':
            dangerLevel = 3
        else:
            dangerLevel = 1

        if dangerLevel == 1:
            color = '#5ED0FF'
        elif dangerLevel == 2:
            color = '#60D287'
        elif dangerLevel == 3:
            color = '#FFC55C'
        elif dangerLevel == 4:
            color = '#FF9239'
        else:
            color = '#C0341C'

        crime_lat = crimeRowData[1][2]
        crime_long = crimeRowData[1][3]

        folium.CircleMarker(location=[crime_lat, crime_long], radius=[20],popup=crime,
                            fill_color=color, fill=True, opacity=0.2).add_to(loc_map)

    count = count + 1

loc_map.save('test.html')
