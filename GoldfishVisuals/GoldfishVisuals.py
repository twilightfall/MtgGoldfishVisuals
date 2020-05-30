import numpy as np
import pandas as pa
import matplotlib.pyplot as mpl

data = pa.read_csv("https://docs.google.com/spreadsheets/d/1nqQ01wzCNwJJOpVjLtOpPuOhm34CMwrZ1pImoZNOMhA/export?format=csv&gid=1802173994")

#rank = data[["Rank"]]
#name = data[["Name"]]
#perc = data[["% of Decks"]]
#num = data[["# Played"]]

print(data)
d = pa.DataFrame(data)
d.hist()
mpl.show()

'''
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('GoldfishVisualizer-c3138a03c9e2.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Data dump").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)
'''