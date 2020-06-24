import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm

cmap = cm.get_cmap('Spectral') # Colour map

###############################################################################

data = pd.read_csv('sectoralloc.csv', delimiter=',', squeeze=True)
data['VALUE'] = data['VALUE'].astype(float)
# data['SECTOR'] = data['SECTOR'].str.lower()


dg = data.groupby(['SECTOR']).sum().reset_index()
dg.VALUE = pd.to_numeric(dg.VALUE, errors='coerce')

dg['HOLDINGS'] = ''

for i,sec in enumerate(dg['SECTOR']):
    h = list(data.loc[data['SECTOR'] == sec].SYMBOL)
    # print('sector: {} | holdings: {}'.format(sec,h))
    dg.at[i,'HOLDINGS'] = ': '+' '.join(h)

dg['sh'] = dg['SECTOR']+dg['HOLDINGS']


dg.VALUE.plot(kind='pie', autopct = "%.2f%%", labels=dg['sh'], cmap=cmap, legend=False)
plt.ylabel('')
plt.show()
