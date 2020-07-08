import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import yfinance as yf
from urllib.request import Request, urlopen
from lxml.html import parse
from lxml.etree import tostring


cmap = cm.get_cmap('Spectral') # Colour map

###############################################################################
def getSector(name):
    req = Request('https://finance.yahoo.com/quote/'+name+'/profile?p='+name, headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req)
    tree = parse(webpage)
    html = tostring(tree)

    sector = ''
    content = tree.xpath('//*[self::span]')
    for i,tag in enumerate(content):
        x = tag.text
        # print(x)
        if(x == 'Sector'):
            sector = content[i+1].text
            break

        if(sector == ''):
            sector = 'ETF'

    return(sector)

###############################################################################


data = pd.read_csv('table.csv', delimiter=',', squeeze=True)
data['VALUE'] = data['VALUE'].astype(float)
data['SECTOR'] = ''

# use yfinance to get the sector for each ticker
for i in data.index:
    ticker = data.loc[i]['SYMBOL']
    sector = getSector(ticker)
    
    data.at[i,'SECTOR'] = sector
    print(i,ticker,sector)


# now do the grouping and counting etc
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
