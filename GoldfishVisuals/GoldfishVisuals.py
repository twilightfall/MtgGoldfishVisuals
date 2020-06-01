import numpy as np
import pandas as pa
import matplotlib.pyplot as mpl
import http.client as http
import json as js

col = {"White":"W", "Blue":"U", "Black":"B", "Red":"R", "Green":"G", "Colorless":"C"}
order = ["W","U","B","R","G","C"]
data = pa.DataFrame(pa.read_csv("https://docs.google.com/spreadsheets/d/1nqQ01wzCNwJJOpVjLtOpPuOhm34CMwrZ1pImoZNOMhA/export?format=csv&gid=1802173994"))

rank = data[["Rank"]]
name = data["Name"]
perc = data[["% of Decks"]]
num = data[["# Played"]]

#names = list(name)

#conn = http.HTTPSConnection("api.scryfall.com")
#conn.request("GET", ("/cards/named?exact={}".format(names[15]).replace(" ", "+")))

#resp = conn.getresponse().read()
#respdata = js.loads(resp)

#colors = []
#colors.append(respdata["colors"])
#res = [list for x in order for list in colors[0] if list[0] == x] 

#print(type(data.to_string(index= False)))

#def GetColors():
#    colors = []
#    names = list(name)
#    conn = http.HTTPSConnection("api.scryfall.com")

#    for n in names:
#        conn.request("GET", ("/cards/named?exact={}".format(n).replace(" ", "+")))
#        resp = js.loads(conn.getresponse().read())
        

#    #print(colors)
#    data.insert(2, "Colors", colors)
#    print(data.to_string(index = False))

#GetColors()

def pullAPIData():
    cmc = []
    colors = []
    names = list(name)
    conn = http.HTTPSConnection("api.scryfall.com")

    for n in names:
        conn.request("GET", ("/cards/named?exact={}".format(n).replace(" ", "+")))
        resp = js.loads(conn.getresponse().read())
        
        # Create CMC column
        cmc.append(int(resp["cmc"]))

        # Create Colors column
        if len(resp["colors"]) > 0:
            colors.append("".join([list for y in order for list in resp["colors"] if list[0] == y]))
        else:
            colors.append("C")

    data.insert(2, "CMC", cmc)
    data.insert(3, "Colors", colors)
    print(data.to_string(index = False))

pullAPIData()

average = data["CMC"].mean()
print(average)