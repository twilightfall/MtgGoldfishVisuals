import pandas as pa
import matplotlib.pyplot as plt
import http.client as http
import json as js
import collections

color = {"W":"White", "U":"Blue", "B":"Black", "R":"Red", "G":"Green", "C":"Colorless"}
dual = (["W","U"],["W","B"],["U","B"],["U","R"],["B","R"],["B","G"],["R","G"],["R","W"],["G","W"],["G","U"])
tri = (["G","W","U"],["W","U","B"],["U","B","R"],["B","R","G"],["R","G","W"],["W","B","G"],["U","R","W"],["B","G","U"],["R","W","B"])
quad = (["W","U","B","R"],["U","B","R","G"],["B","R","G","W"],["R","G","W","U"],["G","W","U","B"])
wubrg = ('W','U','B','R','G')
order = ("W","U","B","R","G","C","WU","WB","UB","UR","BR","BG","RG","RW","GW","GU","GWU","WUB","UBR","BRG","RGW","WBG","URW","BGU","RWB","GUR","WUBR","UBRG","BRGW","RGWU","GWUB","WUBRG")

### GET DATA FROM GOOGLE SHEETS
data = pa.DataFrame(pa.read_csv("https://docs.google.com/spreadsheets/d/1nqQ01wzCNwJJOpVjLtOpPuOhm34CMwrZ1pImoZNOMhA/export?format=csv&gid=1802173994"))

rank = data[["Rank"]]
name = data["Name"]
perc = data[["% of Decks"]]
num = data[["# Played"]]

def pullAPIData():
    cmc = []
    colors = []
    names = list(name)
    conn = http.HTTPSConnection("api.scryfall.com")

    for n in names:
        conn.request("GET", ("/cards/named?exact={}".format(n).replace(" ", "+")))
        resp = js.loads(conn.getresponse().read())
        
        ### Create CMC (Converted Mana Cost) column
        cmc.append(int(resp["cmc"]))

        ### Create Colors column
        if len(resp["colors"]) > 0:
            if len(resp["colors"]) == 2:
                for sort_order in dual:
                    if all(item in resp['colors'] for item in sort_order) == True:
                        colors.append("".join([list for obj in sort_order for list in resp["colors"] if list[0] == obj]))
            elif len(resp["colors"]) == 3:
                for sort_order in tri:
                    if all(item in resp['colors'] for item in sort_order) == True:
                        colors.append("".join([list for obj in sort_order for list in resp["colors"] if list[0] == obj]))
            elif len(resp["colors"]) == 4:
                for sort_order in quad:
                    if all(item in resp['colors'] for item in sort_order) == True:
                        colors.append("".join([list for obj in sort_order for list in resp["colors"] if list[0] == obj]))
            elif len(resp["colors"]) == 5:
                colors.append("".join([list for obj in wubrg for list in resp["colors"] if list[0] == obj]))
            else:
                colors.append("".join(resp["colors"]))
        else:
            colors.append("C")

    data.insert(2, "CMC", cmc)
    data.insert(3, "Colors", colors)
    data['Colors'] = pa.Categorical(data['Colors'], categories = order)
    print(data.to_string(index = False))

pullAPIData()

### GET AVERAGE CONVERTED MANA COST
average = data["CMC"].mean()
print("Average converted mana cost of top cards: ", average)


### GET FREQUENCY OF CARDS BY COLOR/S
count = collections.Counter(data["Colors"])
count = sorted(count.items())
count = [tuple for x in order for tuple in count if tuple[0] == x]
frequency = [i[1] for i in count]
col = [i[0] for i in count]

### DISPLAY FREQUENCY GRAPH
plt.bar(col, frequency)
plt.show()